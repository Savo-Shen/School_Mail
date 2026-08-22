#!/usr/bin/env bash
#
# 把前端构建产物发布到 Cloudflare R2（前面套着阿里云 ESA 做国内加速）。
#
# 用法：
#   cd src/frontend && pnpm build
#   deploy/upload-r2.sh                 # 上传（不删旧文件）
#   deploy/upload-r2.sh --prune         # 上传并清理远端多余文件（见下方说明）
#   R2_BUCKET=goods deploy/upload-r2.sh # 指定别的桶
#
# 前置条件：
#   1. rclone 已配置好名为 r2 的 remote（type=s3, provider=Cloudflare）
#   2. R2 桶已配置 CORS 策略，允许 https://ideccs.savo-shen.com
#      —— 不配的话 <script type="module" crossorigin> 会被浏览器拦掉，页面全白。
#      策略见 doc/deployment.md
#
# 注意 index.html 不在上传范围内：它由服务器上的 nginx 提供，
# 这样才能用 try_files 做 SPA 回退（R2 是纯对象存储，没有目录索引和回退）。

set -euo pipefail

REMOTE="${R2_REMOTE:-r2}"
BUCKET="${R2_BUCKET:-savo-bucket}"   # cdn.savo-shen.com 绑定的桶
PREFIX="${R2_PREFIX:-ideccs}"
DIST="${DIST:-src/frontend/ideccs}"
DEST="${REMOTE}:${BUCKET}/${PREFIX}"

PRUNE=0
[ "${1:-}" = "--prune" ] && PRUNE=1

# rclone 默认在上传前会探测桶是否存在，探测失败就尝试 CreateBucket。
# R2 的作用域 token 通常只有对象读写权限、没有桶级权限，于是每个文件都会
# 报 "operation error S3: CreateBucket ... AccessDenied"。
# 这个开关让 rclone 直接写对象，跳过桶探测。
export RCLONE_S3_NO_CHECK_BUCKET=true

cd "$(dirname "$0")/.."

if [ ! -f "$DIST/index.html" ]; then
  echo "!! 没找到构建产物 $DIST/index.html，先执行： cd src/frontend && pnpm build" >&2
  exit 1
fi

echo "==> 目标: $DEST"
echo "==> 本地: $DIST"
echo

# ---------------------------------------------------------------------------
# 1) 带内容哈希的 assets：文件名变则内容变，可以放心设一年 immutable 强缓存
# ---------------------------------------------------------------------------
echo "==> 上传 assets/（一年强缓存）"
rclone copy "$DIST/assets" "$DEST/assets" \
  --header-upload "Cache-Control: public, max-age=31536000, immutable" \
  --transfers 8 --checkers 16 --progress --stats-one-line

# ---------------------------------------------------------------------------
# 2) 其余文件名不带哈希（KeepRunning、linzidaren、favicon），用较短缓存，
#    保证替换后能在一天内自然过期
# ---------------------------------------------------------------------------
echo
echo "==> 上传其余静态文件（1 天缓存）"
for item in KeepRunning linzidaren; do
  [ -d "$DIST/$item" ] || continue
  rclone copy "$DIST/$item" "$DEST/$item" \
    --header-upload "Cache-Control: public, max-age=86400" \
    --transfers 8 --checkers 16 --stats-one-line
done

rclone copy "$DIST" "$DEST" \
  --include "*.ico" \
  --header-upload "Cache-Control: public, max-age=86400" \
  --stats-one-line

# ---------------------------------------------------------------------------
# 3) 可选清理。默认不删：刚发版时可能还有用户拿着旧的 index.html，
#    立刻删掉旧 assets 会让他们白屏。建议发版几天后再跑 --prune。
# ---------------------------------------------------------------------------
if [ "$PRUNE" = "1" ]; then
  echo
  echo "==> 清理远端多余文件（旧构建产物）"
  read -r -p "    这会删除 $DEST 下本地不存在的文件，确认？[y/N] " ans
  case "$ans" in
    [yY]) rclone sync "$DIST" "$DEST" --exclude "index.html" --progress ;;
    *) echo "    已跳过" ;;
  esac
fi

