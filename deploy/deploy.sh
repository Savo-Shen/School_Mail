#!/usr/bin/env bash
# 后端部署脚本 —— 在服务器上执行。
#
#   ssh savo
#   cd /home/savo_shen/school_mail && ./deploy/deploy.sh
#
# 第一次部署见 doc/deployment.md，这个脚本只负责「更新到最新代码并重启」。

set -euo pipefail

APP_DIR="${APP_DIR:-/home/savo_shen/school_mail}"
BACKEND_DIR="$APP_DIR/src/backend"
SERVICE="school-mail"

cd "$APP_DIR"

echo "==> 拉取最新代码"
git pull --ff-only

cd "$BACKEND_DIR"

if [ ! -f .env ]; then
  echo "!! 缺少 $BACKEND_DIR/.env，先参考 .env.example 创建" >&2
  exit 1
fi

echo "==> 同步依赖"
# 只有这一步用 uv（会联网），其余一律直接调 venv 里的可执行文件 ——
# uv run 每次都要校验依赖，在这台机器上慢到不可用。
uv sync --no-dev

echo "==> 数据库迁移"
"$BACKEND_DIR/.venv/bin/python" manage.py migrate --noinput

echo "==> 收集静态文件"
"$BACKEND_DIR/.venv/bin/python" manage.py collectstatic --noinput

# 用 filecache 时确保目录存在（CACHE_URL=filecache:///var/tmp/school_mail_cache）
CACHE_DIR=$(sed -n 's#^CACHE_URL=filecache://##p' .env | tr -d '\r')
if [ -n "$CACHE_DIR" ]; then
  mkdir -p "$CACHE_DIR"
  echo "==> 缓存目录就绪: $CACHE_DIR"
fi

echo "==> 生产环境自检"
"$BACKEND_DIR/.venv/bin/python" manage.py check --deploy --fail-level WARNING

echo "==> 重启服务"
sudo systemctl restart "$SERVICE"
sleep 2
sudo systemctl is-active --quiet "$SERVICE" || {
  echo "!! 服务未能启动，看日志：journalctl -u $SERVICE -n 50" >&2
  exit 1
}

echo "==> 健康检查"
curl -fsS http://127.0.0.1:8000/api/health/ && echo
echo "✓ 部署完成"
