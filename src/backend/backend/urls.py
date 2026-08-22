"""校函项目根路由。

    /admin/            Django 后台
    /api/              账号相关接口，见 school_mail/urls.py
    /api/timetable/    课表日历工具，见 timetable/urls.py
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("school_mail.urls")),
    path("api/timetable/", include("timetable.urls")),
]

if settings.DEBUG:
    # 开发环境提供 DRF 可浏览 API 的登录入口，方便调试
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls")),
    ]
