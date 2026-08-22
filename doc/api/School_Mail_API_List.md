# 校函 API 文档

## 修订历史

| 日期 | 版本 | 说明 | 修订人 |
| :---: | :---: | :---: | :---: |
| 2022.08.05 | 1.0.0 | 初次拟定 | 沈逸帆 |
| 2026.08.22 | 2.0.0 | 改用 JWT 认证，接口路径调整，统一错误格式 | 沈逸帆 |
| 2026.08.22 | 2.1.0 | 新增课表日历接口 | 沈逸帆 |

## 认证方式

**JWT（Bearer Token）**，不使用 Session Cookie。

之所以换掉 Cookie：前端部署在 Cloudflare Pages、后端在独立域名上，属于跨站请求，
浏览器的 SameSite 策略会直接丢弃 Cookie，导致「登录接口返回成功但下一个请求还是未登录」。
JWT 放在 `Authorization` 头里，不受这个限制，前端部署在任何域名下都能正常工作。

调用需要登录的接口时带上：

```
Authorization: Bearer <access_token>
```

| Token | 有效期 | 说明 |
| :--- | :--- | :--- |
| access | 30 分钟 | 每个请求都带上它 |
| refresh | 7 天 | 只用来换新的 access token |

`refresh` 开启了**轮换**：每次刷新都会返回一个新的 refresh token，旧的立即被拉黑。
所以前端拿到刷新响应后必须把两个 token 都更新掉。

## 接口列表

所有接口都以 `/api/` 开头。

