"""
校函 (School_Mail) 后端配置。

所有环境相关的配置都通过环境变量注入，本地开发把它们写在 src/backend/.env 里
（参考 .env.example）。生产环境请通过部署平台的环境变量下发，不要写进仓库。
"""

from datetime import timedelta
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGIN_REGEXES=(list, []),
    ACCESS_TOKEN_LIFETIME_MINUTES=(int, 30),
    REFRESH_TOKEN_LIFETIME_DAYS=(int, 7),
    ALLOW_REGISTRATION=(bool, True),
)

# 读取 .env（不存在也不报错，生产环境走真实环境变量）
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DJANGO_DEBUG")

# 开发环境给一个固定的占位密钥，生产环境必须显式提供，否则直接启动失败
# （.env.example 里这一项是空字符串，所以不能只靠 default）
SECRET_KEY = env("DJANGO_SECRET_KEY", default="").strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"
    else:
        raise ImproperlyConfigured(
            "生产环境必须设置 DJANGO_SECRET_KEY 环境变量。生成方式：\n"
            '  python -c "from django.core.management.utils import '
            'get_random_secret_key as k; print(k())"'
        )

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS")


# --------------------------------------------------------------------------- #
# 应用
# --------------------------------------------------------------------------- #

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 第三方
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    # 本项目
    "school_mail.apps.SchoolMailConfig",
    "timetable.apps.TimetableConfig",
]

if DEBUG:
    # 仅开发环境加载，生产环境不需要安装这些包
    INSTALLED_APPS += ["django_extensions"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",          # 必须在 CommonMiddleware 之前
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",     # 生产环境直接托管 admin 静态文件
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------------------------------- #
# 数据库
# --------------------------------------------------------------------------- #
# 默认 SQLite，配置 DATABASE_URL 即可无缝切到 Postgres：
#   DATABASE_URL=postgres://user:pass@host:5432/dbname

DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DATABASE_CONN_MAX_AGE", default=60)


# --------------------------------------------------------------------------- #
# 缓存
# --------------------------------------------------------------------------- #
# 限流的计数存在 cache 里。生产环境 gunicorn 会起多个 worker，如果用默认的
# 本地内存缓存，每个 worker 各算各的，10 次/分钟的登录限流会变成 N 倍失效。
# 单机部署用 filecache 即可（跨进程共享，零额外服务）：
#   CACHE_URL=filecache:///var/tmp/school_mail_cache
# 多机部署再换 rediscache://host:6379/1

CACHES = {"default": env.cache_url("CACHE_URL", default="locmemcache://")}


# --------------------------------------------------------------------------- #
# 认证
# --------------------------------------------------------------------------- #

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Django 默认的 PBKDF2 已经够用；Argon2 需要额外依赖，这里保持默认。
AUTH_USER_MODEL = "auth.User"


# --------------------------------------------------------------------------- #
# DRF + JWT
# --------------------------------------------------------------------------- #
# 前后端分离 + 跨域部署，用 JWT（Authorization 头）而不是 Session Cookie：
# 不受 SameSite / 第三方 Cookie 限制，前端部署在任何域名都能用。

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # 默认需要登录，公开接口在视图里显式声明 AllowAny
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ]
    + (["rest_framework.renderers.BrowsableAPIRenderer"] if DEBUG else []),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "240/min",
        "login": "10/min",       # 防暴力破解
        "register": "5/hour",
        "destructive": "5/hour",
        "timetable": "30/min",   # 解析 Excel / 生成 ics 都比普通接口贵
    },
    # 部署在 Nginx / Cloudflare 后面时，限流要按真实客户端 IP 计算。
    # Nginx 已经用 CF-Connecting-IP 还原了 REMOTE_ADDR，所以这里设 0
    # （表示直接信任 REMOTE_ADDR，不再去解析 X-Forwarded-For）。
    # 如果没有反向代理，保持 0 也是对的。
    "NUM_PROXIES": env.int("DRF_NUM_PROXIES", default=0),
    "EXCEPTION_HANDLER": "school_mail.exceptions.api_exception_handler",
    "UNAUTHENTICATED_USER": "django.contrib.auth.models.AnonymousUser",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env("ACCESS_TOKEN_LIFETIME_MINUTES")),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env("REFRESH_TOKEN_LIFETIME_DAYS")),
    # 每次刷新都换一个新的 refresh token，旧的拉黑 —— 被盗用时可及时失效
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# --------------------------------------------------------------------------- #
# CORS
# --------------------------------------------------------------------------- #

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
CORS_ALLOWED_ORIGIN_REGEXES = env("CORS_ALLOWED_ORIGIN_REGEXES")
# 用 JWT，不依赖 Cookie，所以不需要 credentials
CORS_ALLOW_CREDENTIALS = False

if DEBUG and not CORS_ALLOWED_ORIGINS and not CORS_ALLOWED_ORIGIN_REGEXES:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


# --------------------------------------------------------------------------- #
# 业务开关
# --------------------------------------------------------------------------- #

ALLOW_REGISTRATION = env("ALLOW_REGISTRATION")

# 课表日历上传的 Excel 只在内存里解析，不落盘。上传大小在
# timetable/serializers.py 里卡到 2MB，这里把 Django 的内存阈值提到同一量级，
# 避免它先写一个临时文件出来。
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024


# --------------------------------------------------------------------------- #
# 国际化
# --------------------------------------------------------------------------- #

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------- #
# 静态文件
# --------------------------------------------------------------------------- #

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG
        else "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------------------------------- #
# 生产环境安全加固
# --------------------------------------------------------------------------- #

if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "same-origin"
    # 部署在 Nginx / Cloudflare 之类的反向代理后面时，识别原始协议
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# --------------------------------------------------------------------------- #
# 日志
# --------------------------------------------------------------------------- #

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django.db.backends": {"level": "WARNING", "propagate": False, "handlers": ["console"]},
    },
}
