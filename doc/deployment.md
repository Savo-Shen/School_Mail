# 部署指南

## 当前部署进度（2026-08-22）

| 步骤 | 状态 |
| :--- | :--- |
| 代码同步到 `~/school_mail` | ✅ 已完成（rsync，暂未走 git） |
| 安装 uv + `uv sync --no-dev` | ✅ 已完成 |
| 生成 `.env`（SECRET_KEY 在服务器本地生成） | ✅ 已完成 |
| `migrate` + `collectstatic` | ✅ 已完成（全新空库） |
| `check --deploy` | ✅ 零告警 |
| gunicorn 手动启动验证 | ✅ 全部接口正常，PSS 80.7MB |
| **安装 systemd 单元 + nginx 配置** | ⏳ **需要 sudo，见下** |
| 创建管理员账号 | ⏳ 需要你设密码 |
| R2 CORS 策略 | ⏳ 需要在 Cloudflare 控制台配置 |
| 发布前端 | ⏳ 待后端就绪后进行 |

需要 root 的步骤已经打包成一个脚本，登录服务器后执行：

```bash
sudo bash ~/school_mail/deploy/finish-install.sh
```

它会：停掉手动测试进程 → 安装并启动 systemd 服务 → 本地健康检查 →
备份并替换 nginx 配置 → `nginx -t` 后重载 → 通过公网域名做一次验证。
任何一步失败即中止。

> 这台服务器的 sudo 需要密码，所以这部分无法自动化。

## 架构

```
                        ┌─────────────────────────────────────────┐
  国内用户 ─────────────▶│  阿里云 ESA（中国移动节点 223.111.27.x）   │
       │                │        cdn.savo-shen.com                │
       │                └──────────────────┬──────────────────────┘
       │                                   │ 回源
       │                        ┌──────────▼──────────┐
       │                        │  Cloudflare R2      │
       │                        │  桶前缀 ideccs/      │
       │                        │  assets/ 等 20MB     │
       │                        └─────────────────────┘
       │
       │                ┌─────────────────────────────────────────┐
       └───────────────▶│  云服务器 129.211.8.114（灰云直连）        │
                        │      ideccs.savo-shen.com               │
                        │        Nginx:443                        │
                        │          ├── /       → index.html (4KB) │
                        │          └── /api/   → gunicorn:8000     │
                        │                         └─▶ Django + DRF │
                        └─────────────────────────────────────────┘
```

**职责划分**

| 内容 | 体积 | 放哪 | 为什么 |
| :--- | :--- | :--- | :--- |
| `assets/`、`KeepRunning/`、`linzidaren/` | ~20MB | R2 + ESA | 重资源走国内加速，不占服务器带宽 |
| `index.html` | 4KB | nginx | R2 做不了 SPA 回退，见下 |
| `/api/*` | — | nginx → gunicorn | 和前端同域，**零 CORS** |

## 为什么 index.html 不能也放 R2

R2 是纯对象存储，没有目录索引、没有 SPA 回退、`_redirects` 不生效。实测：

```
https://cdn.savo-shen.com/ideccs/                  → 404   没有 index document
https://cdn.savo-shen.com/ideccs/login             → 404   没有 SPA 回退
https://cdn.savo-shen.com/ideccs/assets/index.js   → 200   显式对象才行
```

把 4KB 的 index.html 留在 nginx 上，一行 `try_files $uri /index.html` 就解决了，
而且顺带让 API 和前端同域 —— 少掉一整类 CORS 故障。服务器每次页面加载只出 4KB，
负载可以忽略。

---

## 坑：阿里云 ESA 不遵守 `Vary: Origin`（已通过 ESA 规则根治）

记录一下，避免以后换 CDN 或改配置时再踩。

R2 侧一切正常：配了 CORS 策略后带 `Origin` 的请求能拿到
`Access-Control-Allow-Origin`，响应里也正确带了 `Vary: Origin`。
**但 ESA 忽略 `Vary: Origin`** —— 一个 URL 只缓存一个变体，谁先访问就定型：