| 方法 | 地址 | 说明 | 需要登录 | 限流 |
| :--- | :--- | :--- | :---: | :--- |
| GET | `/api/health/` | 健康检查 | 否 | 无 |
| POST | `/api/auth/register/` | [注册](#注册) | 否 | 5 次/小时 |
| POST | `/api/auth/login/` | [登录](./api_login.md) | 否 | 10 次/分钟 |
| POST | `/api/auth/refresh/` | [刷新 token](#刷新-token) | 否 | 10 次/分钟 |
| POST | `/api/auth/logout/` | [登出](#登出) | 否 | 默认 |
| GET | `/api/auth/me/` | [取当前用户](#取当前用户) | 是 | 默认 |
| DELETE | `/api/auth/me/` | [注销账号](#注销账号) | 是 | 5 次/小时 |
| POST | `/api/timetable/parse/` | [解析课表 Excel](#解析课表-excel) | 是 | 30 次/分钟 |
| POST | `/api/timetable/ics/` | [生成课表日历](#生成课表日历) | 是 | 30 次/分钟 |

> 旧版的 `/api/account_list/`（返回全部用户名和邮箱）已**移除** —— 它无需登录即可调用，
> 属于个人信息泄露。

## 统一错误格式

所有失败响应都是同一个结构，前端可以无脑取 `detail` 展示：

```json
{
  "detail": "用户名已被注册",
  "code": "invalid",
  "errors": {
    "username": ["用户名已被注册"]
  }
}
```

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| detail | string | 一句可直接展示给用户的中文提示，任何情况下都不为空 |
| code | string | 机器可读的错误码 |
| errors | object | 字段级错误，用于表单高亮；非表单类错误为空对象 |
| retry_after | number | 仅限流（429）时出现，单位秒 |

成功与失败通过 **HTTP 状态码**区分，不再使用 `{"status": true/false}`。

| 状态码 | 含义 |
| :--- | :--- |
| 200 / 201 / 204 | 成功 |
| 400 | 参数校验失败，看 `errors` |
| 401 | 未登录或 token 已失效 |
| 403 | 已登录但没有权限 |
| 429 | 触发限流 |

---

## 注册

`POST /api/auth/register/`

### 请求

| 字段 | 类型 | 必填 | 说明 |
| :--- | :--- | :---: | :--- |
| username | string | 是 | 最长 150 字符，不能重复 |
| password | string | 是 | 至少 8 位，不能纯数字、不能是常见弱密码 |
| email | string | 是 | 合法邮箱，不能重复 |

```json
{ "username": "savo", "password": "Idec-Ce-2026!", "email": "savo@example.com" }
```

### 响应 `201`

```json
{
  "detail": "注册成功",
  "user": { "id": 1, "username": "savo", "email": "savo@example.com",
            "date_joined": "2026-08-22T04:15:21+08:00", "is_staff": false }
}
```

注册成功**不会**自动返回 token，前端需要再调一次登录接口（现在的前端已经这么做了，用户无感）。

---

## 刷新 token

`POST /api/auth/refresh/`

```json
{ "refresh": "<refresh_token>" }
```

响应 `200`：

```json
{ "access": "<新的 access token>", "refresh": "<新的 refresh token>" }
```

**两个 token 都要保存**。旧的 refresh token 在这次调用后立即失效，再用会返回 401。

前端的 axios 拦截器已经自动处理了这套逻辑，业务代码不需要关心。

---

## 登出

`POST /api/auth/logout/`

```json
{ "refresh": "<refresh_token>" }
```

响应 `200`：`{"detail": "已登出"}`

把 refresh token 加入黑名单。刻意允许匿名调用 —— access token 已经过期的用户同样需要能登出。
token 本身已失效时也返回成功（结果一致）。

---

## 取当前用户

`GET /api/auth/me/`，需要 `Authorization` 头。

响应 `200`：

```json
{ "id": 1, "username": "savo", "email": "savo@example.com",
  "date_joined": "2026-08-22T04:15:21+08:00", "is_staff": false }
```

未登录返回 `401`。前端也用这个接口在启动时确认登录状态。

---

## 注销账号

`DELETE /api/auth/me/`，需要 `Authorization` 头。

```json
{ "password": "<当前密码>" }
```

响应 `204`，无响应体。密码错误返回 `400`。

只能注销**自己**的账号。旧版的「超级密码」`superCode` 已移除 —— 它硬编码在源码里（`123456`），
任何人拿到都能删掉别人的账号。

---

## 课表日历

把教务系统导出的课表变成 `.ics` 日历文件，分两步：

1. `POST /api/timetable/parse/` 上传 Excel，拿到结构化的课程和时段；
2. 用户在页面上校对（勾掉不上的课、改教室、调作息）后，
   `POST /api/timetable/ics/` 把校对完的数据换成 `.ics`。

分两步是为了让中间那一步可编辑 —— 教务系统的导出并不总是干净的，
比如网格课表会把整个班的体育选项课都列在一格里。

两个接口都**需要登录**：课表属于个人信息，且解析 Excel 比普通接口贵。
上传的文件只在内存里解析，不落盘、不入库，服务端不保存任何课表数据。

### 解析课表 Excel

`POST /api/timetable/parse/`，`multipart/form-data`，需要 `Authorization` 头。

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| file | file | `.xlsx` / `.xlsm` / `.xls`，不超过 2MB |

自动识别三种导出格式：

| format | 说明 | 「上课时间」的写法 |
| :--- | :--- | :--- |
| `undergraduate` | 本科选课清单 | `星期一第1-2节{1-16周};星期四第3-4节{1-15周(单)}` |
| `graduate` | 研究生课表清单 | `3-18周： 周一 5-6节  ,2周： 周四 3-4节` |
| `grid` | 网格课表（行是节次、列是星期） | 单元格里 `课程名/(1-2节)1-16周/ J-506/教师/……` |

响应 `200`：

```json
{
  "format": "undergraduate",
  "format_label": "本科选课清单",
  "title": "2025-2026年第1学期 2024级……1班课表",
  "sections": [{ "index": 1, "start": "08:30", "end": "09:15" }],
  "courses": [
    {
      "key": "c0",
      "name": "高等数学",
      "teacher": "王芳",
      "course_id": "MA101",
      "class_name": "",
      "category": "",
      "credit": "",
      "sessions": [
        {
          "key": "c0s0",
          "weekday": 1,
          "start_section": 1,
          "end_section": 2,
          "weeks": [1, 2, 3],
          "weeks_text": "1-3周",
          "location": "J-506"
        }
      ]
    }
  ],
  "warnings": ["高等数学：无法识别的上课时间：待定"],
  "stats": { "course_count": 11, "session_count": 16, "max_week": 16, "max_section": 10 }
}
```

| 字段 | 说明 |
| :--- | :--- |
| sections | 默认作息，供前端渲染和回传；各校区不同，允许用户改 |
| weekday | 1 = 周一 …… 7 = 周日 |
| weeks | 展开后的周次列表，单双周已经算好 |
| weeks_text | 原始写法（`1-15周(单)`），只用于展示 |
| warnings | 解析时跳过的内容，如实返回，不静默丢弃 |

认不出格式返回 `400`，`code` 为 `unsupported_timetable`。

### 生成课表日历

`POST /api/timetable/ics/`，JSON，需要 `Authorization` 头。

```json
{
  "calendar_name": "2025-2026_1课程表",
  "first_monday": "2025-09-01",
  "sections": [{ "index": 1, "start": "08:30", "end": "09:15" }],
  "alarm_minutes": [10, 1440],
  "courses": [
    {
      "name": "高等数学",
      "teacher": "王芳",
      "sessions": [
        { "weekday": 1, "start_section": 1, "end_section": 2, "weeks": [1, 3], "location": "J-506" }
      ]
    }
  ]
}
```

| 字段 | 必填 | 说明 |
| :--- | :---: | :--- |
| calendar_name | 否 | 日历名（`X-WR-CALNAME`）和下载文件名，默认「课程表」 |
| first_monday | 是 | 第 1 教学周的**星期一**，不是星期一返回 400 |
| sections | 是 | 作息时间，必须覆盖用到的每一节，否则返回 400 |
| alarm_minutes | 否 | 提前多少分钟提醒，最多 4 个；空数组表示不加提醒 |
| courses | 是 | 只传用户勾选的课和时段 |

响应 `200`，`Content-Type: text/calendar; charset=utf-8`，响应体就是 `.ics` 内容：

| 响应头 | 说明 |
| :--- | :--- |
| `Content-Disposition` | 附件，文件名按 RFC 5987 编码 |
| `X-Event-Count` | 生成的日程条数 |

日程的 `UID` 由「课程 + 日期 + 节次」哈希得到，是稳定的 ——
改完课表重新生成再导入是**覆盖**，不会多出一份重复日程。

单次最多 5000 条日程，超出返回 `400`。
