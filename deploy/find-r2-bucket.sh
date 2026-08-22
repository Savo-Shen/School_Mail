#!/usr/bin/env bash
#
# 探测 cdn.savo-shen.com 到底绑的是哪个 R2 桶、以及对象前缀是什么。
#
#   deploy/find-r2-bucket.sh
#
# 做法：往候选桶里写一个临时探针对象，再从 CDN 上把它取回来，
# 能取到的那个组合就是正确答案。跑完会自动删掉探针。
#
# 之所以需要探测：R2 的作用域 token 没有 ListBuckets 权限，
# `rclone lsd r2:` 列不出桶，只能靠实际写入来判断。

set -uo pipefail

REMOTE="${R2_REMOTE:-r2}"
CDN="${CDN_HOST:-https://cdn.savo-shen.com}"
CANDIDATES=("${@:-}")
[ -z "${CANDIDATES[0]:-}" ] && CANDIDATES=(savo-bucket goods)

export RCLONE_S3_NO_CHECK_BUCKET=true

TOKEN="probe-$$-$(od -An -N4 -tx4 /dev/urandom | tr -d ' ')"
TMP=$(mktemp)
echo "$TOKEN" > "$TMP"

echo "=== 第一步：哪些桶可写 ==="
WRITABLE=()
for b in "${CANDIDATES[@]}"; do
  printf "  %-12s " "$b"
  ERR=$(rclone copyto "$TMP" "$REMOTE:$b/__probe_$TOKEN.txt" 2>&1 | grep -o "NoSuchBucket\|AccessDenied\|Forbidden" | head -1)
  if [ -z "$ERR" ]; then
    echo "可写 ✓"; WRITABLE+=("$b")
  else
    echo "$ERR"
  fi
done

if [ ${#WRITABLE[@]} -eq 0 ]; then
  echo; echo "!! 没有任何候选桶可写。请到 Cloudflare 控制台 R2 页面确认桶名，然后："
  echo "   deploy/find-r2-bucket.sh 你的桶名"
  rm -f "$TMP"; exit 1
fi

echo
echo "=== 第二步：哪个桶 + 前缀能从 CDN 取到 ==="
FOUND=""
for b in "${WRITABLE[@]}"; do
  for prefix in "" "ideccs"; do
    KEY="${prefix:+$prefix/}__probe_$TOKEN.txt"
    # 探针刚才写在桶根，这里把它也复制到带前缀的位置
    [ -n "$prefix" ] && rclone copyto "$TMP" "$REMOTE:$b/$KEY" >/dev/null 2>&1
    URL="$CDN/$KEY"
    BODY=$(curl -s --max-time 20 "$URL" 2>/dev/null | tr -d "[:space:]")
    printf "  桶=%-10s 前缀=%-8s -> %s  " "$b" "${prefix:-（无）}" "$URL"
    if [ "$BODY" = "$TOKEN" ]; then
      echo "命中 ✓"; FOUND="$b|$prefix"
    else
      echo "取不到"
    fi
  done
done

echo
echo "=== 清理探针 ==="
for b in "${WRITABLE[@]}"; do
  rclone deletefile "$REMOTE:$b/__probe_$TOKEN.txt" 2>/dev/null
  rclone deletefile "$REMOTE:$b/ideccs/__probe_$TOKEN.txt" 2>/dev/null
done
rm -f "$TMP"
echo "  完成"

echo
if [ -n "$FOUND" ]; then
  B="${FOUND%%|*}"; P="${FOUND##*|}"
  echo "✓ 结论：桶 = $B，前缀 = ${P:-（无，即桶根就是 cdn.savo-shen.com 根）}"
  echo
  echo "用这条命令发布："
  if [ -n "$P" ]; then
    echo "  R2_BUCKET=$B R2_PREFIX=$P deploy/upload-r2.sh"
  else
    echo "  R2_BUCKET=$B R2_PREFIX=ideccs deploy/upload-r2.sh"
    echo "  （前缀仍用 ideccs，这样资源落在 $CDN/ideccs/ 下，和构建时的 base 一致）"
  fi
else
  echo "!! 桶可写但 CDN 上取不到探针。可能是 ESA 缓存了 404，或域名绑的是别的桶。"
  echo "   建议到 Cloudflare 控制台 R2 -> 各桶 -> Settings -> Custom Domains，"
  echo "   看 cdn.savo-shen.com 挂在哪个桶下。"
fi
