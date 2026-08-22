#!/usr/bin/env bash
# 原地压缩静态图片，保持文件名与扩展名不变（所以不需要改任何引用）。
# 原图都在 git 里，随时 `git checkout -- <path>` 可还原。
set -uo pipefail

JPEG_MAX=2560     # JPEG 长边上限（多为整屏背景/相册照片）
PNG_MAX=1920      # PNG 长边上限
JPEG_QUALITY=82
MIN_BYTES=$((300 * 1024))   # 小于这个体积且尺寸达标的就不动，避免二次损失

total_before=0
total_after=0
changed=0

process() {
  local f="$1" ext="$2"
  local before after w h max
  before=$(stat -f%z "$f")

  w=$(magick identify -format "%w" "$f" 2>/dev/null) || return
  h=$(magick identify -format "%h" "$f" 2>/dev/null) || return
  [ -z "$w" ] && return

  if [ "$ext" = "png" ]; then max=$PNG_MAX; else max=$JPEG_MAX; fi
  local long=$(( w > h ? w : h ))

  # 尺寸已达标且体积不大 -> 跳过
  if [ "$long" -le "$max" ] && [ "$before" -lt "$MIN_BYTES" ]; then
    total_before=$((total_before + before)); total_after=$((total_after + before)); return
  fi

  local tmp="${f}.opt.tmp"
  if [ "$ext" = "png" ]; then
    # 有 alpha 的先只缩放；体积仍大再做 256 色量化（logo/图标量化效果很好）
    local alpha; alpha=$(magick identify -format "%A" "$f" 2>/dev/null)
    magick "$f" -auto-orient -resize "${max}x${max}>" -strip "$tmp" 2>/dev/null || { rm -f "$tmp"; return; }
    if [ "$(stat -f%z "$tmp")" -gt $((200 * 1024)) ]; then
      magick "$f" -auto-orient -resize "${max}x${max}>" -strip -colors 256 "PNG8:$tmp" 2>/dev/null || true
    fi
  else
    magick "$f" -auto-orient -resize "${max}x${max}>" -strip \
      -interlace Plane -sampling-factor 4:2:0 -quality $JPEG_QUALITY "$tmp" 2>/dev/null || { rm -f "$tmp"; return; }
  fi

  [ -f "$tmp" ] || return
  after=$(stat -f%z "$tmp")

  # 只有确实变小才替换
  if [ "$after" -lt "$before" ]; then
    mv "$tmp" "$f"
    changed=$((changed + 1))
    total_before=$((total_before + before)); total_after=$((total_after + after))
    printf "  %7s -> %7s  (-%2d%%)  %s\n" \
      "$(numfmt --to=iec $before 2>/dev/null || echo ${before})" \
      "$(numfmt --to=iec $after 2>/dev/null || echo ${after})" \
      "$(( 100 - after * 100 / before ))" "${f#./}"
  else
    rm -f "$tmp"
    total_before=$((total_before + before)); total_after=$((total_after + before))
  fi
}

echo "=== 开始压缩 ==="
while IFS= read -r -d '' f; do
  case "${f##*.}" in
    png|PNG) process "$f" png ;;
    jpg|JPG|jpeg|JPEG) process "$f" jpg ;;
  esac
done < <(find "$@" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) -print0)

echo
echo "=== 汇总 ==="
echo "处理文件数: $changed"
echo "总体积: $((total_before/1024/1024)) MB -> $((total_after/1024/1024)) MB  (减少 $(( 100 - total_after * 100 / total_before ))%)"
