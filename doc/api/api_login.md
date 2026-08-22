# login 接口详情

## 修订历史

| 日期 | 版本 | 说明 | 修订人 |
| :---: | :---: | :---: | :---: |
| 2022.08.05 | 1.0.0 | 初次拟定 | 沈逸帆 |
| 2026.08.22 | 2.0.0 | 改用 JWT，路径改为 /api/auth/login/ | 沈逸帆 |

## 接口描述

用账号密码换取一对 JWT token。登录成功后前端把 token 存到 localStorage，
后续请求通过 `Authorization: Bearer <access>` 头携带。

## 基本信息

| 项 | 值 |
| :--- | :--- |
| 接口地址 | `<server>/api/auth/login/` |
| 请求方式 | POST |
| Content-Type | application/json |
| 是否需要授权 | 否 |
| 限流 | 10 次 / 分钟（按 IP，防暴力破解） |

## 请求参数

| 字段名 | 变量名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :---: | :--- |
| 用户名 | username | string | 是 | 注册时填的用户名 |
| 密码 | password | string | 是 | 明文密码，走 HTTPS 传输 |

> 注意：登录**不需要** email 字段。旧版文档里写了 email 必填，是错的。

## 返回参数

### 成功 `200`

| 字段名 | 变量名 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| 访问令牌 | access | string | 有效期 30 分钟，放进 Authorization 头 |
| 刷新令牌 | refresh | string | 有效期 7 天，用来换新的 access |
| 用户信息 | user | object | 顺带返回，省掉一次 `/api/auth/me/` 请求 |

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "user": {
    "id": 1,
    "username": "savo",
    "email": "savo@example.com",
    "date_joined": "2026-08-22T04:15:21+08:00",
    "is_staff": false
  }
}
```

### 账号或密码错误 `401`

```json
{ "detail": "账号或密码错误", "code": "authentication_failed", "errors": {} }
```

出于安全考虑，不区分「用户名不存在」和「密码错误」—— 否则接口会变成用户名枚举工具。

### 缺少参数 `400`

```json
{
  "detail": "该字段是必填项。",
  "code": "invalid",
  "errors": { "password": ["该字段是必填项。"] }
}
```

### 触发限流 `429`

```json
{ "detail": "操作过于频繁，请 42 秒后再试", "code": "throttled", "errors": {}, "retry_after": 42 }
```

## 调用示例

```bash
curl -X POST https://api.ideccs.com/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"savo","password":"Idec-Ce-2026!"}'
```

前端不需要直接调这个接口，用封装好的 store：

```js
import { useAuthStore } from '@/stores/auth.js'
import { ApiError } from '@/api/http.js'

const auth = useAuthStore()
try {
  await auth.login({ username, password })   // token 会自动存好
} catch (error) {
  message.value = error instanceof ApiError ? error.message : '登录失败，请稍后重试'
}
```