| 首次访问方式 | 之后带 Origin 再取 |
| :--- | :--- |
| 不带 Origin | 拿不到 ACAO |
| 带 Origin | 正常 |

后果很严重：新资源如果被不带 Origin 的请求（爬虫、uptime 监控、别人直接粘链接）
先取走，那份没有 CORS 头的响应就会进缓存，浏览器加载 ES module 被跨域拦截。
而 `assets/*` 设的是 `immutable, max-age=31536000` —— **白屏一年**。

### 根治方案（已实施）

阿里云 ESA → 规则 → 转换规则 → **修改响应头** → **ESA 到客户端**，
新增规则 `cors-acao-ideccs`：

- 匹配条件：`starts_with(http.request.uri.path, "/ideccs/")`
- 操作（两条，顺序不能反）：

| 顺序 | 类型 | 操作方式 | 响应头名称 | 响应头值 |
| :---: | :--- | :--- | :--- | :--- |
| 1 | 静态 | **删除** | `Access-Control-Allow-Origin` | —— |
| 2 | 静态 | **添加** | `Access-Control-Allow-Origin` | `https://ideccs.savo-shen.com` |

两个关键点，都是实测踩出来的：

1. **不能用「变更」**。ESA 的「变更」只修改**已存在**的响应头，头缺失时不会创建 ——
   而缓存里那份被污染的变体恰恰就是没有这个头，所以「变更」救不了它。
   必须「删除 + 添加」：先清掉源站可能带的，再无条件写入。
2. **不能只用「添加」**。R2 在请求带 Origin 时本来就会回一个 ACAO，
   只加不删会变成两个同名响应头，浏览器同样判定跨域失败。
3. **匹配条件必须限定 `/ideccs/` 前缀**。同一个 `savo-bucket` 里还有 `savo-home/`，
   而 R2 的 CORS 白名单也放行了 `https://www.savo-shen.com`；
   规则若作用于全站，会把那边的 ACAO 强制盖成 `ideccs.savo-shen.com`，反而搞坏它。

验证方法（三项都要过）：

```bash
B=https://cdn.savo-shen.com/ideccs/assets/<任一构建产物>.css

# 1. 全新 URL、不带 Origin，也应该有且只有一个 ACAO
curl -sI "$B?t=$RANDOM" | grep -ci "^access-control-allow-origin"    # 期望 1

# 2. 污染实验：先不带 Origin 打一遍，再带 Origin 取
Q="?t=$RANDOM"; curl -so /dev/null "$B$Q"
curl -sI "$B$Q" -H "Origin: https://ideccs.savo-shen.com" | grep -ci "^access-control-allow-origin"   # 期望 1

# 3. 作用域没溢出：/ideccs/ 之外不应被写入
curl -sI "https://cdn.savo-shen.com/savo-home/" | grep -ci "^access-control-allow-origin"            # 期望 0
```

### 第二道保险（保留）

`deploy/upload-r2.sh` 上传后仍会用带 Origin 的请求预热每个 js/css。
ESA 规则已经根治了问题，预热现在是冗余的保险 —— 但留着无害，
万一以后规则被误删或换了 CDN，它能兜住。

---

## ⚠️ 必做前置：给 R2 桶配 CORS 策略

Vite 生成的是 `<script type="module" crossorigin src="https://cdn...">`。
**ES module 强制以 CORS 模式加载**，R2 不返回 `Access-Control-Allow-Origin` 的话
浏览器会直接拦掉，页面全白。当前实测 CDN **没有**返回这个头，所以这一步必须做。

Cloudflare 控制台 → R2 → 选中桶 → Settings → CORS Policy：

```json
[
  {
    "AllowedOrigins": ["https://ideccs.savo-shen.com"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 86400
  }
]
```

