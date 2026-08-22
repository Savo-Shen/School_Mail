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

# 服务器到 GitHub 的连接不稳（常见 GnuTLS recv error，要重试几次才通），
# 所以支持跳过拉取：从本地 rsync 完代码后用 SKIP_PULL=1 跑本脚本即可。
if [ "${SKIP_PULL:-0}" = "1" ]; then
  echo "==> 跳过 git pull（SKIP_PULL=1）"
elif [ -d .git ]; then
  echo "==> 拉取最新代码"
  ok=0
  for i in 1 2 3; do
    if git pull --ff-only; then ok=1; break; fi
    echo "    第 $i 次失败，重试..."; sleep 5
  done
  [ "$ok" = "1" ] || { echo "!! git pull 三次都失败。可以改用本地 rsync + SKIP_PULL=1：" >&2
                       echo "   deploy/rsync-backend.sh" >&2; exit 1; }
else
  echo "==> 非 git 仓库，跳过拉取（假定代码已由 rsync 同步）"
fi

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
# 用 sudo -n（非交互）：这台机器的 sudo 需要密码，
# 装了 /etc/sudoers.d/school-mail 之后这一步才能免密自动完成。
if sudo -n systemctl restart "$SERVICE" 2>/dev/null; then
  sleep 2
  sudo -n systemctl is-active --quiet "$SERVICE" || {
    echo "!! 服务未能启动，看日志：journalctl -u $SERVICE -n 50" >&2
    exit 1
  }
else
  echo
  echo "  !! 无法免密重启服务。代码和依赖都已更新，只差重启这一步。"
  echo
  echo "  手动执行： sudo systemctl restart $SERVICE"
  echo
  echo "  想让以后全自动，装一个只放行这几条命令的 sudoers 规则："
  echo "    sudo install -m 440 -o root -g root \\"
  echo "      $APP_DIR/deploy/sudoers-school-mail /etc/sudoers.d/school-mail"
  echo
  exit 2
fi

echo "==> 健康检查"
curl -fsS http://127.0.0.1:8000/api/health/ && echo
echo "✓ 部署完成"
