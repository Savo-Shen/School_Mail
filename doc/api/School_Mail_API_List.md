# 校函 API 文档

## 修订历史

| 日期 | 版本 | 说明 | 修订人 |
| :---: | :---: | :---: | :---: |
| 2022.08.05 | 1.0.0 | 初次拟定 | 沈逸帆 |
| 2026.08.22 | 2.0.0 | 改用 JWT 认证，接口路径调整，统一错误格式 | 沈逸帆 |

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