改完后需要**刷新阿里云 ESA 的缓存**，否则边缘还留着没有 CORS 头的旧响应。

验证：

```bash
curl -sI https://cdn.savo-shen.com/ideccs/index.html \
  -H "Origin: https://ideccs.savo-shen.com" | grep -i access-control
# 必须能看到 access-control-allow-origin
```

---

## 服务器现状（2026-08 勘察）

| 项 | 值 |
| :--- | :--- |
| 系统 | Ubuntu 24.04.4 LTS |
| 配置 | 2 核 / 2GB 内存（**可用约 780MB**）/ 50GB 磁盘（已用 51%） |
| 已装 | nginx 1.30、docker、git、curl、Python 3.12 |
| 缺 | uv |
| 8000 端口 | 空闲，可用 |
| 已有服务 | emqx、matrix、element、ntfy、rustdesk、frps、homepage、savo-llm-api 等十余个容器 |
| 证书 | `/etc/letsencrypt/live/savo-shen.com/` → `*.savo-shen.com`，2026-10-11 到期 |
| nginx 约定 | 只 include `conf.d/*.conf`（`sites-enabled/` 空且未被引用），按「域名.conf」命名 |
| 现成 snippet | `snippets/ssl-params.conf`（证书 + TLS + CF 真实 IP）、`snippets/proxy-params.conf` |

内存偏紧，gunicorn 只开 **2 个 worker**，并开启 `--max-requests` 定期回收。

**不需要改任何 DNS**：`ideccs.savo-shen.com` 已经指向这台服务器，
`cdn.savo-shen.com` 已经指向 ESA/R2。

---

# 第一步：部署后端

## 1.1 装 uv

nginx / git / curl 都已经有了：

```bash
ssh savo
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

## 1.2 拉代码

```bash
git clone https://github.com/Savo-Shen/School_Mail.git ~/school_mail
cd ~/school_mail/src/backend
uv sync --no-dev
```

> 部署在 `~/school_mail` 而不是惯例的 `/srv`，是因为这台服务器的 sudo 需要密码，
> 放家目录可以让代码更新、依赖安装、迁移这些日常操作全程不需要 sudo。
> 只有安装 systemd 单元和 nginx 配置这两步需要（一次性）。

## 1.3 写生产配置

```bash
cp .env.example .env
.venv/bin/python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

编辑 `.env`：

```bash
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<上面生成的>
DJANGO_ALLOWED_HOSTS=ideccs.savo-shen.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://ideccs.savo-shen.com
CORS_ALLOWED_ORIGINS=
CACHE_URL=filecache:///var/tmp/school_mail_cache
DRF_NUM_PROXIES=0
```

注意 `CORS_ALLOWED_ORIGINS` **留空**：前端和 API 同域，是同源请求，不走 CORS。

| 配置 | 填错的后果 |
| :--- | :--- |
| `DJANGO_ALLOWED_HOSTS` | 不是当前访问的域名 → 所有请求 400 DisallowedHost |
| `CACHE_URL` | 用默认 locmemcache → 2 个 worker 各算各的，登录限流形同虚设 |
| `DJANGO_SECRET_KEY` | 不填 → 直接启动失败（刻意设计，避免用默认密钥上生产）|

## 1.4 初始化

```bash
mkdir -p /var/tmp/school_mail_cache
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic --noinput
.venv/bin/python manage.py createsuperuser        # 用于 /admin/
.venv/bin/python manage.py check --deploy         # 应当零告警
```

### ⚠️ 首次部署后立即改掉历史账号的密码

`db.sqlite3` 曾经被提交进 git **11 次**，虽然现在已经从索引里移除并加进
`.gitignore`，但**旧版本仍留在 git 历史里**，GitHub 上任何人都能拉到：

```bash
git show <任意旧提交>:src/backend/db.sqlite3
# → savo / savo_shen@qq.com / pbkdf2_sha256$320000$...
```

