#!/usr/bin/env bash
#
# 从本地把后端代码同步到服务器，然后触发部署。
#
#   deploy/rsync-backend.sh
#
# 适用场景：服务器到 GitHub 的连接不稳（GnuTLS recv error），
# 或者你还没把改动 push 上去、想先在服务器上验证。
#
# 排除项保证服务器上的 .env、数据库、虚拟环境、静态文件不被覆盖。

set -euo pipefail

HOST="${DEPLOY_HOST:-savo}"
DEST="${DEPLOY_PATH:-~/school_mail}"

cd "$(dirname "$0")/.."

echo "==> 同步代码到 $HOST:$DEST"
rsync -az --info=stats1 \
  --exclude '.venv' --exclude '__pycache__' --exclude '*.pyc' \
  --exclude 'db.sqlite3' --exclude '.env' --exclude 'staticfiles' \
  --exclude '.DS_Store' --exclude '.git' \
  --include 'src/' --include 'src/backend/***' \
  --include 'deploy/***' --include 'doc/***' --include 'README.md' \
  --exclude '*' \
  ./ "$HOST:$DEST/"

echo
echo "==> 在服务器上执行部署（跳过 git pull）"
ssh "$HOST" "cd $DEST && export PATH=\"\$HOME/.local/bin:\$PATH\" && SKIP_PULL=1 ./deploy/deploy.sh"
