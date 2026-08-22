"""课表日历接口的入参校验。

上传的文件不落库，生成 .ics 的数据也全部由前端回传 —— 所以这里的校验既是
表单校验，也是唯一的一道防线，边界值要卡死（节次、周次、条数、文件大小）。
"""

from __future__ import annotations

from rest_framework import serializers

from .constants import MAX_SECTION, MAX_WEEK

MAX_UPLOAD_BYTES = 2 * 1024 * 1024
ALLOWED_SUFFIXES = (".xlsx", ".xlsm", ".xls")


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        name = (value.name or "").lower()
        if not name.endswith(ALLOWED_SUFFIXES):
            raise serializers.ValidationError("只支持 .xlsx / .xlsm / .xls 文件")
        if value.size > MAX_UPLOAD_BYTES:
            raise serializers.ValidationError(
                f"文件不能超过 {MAX_UPLOAD_BYTES // 1024 // 1024} MB"
            )
        return value


class SectionSerializer(serializers.Serializer):
    """一节课的作息时间。"""

    index = serializers.IntegerField(min_value=1, max_value=MAX_SECTION)
    start = serializers.TimeField(input_formats=["%H:%M", "%H:%M:%S"])
    end = serializers.TimeField(input_formats=["%H:%M", "%H:%M:%S"])

    def validate(self, attrs):
        if attrs["end"] <= attrs["start"]:
            raise serializers.ValidationError(
                f"第 {attrs['index']} 节的结束时间必须晚于开始时间"
            )
        return attrs


class SessionSerializer(serializers.Serializer):
    """一个上课时段。"""

    weekday = serializers.IntegerField(min_value=1, max_value=7)
    start_section = serializers.IntegerField(min_value=1, max_value=MAX_SECTION)
    end_section = serializers.IntegerField(min_value=1, max_value=MAX_SECTION)
    weeks = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=MAX_WEEK),
        min_length=1,
        max_length=MAX_WEEK,
    )
    location = serializers.CharField(
        max_length=200, allow_blank=True, required=False, default=""
    )

    def validate(self, attrs):
        if attrs["end_section"] < attrs["start_section"]:
            raise serializers.ValidationError("结束节次不能早于开始节次")
        attrs["weeks"] = sorted(set(attrs["weeks"]))
        return attrs


class CourseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    teacher = serializers.CharField(max_length=120, allow_blank=True, required=False, default="")
    course_id = serializers.CharField(max_length=60, allow_blank=True, required=False, default="")
    class_name = serializers.CharField(
        max_length=120, allow_blank=True, required=False, default=""
    )
    category = serializers.CharField(max_length=60, allow_blank=True, required=False, default="")
    credit = serializers.CharField(max_length=20, allow_blank=True, required=False, default="")
    sessions = SessionSerializer(many=True, min_length=1, max_length=40)


class IcsRequestSerializer(serializers.Serializer):
    calendar_name = serializers.CharField(max_length=80, required=False, default="课程表")
    first_monday = serializers.DateField()
    sections = SectionSerializer(many=True, min_length=1, max_length=MAX_SECTION)
    # 提前多少分钟提醒；空列表表示不加提醒。1440 = 提前一天
    alarm_minutes = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=7 * 24 * 60),
        required=False,
        default=list,
        max_length=4,
    )
    courses = CourseSerializer(many=True, min_length=1, max_length=200)

    def validate_first_monday(self, value):
        if value.weekday() != 0:
            raise serializers.ValidationError("第一教学周的起始日必须是星期一，请对照校历选择")
        return value

    def validate_sections(self, value):
        seen = {section["index"] for section in value}
        if len(seen) != len(value):
            raise serializers.ValidationError("作息表里有重复的节次")
        return value

    def validate_calendar_name(self, value):
        value = value.strip()
        return value or "课程表"
