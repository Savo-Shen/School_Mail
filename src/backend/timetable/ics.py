"""把解析好的课表拼成 iCalendar (.ics)。

转义（课程名里的逗号分号）、75 字节折行、VTIMEZONE 都交给 icalendar 处理，
这里只负责算日期和组织字段。
"""

from __future__ import annotations

import datetime
import hashlib
from zoneinfo import ZoneInfo

from icalendar import Alarm, Calendar, Event, Timezone

from .constants import MAX_EVENTS

TIMEZONE = "Asia/Shanghai"
TZ = ZoneInfo(TIMEZONE)
UID_DOMAIN = "ideccs.savo-shen.com"
PRODID = "-//IDEC CS//School_Mail Timetable//CN"


class IcsError(Exception):
    """数据不足以生成日历时抛出，视图层翻译成 400。"""


def build_calendar(
    *,
    calendar_name: str,
    first_monday: datetime.date,
    sections: dict[int, tuple[datetime.time, datetime.time]],
    courses: list[dict],
    alarm_minutes: list[int],
) -> tuple[bytes, int]:
    """返回 (ics 字节流, 日程数量)。"""
    cal = Calendar()
    cal.add("VERSION", "2.0")
    cal.add("PRODID", PRODID)
    cal.add("CALSCALE", "GREGORIAN")
    cal.add("METHOD", "PUBLISH")
    cal.add("X-WR-CALNAME", calendar_name)
    cal.add("X-WR-TIMEZONE", TIMEZONE)
    cal.add_component(Timezone.from_tzid(TIMEZONE))

    stamp = datetime.datetime.now(datetime.UTC)
    count = 0
    missing: set[int] = set()

    for course in courses:
        for session in course.get("sessions", []):
            start_section = session["start_section"]
            end_section = session["end_section"]

            if start_section not in sections or end_section not in sections:
                missing.update(
                    index for index in (start_section, end_section) if index not in sections
                )
                continue

            begin_time = sections[start_section][0]
            end_time = sections[end_section][1]

            for week in session["weeks"]:
                day = first_monday + datetime.timedelta(
                    days=session["weekday"] - 1 + (week - 1) * 7
                )

                count += 1
                if count > MAX_EVENTS:
                    raise IcsError(f"日程数量超过 {MAX_EVENTS} 条，请减少勾选的课程")

                cal.add_component(
                    _build_event(
                        course=course,
                        session=session,
                        week=week,
                        day=day,
                        begin_time=begin_time,
                        end_time=end_time,
                        stamp=stamp,
                        alarm_minutes=alarm_minutes,
                    )
                )

    if missing:
        raise IcsError(
            "作息表里缺少第 " + "、".join(str(index) for index in sorted(missing)) + " 节的时间"
        )
    if count == 0:
        raise IcsError("没有可生成的日程，请至少勾选一门课")

    return cal.to_ical(), count


def _build_event(
    *,
    course: dict,
    session: dict,
    week: int,
    day: datetime.date,
    begin_time: datetime.time,
    end_time: datetime.time,
    stamp: datetime.datetime,
    alarm_minutes: list[int],
) -> Event:
    event = Event()

    # UID 由「课程 + 日期 + 节次」决定：改完再导一次是覆盖，而不是多出一份重复日程
    event.add("UID", _uid(course, session, day))
    event.add("DTSTAMP", stamp)
    event.add("DTSTART", datetime.datetime.combine(day, begin_time, tzinfo=TZ))
    event.add("DTEND", datetime.datetime.combine(day, end_time, tzinfo=TZ))
    event.add("SEQUENCE", 0)
    event.add("SUMMARY", _summary(course))
    event.add("DESCRIPTION", _description(course, session, week))

    if session.get("location"):
        event.add("LOCATION", session["location"])

    for minutes in alarm_minutes:
        alarm = Alarm()
        alarm.add("ACTION", "DISPLAY")
        alarm.add("DESCRIPTION", _summary(course))
        alarm.add("TRIGGER", datetime.timedelta(minutes=-minutes))
        event.add_component(alarm)

    return event


def _uid(course: dict, session: dict, day: datetime.date) -> str:
    seed = "|".join(
        [
            course.get("course_id") or "",
            course.get("class_name") or "",
            course.get("name") or "",
            course.get("teacher") or "",
            str(session["weekday"]),
            str(session["start_section"]),
            day.isoformat(),
        ]
    )
    return f"{hashlib.sha1(seed.encode()).hexdigest()}@{UID_DOMAIN}"


def _summary(course: dict) -> str:
    name = course.get("name") or "课程"
    # 实验课单独标一下，免得和同名的理论课在日历里分不清
    if "实验" in (course.get("class_name") or "") and "实验" not in name:
        return f"{name}（实验）"
    return name


def _description(course: dict, session: dict, week: int) -> str:
    lines = []
    if course.get("teacher"):
        lines.append(f"任课教师：{course['teacher']}")
    if course.get("course_id"):
        lines.append(f"课程编号：{course['course_id']}")
    if course.get("class_name"):
        lines.append(f"教学班：{course['class_name']}")

    extra = []
    if course.get("category"):
        extra.append(course["category"])
    if course.get("credit"):
        extra.append(f"{course['credit']} 学分")
    if extra:
        lines.append("　".join(extra))

    lines.append(f"第 {week} 周 · 第 {session['start_section']}-{session['end_section']} 节")
    lines.append("由 IDEC 计科官网课表日历生成")
    return "\n".join(lines)
