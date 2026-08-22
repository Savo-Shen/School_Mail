"""课表日历的测试。

解析是这个功能的核心，用例直接照搬教务系统导出文件里出现过的真实写法
（单双周、一个周次头带多个时段、教室数量和时段对不上等等）。
"""

import datetime
from io import BytesIO

import openpyxl
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .ics import IcsError, build_calendar
from .parsers import ParseError, parse_time_text, parse_weeks, parse_workbook

User = get_user_model()


def make_xlsx(rows) -> BytesIO:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    buffer.name = "课表.xlsx"
    return buffer


UNDERGRAD_HEADER = ["课程名称", "教师姓名", "上课时间", "教学地点"]
GRAD_HEADER = [
    "课程编号", "课程名称", "课程类别", "学分",
    "教学班编号", "教学班名称", "任课教师", "上课时间", "上课教室",
]


class ParseWeeksTests(TestCase):
    def test_range(self):
        self.assertEqual(parse_weeks("1-5周"), [1, 2, 3, 4, 5])

    def test_single(self):
        self.assertEqual(parse_weeks("7周"), [7])

    def test_odd_weeks(self):
        self.assertEqual(parse_weeks("1-15周(单)"), [1, 3, 5, 7, 9, 11, 13, 15])

    def test_even_weeks(self):
        self.assertEqual(parse_weeks("2-8周(双)"), [2, 4, 6, 8])

    def test_mixed_list(self):
        self.assertEqual(parse_weeks("3-5,7-9,12周"), [3, 4, 5, 7, 8, 9, 12])

    def test_out_of_range_is_dropped(self):
        self.assertEqual(parse_weeks("29-40周"), [29, 30])

    def test_garbage(self):
        self.assertEqual(parse_weeks("待定"), [])


class ParseTimeTextTests(TestCase):
    def test_undergraduate(self):
        sessions, warnings = parse_time_text("星期一第1-2节{1-2周};星期二第3-4节{1-10周}")
        self.assertEqual(warnings, [])
        self.assertEqual(len(sessions), 2)
        self.assertEqual(
            (sessions[0].weekday, sessions[0].start_section, sessions[0].end_section),
            (1, 1, 2),
        )
        self.assertEqual(sessions[1].weeks, list(range(1, 11)))

    def test_undergraduate_odd_weeks(self):
        sessions, _ = parse_time_text("星期五第1-2节{1-15周(单)}")
        self.assertEqual(sessions[0].weeks, [1, 3, 5, 7, 9, 11, 13, 15])

    def test_undergraduate_sunday(self):
        sessions, _ = parse_time_text("星期日第9节{3-4周}")
        self.assertEqual(sessions[0].weekday, 7)
        self.assertEqual((sessions[0].start_section, sessions[0].end_section), (9, 9))

    def test_graduate_multiple_slots_share_one_week_header(self):
        sessions, warnings = parse_time_text(
            "2周： 周四 3-4节  ，周五 3-4节  ,3-4,6-9周： 周五 1-2节  "
        )
        self.assertEqual(warnings, [])
        self.assertEqual(len(sessions), 3)
        # 前两个时段共用「2周」这个头
        self.assertEqual(sessions[0].weeks, [2])
        self.assertEqual(sessions[1].weeks, [2])
        self.assertEqual((sessions[1].weekday, sessions[1].start_section), (5, 3))
        self.assertEqual(sessions[2].weeks, [3, 4, 6, 7, 8, 9])

    def test_graduate_sparse_weeks(self):
        sessions, _ = parse_time_text("3,5,7,9,11,13,15,17周： 周三 1-2节  ")
        self.assertEqual(sessions[0].weeks, [3, 5, 7, 9, 11, 13, 15, 17])

    def test_unrecognised(self):
        sessions, warnings = parse_time_text("每周不定时")
        self.assertEqual(sessions, [])
        self.assertEqual(len(warnings), 1)

    def test_blank(self):
        self.assertEqual(parse_time_text(""), ([], []))
        self.assertEqual(parse_time_text("nan"), ([], []))