密码哈希本身是安全的（PBKDF2-SHA256，32 万轮），但**邮箱是明文的**，
拿到哈希后跑字典就能试弱密码。所以生产库一旦建好（无论是新建还是从本地
拷过去的），第一件事就是：

```bash
.venv/bin/python manage.py changepassword savo
```

顺带确认一下没有遗留的测试账号：

```bash
.venv/bin/python manage.py shell -c "
from django.contrib.auth import get_user_model
print(list(get_user_model().objects.values_list('username','email','is_superuser')))
"
```

（`test / 123456@qq.com` 这个 2022 年的测试账号已经在本地库里删掉了。）

彻底从 git 历史抹掉需要 `git filter-repo` 重写历史 + 强推，会让所有协作者的
本地仓库失效，而且 GitHub 上的旧对象可能仍有缓存 —— 对这个项目性价比不高，
改密码就够了。

## 1.5 起服务

```bash
sudo cp /home/savo_shen/school_mail/deploy/school-mail.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now school-mail
curl http://127.0.0.1:8000/api/health/          # 期望 {"status":"ok"}
```

日志：`journalctl -u school-mail -f`

---

# 第二步：换 nginx 配置

原来那份是 certbot 生成的纯静态站点配置，现在要加 SPA 回退和 `/api/` 反代。

```bash
sudo cp /etc/nginx/conf.d/ideccs.savo-shen.com.conf ~/ideccs.conf.bak    # 备份
sudo cp /home/savo_shen/school_mail/deploy/nginx.conf /etc/nginx/conf.d/ideccs.savo-shen.com.conf
sudo nginx -t && sudo systemctl reload nginx
```

验证 API 通了（此时前端还是旧版，不影响）：

```bash
curl https://ideccs.savo-shen.com/api/health/
# 期望 {"status": "ok"}

curl -X POST https://ideccs.savo-shen.com/api/auth/login/ \
  -H 'Content-Type: application/json' -d '{"username":"x","password":"y"}'
# 期望 401 + {"detail":"账号或密码错误"}
```

---

# 第三步：发布前端

## 3.1 构建

```bash
cd src/frontend
pnpm install
pnpm build
```

产物 `src/frontend/ideccs/` 会分成两部分去两个地方。构建时 `base` 取自
`.env.production` 的 `VITE_ASSET_BASE`，已经指向 `https://cdn.savo-shen.com/ideccs/`。

## 3.2 重资源传 R2

```bash
deploy/upload-r2.sh
```

脚本用你本机已配好的 rclone `r2:` remote，并且分类设了缓存头：

- `assets/*` 文件名带内容哈希 → `max-age=31536000, immutable`（一年强缓存）
- `KeepRunning/`、`linzidaren/`、favicon → `max-age=86400`（一天）

桶名默认 `savo-bucket`、前缀默认 `ideccs`，可以用环境变量覆盖：

```bash
R2_BUCKET=savo-bucket R2_PREFIX=ideccs deploy/upload-r2.sh
```

> R2 的作用域 token 没有 ListBuckets 权限，`rclone lsd r2:` 列不出桶，
> 而且对不存在的桶 `rclone lsjson` 会返回空数组（假阳性）。
> 桶名不确定时用 `deploy/find-r2-bucket.sh` 探测，别靠列举。

默认**不删**远端旧文件 —— 刚发版时可能还有用户拿着旧的 index.html，
立刻删旧 assets 会让他们白屏。过几天再跑 `deploy/upload-r2.sh --prune` 清理。

> 如果 rclone 报 `dial tcp 198.18.x.x:443: i/o timeout`，是本机代理
> （Clash 类工具的 fake-IP）把 R2 的 S3 端点劫持了，关掉代理或给
> `*.r2.cloudflarestorage.com` 加直连规则。

## 3.3 index.html 放服务器

```bash
scp src/frontend/ideccs/index.html savo:/tmp/index.html
ssh savo 'sudo install -m 644 /tmp/index.html /var/www/ideccs/index.html'
```

