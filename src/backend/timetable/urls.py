"""课表日历的路由，挂在 /api/timetable/ 下。"""

from django.urls import path

from . import views

app_name = "timetable"

urlpatterns = [
    path("parse/", views.TimetableParseView.as_view(), name="parse"),
    path("ics/", views.TimetableIcsView.as_view(), name="ics"),
]