class ParseWorkbookTests(TestCase):
    def test_undergraduate_list(self):
        stream = make_xlsx([
            UNDERGRAD_HEADER,
            [
                "高等数学\xa0", "王芳",
                "星期一第1-2节{1-16周};星期四第3-4节{1-15周(单)}", "J-506;J-706",
            ],
        ])
        result = parse_workbook(stream, "课表.xlsx")

        self.assertEqual(result.fmt, "undergraduate")
        self.assertEqual(len(result.courses), 1)
        course = result.courses[0]
        self.assertEqual(course.name, "高等数学")   # \xa0 被清掉
        self.assertEqual([s.location for s in course.sessions], ["J-506", "J-706"])

    def test_undergraduate_single_location_applies_to_all_slots(self):
        stream = make_xlsx([
            UNDERGRAD_HEADER,
            ["软件工程", "陈雄峰", "星期一第1-2节{1-3周};星期三第5-6节{1-3周}", "3A603"],
        ])
        result = parse_workbook(stream, "课表.xlsx")
        self.assertEqual([s.location for s in result.courses[0].sessions], ["3A603", "3A603"])

    def test_graduate_list(self):
        stream = make_xlsx([
            GRAD_HEADER,
            [
                "M3501002", "研究生综合英语", "公共必修课", "3.0",
                "2026M3501002194", "2026研究生综合英语194", "谢钦2075",
                "3,5,7周： 周三 1-2节  ,3-5周： 周一 3-4节  ",
                "3A509(院本部),3A509(院本部)",
            ],
        ])
        result = parse_workbook(stream, "课表.xlsx")

        self.assertEqual(result.fmt, "graduate")
        course = result.courses[0]
        self.assertEqual(course.teacher, "谢钦（2075）")   # 工号拆出来
        self.assertEqual(course.credit, "3.0")
        self.assertEqual(len(course.sessions), 2)

    def test_grid(self):
        stream = make_xlsx([
            ["2025-2026年第1学期", "", "", "2024级汉语言文学1班课表"],
            ["节次", "", "星期一", "星期二", "星期三", "星期四", "星期五"],
            [
                "上午", "第一二节", "",
                "马克思主义基本原理/(1-2节)1-16周/ J-506/王芳/2024级汉语言文学1班/56",
                "大学英语/(1-2节)1-12周/ J-305/林巧文/2024级/55\r\n"
                "大学英语/(1-2节)13-16周/ K-805/林巧文/2024级/55",
                "", "",
            ],
        ])
        result = parse_workbook(stream, "课表.xlsx")

        self.assertEqual(result.fmt, "grid")
        self.assertIn("2025-2026年第1学期", result.title)

        by_name = {course.name: course for course in result.courses}
        self.assertEqual(set(by_name), {"马克思主义基本原理", "大学英语"})
        # 同一格里换行分隔的两条是同一门课的两个时段，合并到一门课下
        self.assertEqual(len(by_name["大学英语"].sessions), 2)
        self.assertEqual(by_name["马克思主义基本原理"].sessions[0].weekday, 2)

    def test_grid_section_falls_back_to_row_label(self):
        stream = make_xlsx([
            ["节次", "", "星期一", "星期二", "星期三"],
            ["下午", "第五六节", "体育/1-16周/ 操场/张三", "", ""],
        ])
        result = parse_workbook(stream, "课表.xlsx")
        session = result.courses[0].sessions[0]
        self.assertEqual((session.start_section, session.end_section), (5, 6))

    def test_unknown_format(self):
        stream = make_xlsx([["姓名", "学号"], ["张三", "1001"]])
        with self.assertRaises(ParseError):
            parse_workbook(stream, "名单.xlsx")

    def test_bad_suffix(self):
        with self.assertRaises(ParseError):
            parse_workbook(BytesIO(b"x"), "课表.csv")


