"""校函项目根路由。

    /admin/   Django 后台
    /api/     业务接口，见 school_mail/urls.py
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("school_mail.urls")),
]

if settings.DEBUG:
    # 开发环境提供 DRF 可浏览 API 的登录入口，方便调试
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]
