# <div align="center"> 校函 </div>
<div align="center">
  <a href="https://ideccs.savo-shen.com"><img src="https://github.com/Savo-Shen/School_Mail/blob/main/src/frontend/src/assets/icons/IDEC_CE/idec_ce2.png?raw=true" width="70%" alt="School Mail"></a>
</div>

## <div align="center">IDEC计科官网</div>

<div align="center">
  <a href="https://github.com/Savo-Shen/School_Mail/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="2%" alt="space"></a>
</div>

### <div align="center">项目介绍</div>
为部分有想法、有自主学习能力的同学建立的一个团队合作小项目，尽量以规范的项目开发模式，开发一个网站平台。项目的目的是为了让大家在实践中学习，提高自己的技术水平，同时也为班级的宣传提供一个平台。

- 使用vue + Django 前后端分离开发。
- 学习使用git代码管理，完成团队协作。
- 以网站平台为基础，拓展部署其他功能，整合成为一个完整的项目。

### <div align="center">项目运行</div>
本项目现在运行在 [ideccs.savo-shen.com](https://ideccs.savo-shen.com/) 上，前后端均已部署。

### <div align="center">技术栈</div>

| 端 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + Pinia + vue-router，pnpm 管理依赖 |
| 后端 | Django 5.2 LTS + Django REST Framework，JWT 认证，uv 管理依赖 |
| 部署 | 前端 Cloudflare Pages，后端独立域名 |

### <div align="center">本地运行</div>

需要同时把前后端跑起来。

**后端**（需要 Python 3.12+ 和 [uv](https://docs.astral.sh/uv/)）：

```bash
cd src/backend
uv sync
cp .env.example .env          # 开发环境默认配置即可直接用
uv run python manage.py migrate
uv run python manage.py runserver
```

**前端**（需要 Node 20+ 和 pnpm）：

```bash
cd src/frontend
pnpm install
pnpm dev
```

打开 http://localhost:3000 即可。开发环境下 `/api` 请求由 Vite 代理到本地后端，
不涉及跨域。

跑后端测试：

```bash
cd src/backend && uv run python manage.py test
```

### <div align="center">部署</div>

完整步骤见 [部署指南](./doc/deployment.md)，接口文档见 [API 文档](./doc/api/School_Mail_API_List.md)。

线上架构：

| 内容 | 位置 |
|---|---|
| `assets/` 等 20MB 重资源 | Cloudflare R2 + 阿里云 ESA（`cdn.savo-shen.com/ideccs/`） |
| `index.html`（4KB） | 云服务器 nginx（`ideccs.savo-shen.com`） |
| `/api/*` | 同一台服务器的 gunicorn，与前端同域，无需 CORS |

发版：

```bash
cd src/frontend && pnpm build          # 构建
cd ../.. && deploy/upload-r2.sh        # 重资源传 R2
scp src/frontend/ideccs/index.html savo:/tmp/index.html && \
  ssh savo 'sudo install -m 644 /tmp/index.html /var/www/ideccs/index.html'
```

后端：`ssh savo && cd /home/savo_shen/school_mail && ./deploy/deploy.sh`

### <div align="center">项目结构介绍</div>
| 目录            | 说明       |
|---------------|----------   |
| doc           | 文档目录     |
| src/frontend  | 前端源码     |
| src/backend   | 后端源码     |
| log           | 更新日志目录  |

### <div align="center">项目成员及其贡献</div>

#### 前端工程师：
Ethan：设计并Header组件、设计并制作主页、设计登录页面 <br>
Shark：美化组件

#### 后端工程师：


#### 美术工程师：


#### 文案：
Shark: 完成了关于我们、团日活动的文档撰写

#### 其他：

### <div align="center">友情链接</div>
- [IDEC计科官网](https://ideccs.savo-shen.com)
- [Savo的网站](https://shenyifan.home.blog)
