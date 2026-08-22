"""课表日历接口。

    POST /api/timetable/parse/   上传 Excel -> 结构化课表（需要登录）
    POST /api/timetable/ics/     结构化课表 -> .ics 文件（需要登录）

两步分开是为了让用户在中间那一步可以改：勾掉不想要的课、调作息时间、
在虚拟日历里确认没排错，确认无误再生成。

上传的文件只在内存里解析，解析完就丢，不落盘也不入库。
"""

import logging
from urllib.parse import quote

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import DEFAULT_SECTIONS
from .ics import IcsError, build_calendar
from .parsers import ParseError, parse_workbook
from .serializers import IcsRequestSerializer, UploadSerializer

logger = logging.getLogger(__name__)


class TimetableParseView(APIView):
    """POST /api/timetable/parse/ —— 解析上传的课表 Excel。"""

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    throttle_scope = "timetable"

    def post(self, request):
        upload = UploadSerializer(data=request.data)
        upload.is_valid(raise_exception=True)
        uploaded = upload.validated_data["file"]

        try:
            result = parse_workbook(uploaded, uploaded.name)
        except ParseError as exc:
            return Response(
                {"detail": str(exc), "code": "unsupported_timetable", "errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            # 解析的是用户上传的任意文件，兜住所有意外，不要把堆栈丢给前端
            logger.exception("课表解析失败: %s", uploaded.name)
            return Response(
                {"detail": "解析失败，请确认上传的是教务系统导出的课表", "code": "parse_failed",
                 "errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        courses = [course.as_dict(index) for index, course in enumerate(result.courses)]
        sessions = [session for course in courses for session in course["sessions"]]

        return Response(
            {
                "format": result.fmt,
                "format_label": result.fmt_label,
                "title": result.title,
                "sections": DEFAULT_SECTIONS,
                "courses": courses,
                # 解析过程中跳过的内容，原样告诉用户，别让它悄悄消失
                "warnings": result.warnings[:20],
                "stats": {
                    "course_count": len(courses),
                    "session_count": len(sessions),
                    "max_week": max(
                        (week for session in sessions for week in session["weeks"]), default=0
                    ),
                    "max_section": max(
                        (session["end_section"] for session in sessions), default=0
                    ),
                },
            }
        )


class TimetableIcsView(APIView):
    """POST /api/timetable/ics/ —— 生成 .ics 文件。"""

    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "timetable"

    def post(self, request):
        serializer = IcsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        sections = {
            section["index"]: (section["start"], section["end"])
            for section in data["sections"]
        }

        try:
            content, count = build_calendar(
                calendar_name=data["calendar_name"],
                first_monday=data["first_monday"],
                sections=sections,
                courses=data["courses"],
                alarm_minutes=data["alarm_minutes"],
            )
        except IcsError as exc:
            return Response(
                {"detail": str(exc), "code": "ics_failed", "errors": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info("用户 %s 生成课表日历，共 %d 条日程", request.user.username, count)

        response = HttpResponse(content, content_type="text/calendar; charset=utf-8")
        response["Content-Disposition"] = _attachment(f"{data['calendar_name']}.ics")
        # 前端读它来提示「共生成 N 条日程」；跨域时要显式放行自定义响应头
        response["X-Event-Count"] = str(count)
        response["Access-Control-Expose-Headers"] = "X-Event-Count, Content-Disposition"
        return response


def _attachment(filename: str) -> str:
    """中文文件名按 RFC 5987 编码，同时给不支持的老浏览器留一个 ASCII 兜底名。"""
    return f"attachment; filename=\"timetable.ics\"; filename*=UTF-8''{quote(filename)}"
