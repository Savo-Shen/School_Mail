#!/usr/bin/env bash
#
# 需要 root 的收尾步骤（安装 systemd 单元 + nginx 配置）。
# 这台服务器 sudo 需要密码，所以这部分没法自动化，请手动执行：
#
#   sudo bash ~/school_mail/deploy/finish-install.sh
#
# 前面的步骤（装 uv、同步依赖、生成 .env、迁移、collectstatic）都已完成。

set -euo pipefail

APP_DIR=/home/savo_shen/school_mail
NGINX_CONF=/etc/nginx/conf.d/ideccs.savo-shen.com.conf
BACKUP=/root/ideccs.savo-shen.com.conf.bak.$(date +%Y%m%d%H%M%S)

[ "$(id -u)" -eq 0 ] || { echo "请用 sudo 运行" >&2; exit 1; }

echo "==> 1/5 停掉手动启动的测试进程"
[ -f /tmp/sm_test.pid ] && kill "$(cat /tmp/sm_test.pid)" 2>/dev/null || true
rm -f /tmp/sm_test.pid
sleep 1

echo "==> 2/5 安装 systemd 单元"
install -m 644 "$APP_DIR/deploy/school-mail.service" /etc/systemd/system/school-mail.service
systemctl daemon-reload
systemctl enable --now school-mail
sleep 3
systemctl is-active --quiet school-mail || {
  echo "!! 服务未能启动，日志："; journalctl -u school-mail -n 30 --no-pager; exit 1;
}
echo "    服务已启动"

echo "==> 3/5 本地健康检查"
curl -fsS -H 'Host: ideccs.savo-shen.com' -H 'X-Forwarded-Proto: https' \
     http://127.0.0.1:8000/api/health/ && echo

echo "==> 4/5 安装 nginx 配置（先备份原有的）"
[ -f "$NGINX_CONF" ] && cp "$NGINX_CONF" "$BACKUP" && echo "    原配置已备份到 $BACKUP"
install -m 644 "$APP_DIR/deploy/nginx.conf" "$NGINX_CONF"
nginx -t
systemctl reload nginx
echo "    nginx 已重载"

echo "==> 5/5 通过 nginx 验证"
curl -fsS https://ideccs.savo-shen.com/api/health/ && echo
echo
echo "✓ 安装完成。接下来："
echo "  1. 创建管理员账号（需要你自己设密码）："
echo "     cd $APP_DIR/src/backend && .venv/bin/python manage.py createsuperuser"
echo "  2. 发布前端（见 doc/deployment.md 第三步）"
echo "  3. 记得给 R2 桶配 CORS 策略，否则前端页面会白屏"