**顺序很重要**：先传 R2 再换 index.html。反过来的话，新 index.html 引用的
assets 还没上传，用户会白屏。

## 3.4 清理旧站点（可选，稳定后再做）

`/var/www/ideccs` 里堆了 318MB 的历史构建产物
（其中 `/var/www/ideccs/ideccs/` 是 159MB 的嵌套重复）。新架构下这个目录
只需要留一个 index.html：

```bash
ssh savo
du -sh /var/www/ideccs                       # 确认现状
sudo cp /var/www/ideccs/index.html /tmp/     # 保住当前的
sudo rm -rf /var/www/ideccs/*
sudo install -m 644 /tmp/index.html /var/www/ideccs/index.html
```

---

# 验证

```bash
# 1. CORS 头（最容易忘的一步）
curl -sI https://cdn.savo-shen.com/ideccs/assets/  \
  -H "Origin: https://ideccs.savo-shen.com" | grep -i access-control

# 2. 后端
curl https://ideccs.savo-shen.com/api/health/

# 3. SPA 回退
curl -so /dev/null -w '%{http_code}\n' https://ideccs.savo-shen.com/login
# 期望 200（不是 404）
```

浏览器打开 https://ideccs.savo-shen.com ，F12 → Network：

- JS/CSS 应该来自 `cdn.savo-shen.com`，且**没有 CORS 报错**；
- `/api/auth/me/` 应该请求到 `ideccs.savo-shen.com/api/...`（同域，没有 OPTIONS 预检）；
- 登录成功后 Application → Local Storage 应有
  `school_mail.access_token` 和 `school_mail.refresh_token`；
- 刷新页面保持登录状态；
- 直接访问 /login 不 404。

---

# 日常发版

**后端**：

```bash
ssh savo && cd /home/savo_shen/school_mail && ./deploy/deploy.sh
```

**前端**：

```bash
cd src/frontend && pnpm build
cd ../.. && deploy/upload-r2.sh
scp src/frontend/ideccs/index.html savo:/tmp/index.html
ssh savo 'sudo install -m 644 /tmp/index.html /var/www/ideccs/index.html'
```

---

# 内存占用

这台机器只有 2GB 内存且已经跑了十余个服务，所以实测了一遍再定参数。

## 后端自身占用（实测）

用生产配置跑 gunicorn，走完整认证链路（登录 → 带 token 访问 → 刷新 token）预热后：

| 配置 | master | worker × 2 | 合计 |
| :--- | ---: | ---: | ---: |
| 默认 | 19.8 MB | 45.8 MB × 2 | **111 MB** |
| 加 `--preload` | 46.0 MB | 20.5 MB × 2 | **87 MB** |

`--preload` 让 master 先加载 Django 再 fork，worker 通过写时复制共享代码页。
省下的 24MB 还是保守估计 —— RSS 会把共享页在每个 worker 里重复计一次，
Linux 上按 PSS 算实际节省更多。

跑完 30 轮完整认证链路后内存**零增长**，没有泄漏迹象。

## 服务器现有负载（实测）

```
              total   used   free  buff/cache  available
Mem:          1935M  1215M   117M       947M       720M
Swap:         1987M  1042M
```

| 类别 | 占用 |
| :--- | :--- |
| 宿主机进程 | mysqld 186M、php-fpm 108M、next-server 85M、YDService 58M |
| Docker 容器（12 个） | 合计约 262M（homepage 86M、emqx 52M、savo-llm-api 37M、postgres 32M…） |

**swap 用了 1GB 但不用担心**：`vmstat` 采样显示 si/so ≈ 0，说明是闲置服务的冷页
被内核换出停放，不是在颠簸；历史 OOM 击杀次数为 **0**。占 swap 大头的是
mysqld（484M）和 EMQX 的 beam.smp（183M），都是长期空闲的进程。

## 结论