class BuildCalendarTests(TestCase):
    sections = {
        1: (datetime.time(8, 30), datetime.time(9, 15)),
        2: (datetime.time(9, 25), datetime.time(10, 10)),
    }
    course = {
        "name": "高等数学",
        "teacher": "王芳",
        "course_id": "MA101",
        "class_name": "",
        "category": "",
        "credit": "",
        "sessions": [
            {
                "weekday": 1,
                "start_section": 1,
                "end_section": 2,
                "weeks": [1, 3],
                "location": "J-506",
            }
        ],
    }

    def build(self, **kwargs):
        params = {
            "calendar_name": "2025-2026_1课程表",
            "first_monday": datetime.date(2025, 9, 1),
            "sections": self.sections,
            "courses": [self.course],
            "alarm_minutes": [10],
        }
        params.update(kwargs)
        return build_calendar(**params)

    def test_dates_and_times(self):
        content, count = self.build()
        text = content.decode()

        self.assertEqual(count, 2)
        # 第 1 周周一 = 2025-09-01，第 3 周周一 = 2025-09-15
        self.assertIn("DTSTART;TZID=Asia/Shanghai:20250901T083000", text)
        self.assertIn("DTEND;TZID=Asia/Shanghai:20250901T101000", text)
        self.assertIn("DTSTART;TZID=Asia/Shanghai:20250915T083000", text)
        self.assertIn("LOCATION:J-506", text)
        self.assertIn("TRIGGER:-PT10M", text)
        self.assertIn("BEGIN:VTIMEZONE", text)

    def test_uid_is_stable_across_runs(self):
        first = {line for line in self.build()[0].decode().splitlines() if line.startswith("UID:")}
        second = {line for line in self.build()[0].decode().splitlines() if line.startswith("UID:")}
        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)

    def test_no_alarm(self):
        content, _ = self.build(alarm_minutes=[])
        self.assertNotIn("BEGIN:VALARM", content.decode())

    def test_missing_section_time(self):
        with self.assertRaises(IcsError):
            self.build(sections={1: self.sections[1]})

    def test_lab_class_is_marked(self):
        course = dict(self.course, class_name="2026数据结构实验班")
        content, _ = self.build(courses=[course])
        self.assertIn("SUMMARY:高等数学（实验）", content.decode())


class TimetableApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="student", email="s@example.com", password="pw-for-test-1"
        )
        self.parse_url = reverse("timetable:parse")
        self.ics_url = reverse("timetable:ics")

    def login(self):
        self.client.force_authenticate(self.user)

    def test_parse_requires_login(self):
        response = self.client.post(self.parse_url, {"file": make_xlsx([UNDERGRAD_HEADER])})
        self.assertEqual(response.status_code, 401)

    def test_ics_requires_login(self):
        response = self.client.post(self.ics_url, {}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_parse_returns_courses(self):
        self.login()
        stream = make_xlsx([
            UNDERGRAD_HEADER,
            ["高等数学", "王芳", "星期一第1-2节{1-16周}", "J-506"],
        ])
        response = self.client.post(self.parse_url, {"file": stream}, format="multipart")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["format"], "undergraduate")
        self.assertEqual(body["stats"]["course_count"], 1)
        self.assertEqual(body["stats"]["max_week"], 16)
        self.assertTrue(body["sections"])
        self.assertEqual(body["courses"][0]["name"], "高等数学")

    def test_parse_rejects_unknown_format(self):
        self.login()
        stream = make_xlsx([["姓名", "学号"], ["张三", "1001"]])
        response = self.client.post(self.parse_url, {"file": stream}, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_parse_rejects_wrong_suffix(self):
        self.login()
        stream = BytesIO(b"not an excel")
        stream.name = "课表.csv"
        response = self.client.post(self.parse_url, {"file": stream}, format="multipart")
        self.assertEqual(response.status_code, 400)

    def ics_payload(self, **kwargs):
        payload = {
            "calendar_name": "2025-2026_1课程表",
            "first_monday": "2025-09-01",
            "sections": [
                {"index": 1, "start": "08:30", "end": "09:15"},
                {"index": 2, "start": "09:25", "end": "10:10"},
            ],
            "alarm_minutes": [10],
            "courses": [
                {
                    "name": "高等数学",
                    "teacher": "王芳",
                    "sessions": [
                        {
                            "weekday": 1,
                            "start_section": 1,
                            "end_section": 2,
                            "weeks": [1, 2],
                            "location": "J-506",
                        }
                    ],
                }
            ],
        }
        payload.update(kwargs)
        return payload

    def test_ics_download(self):
        self.login()
        response = self.client.post(self.ics_url, self.ics_payload(), format="json")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/calendar"))
        self.assertEqual(response["X-Event-Count"], "2")
        self.assertIn("filename*=UTF-8''", response["Content-Disposition"])
        self.assertIn("BEGIN:VEVENT", response.content.decode())

    def test_ics_rejects_non_monday(self):
        self.login()
        response = self.client.post(
            self.ics_url, self.ics_payload(first_monday="2025-09-02"), format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("星期一", response.json()["detail"])

    def test_ics_rejects_empty_courses(self):
        self.login()
        response = self.client.post(self.ics_url, self.ics_payload(courses=[]), format="json")
        self.assertEqual(response.status_code, 400)

    def test_ics_rejects_bad_section_range(self):
        self.login()
        payload = self.ics_payload()
        payload["courses"][0]["sessions"][0]["end_section"] = 99
        response = self.client.post(self.ics_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