# ---------------------------------------------------------------------------
# 4) 缓存预热 —— 这一步不能省。
#
# R2 会正确返回 `Vary: Origin`，但阿里云 ESA **不遵守** 它：一个 URL 只缓存
# 一个变体，谁先访问就定型。如果某个新资源第一次是被不带 Origin 的请求
# （爬虫、监控、别人直接点链接）取走的，那份**没有 CORS 头**的响应就会被缓存，
# 之后浏览器加载 ES module 全部失败 —— 而 assets 设的是 immutable + 一年强缓存，
# 等于白屏一年。
#
# 所以上传完立刻用带 Origin 的请求把每个资源都拉一遍，抢先把正确的变体灌进缓存。
# 根治方案见 doc/deployment.md：在 ESA 上加一条无条件写入 ACAO 的响应头规则。
# ---------------------------------------------------------------------------
ORIGIN="${SITE_ORIGIN:-https://ideccs.savo-shen.com}"
CDN_BASE="${CDN_BASE:-https://cdn.savo-shen.com/${PREFIX}}"

echo
echo "==> 预热 CDN 缓存（带 Origin，抢占正确的 CORS 变体）"
WARM=0; COLD=0
while IFS= read -r rel; do
  URL="$CDN_BASE/$rel"
  if curl -sI --max-time 30 -H "Origin: $ORIGIN" "$URL" | grep -qi "access-control-allow-origin"; then
    WARM=$((WARM+1))
  else
    COLD=$((COLD+1)); echo "    !! 无 CORS 头: $rel"
  fi
done < <(cd "$DIST" && find assets -type f \( -name "*.js" -o -name "*.css" \) | sed "s|^|assets/|;s|^assets/assets/|assets/|")
echo "    已预热 $WARM 个，异常 $COLD 个"
if [ "$COLD" -gt 0 ]; then
  echo "    !! 有资源拿不到 CORS 头，很可能是 ESA 已经缓存了错误变体。"
  echo "       请到阿里云 ESA 控制台刷新这些路径的缓存后重跑本脚本。"
fi

# ---------------------------------------------------------------------------
# 5) 自检：确认刚上传的文件真的能从 CDN 取到。
#    这一步能立刻抓出「传错桶」——账号下有 cdn 和 ideccs 两个桶，
#    而域名只绑定了其中一个，传错的话文件在 R2 里但 URL 404。
# ---------------------------------------------------------------------------
CDN_BASE="${CDN_BASE:-https://cdn.savo-shen.com/${PREFIX}}"
PROBE=$(ls "$DIST/assets"/index-*.js 2>/dev/null | head -1)

if [ -n "$PROBE" ]; then
  PROBE_URL="$CDN_BASE/assets/$(basename "$PROBE")"
  echo
  echo "==> 自检: $PROBE_URL"
  CODE=$(curl -so /dev/null -w "%{http_code}" --max-time 25 \
         -H "Origin: https://ideccs.savo-shen.com" "$PROBE_URL" || echo 000)
  ACAO=$(curl -sI --max-time 25 -H "Origin: https://ideccs.savo-shen.com" "$PROBE_URL" \
         | grep -ic "access-control-allow-origin" || true)

  if [ "$CODE" != "200" ]; then
    echo "    !! HTTP $CODE —— 文件取不到。可能是桶选错了（当前 R2_BUCKET=$BUCKET）。"
    echo "       换另一个试试： R2_BUCKET=ideccs $0"
    exit 1
  fi
  if [ "$ACAO" = "0" ]; then
    echo "    !! 取到了文件但没有 Access-Control-Allow-Origin 响应头。"
    echo "       前端会因为跨域加载 ES module 失败而白屏。"
    echo "       检查 R2 桶的 CORS 策略，并刷新阿里云 ESA 缓存。"
    exit 1
  fi
  echo "    HTTP 200 + CORS 头正常 ✓"
fi

echo
echo "✓ 上传完成并自检通过"
echo
echo "下一步：把 index.html 放到服务器（它不上 R2，由 nginx 提供以支持 SPA 回退）"
echo "  scp $DIST/index.html savo:/tmp/index.html"
echo "  ssh savo 'sudo install -m 644 /tmp/index.html /var/www/ideccs/index.html'"