**87MB 对 720MB 可用内存，占约 12%，余量充足，可以放心部署。**

几个把风险压到更低的决定：

| 决定 | 省下的内存 |
| :--- | :--- |
| 用 SQLite 而不是另起 Postgres | 一个进程（现有 postgres 容器占 32M） |
| 用 filecache 而不是另起 Redis | 一个进程 |
| `--workers 2` 而不是常规的 `2*CPU+1=5` | 约 60M |
| `--preload` | 约 24M |

systemd 单元里设了 `MemoryHigh=250M` / `MemoryMax=400M`（约 4 倍余量）。
这不是为了省内存，而是**限制故障半径**：万一哪天内存泄漏，systemd 会杀掉并重启
本服务，而不是让内核的 OOM killer 去挑受害者 —— 它很可能挑中占 484MB swap 的
mysqld，那就从「一个接口挂了」升级成「全站事故」。

## 什么时候需要担心

```bash
systemctl status school-mail | grep Memory      # 当前占用
journalctl -u school-mail | grep -i "memory"    # 是否被 MemoryMax 限制过
vmstat 5 3                                       # si/so 持续 >0 才是真的在颠簸
```

如果以后加了图片上传、内容管理这类功能，内存需求会上升，届时再考虑
减到 1 个 worker 或给机器加内存。

---

# 静态资源优化

源图曾是单反原图直出（6000×4000，单张 6~7MB），字体是 33MB 的中文全字库。
已做过一轮压缩，构建产物 **98MB → 21MB**：

| 项目 | 处理方式 | 结果 |
| :--- | :--- | :--- |
| 照片 (JPEG) | 长边限 2560px，q82，渐进式，剥 EXIF | 115MB → 16MB |
| 大图 (PNG) | 长边限 1920px，256 色量化 | 23MB → 605KB（单张） |
| 书法字体 | 子集化到实际用到的 4 个字 + WOFF2 | 33MB → 8KB |
| Unity 游戏 | `.unityweb` 已是 gzip 产物，未动 | 9.3MB |

新增图片后重跑（对已达标的文件自动跳过）：

```bash
# 需要 imagemagick: brew install imagemagick
deploy/optimize-images.sh src/frontend/src/assets src/frontend/public
```

字体子集化（换字体或改了文案后重跑）：

```bash
uvx --from "fonttools[woff]" pyftsubset 原字体.ttf \
  --text="要用到的所有字" --flavor=woff2 --layout-features='*' \
  --no-hinting --output-file=字体.woff2
```

缓存策略在 `deploy/upload-r2.sh` 里按文件类型设置（R2 不支持 `_headers`，
必须在上传时写进对象元数据）。

---

# 常见问题

**Q: 页面全白，控制台报 CORS / 模块加载失败**
R2 桶没配 CORS 策略，或者配了但 ESA 缓存了旧响应。见文首的必做前置。

**Q: 400 DisallowedHost** —— `DJANGO_ALLOWED_HOSTS` 里没有 `ideccs.savo-shen.com`。

**Q: 直接访问 /login 返回 404** —— nginx 配置没换成新的，
`try_files $uri /index.html` 没生效。

**Q: 发新版后用户还是看到旧页面** —— index.html 被缓存了。
新 nginx 配置里对 `/index.html` 设了 `no-cache, must-revalidate`，确认配置已 reload。

**Q: 发新版后白屏，控制台 404 找不到 js** —— 先换了 index.html 但 assets 还没传到 R2。
永远先跑 `upload-r2.sh`，再传 index.html。

**Q: 几个人同时登录就报「操作过于频繁」** —— `CACHE_URL` 还是默认的 locmemcache，
两个 worker 各算各的；或 nginx 没传 `X-Real-IP`。

**Q: rclone 报 198.18.x.x i/o timeout** —— 本机代理的 fake-IP 劫持了
`*.r2.cloudflarestorage.com`，关代理或加直连规则。
