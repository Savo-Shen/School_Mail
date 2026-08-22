/**
 * 账号相关的接口封装。
 *
 * 这里只负责「发请求 / 返回数据」，失败一律抛 ApiError，
 * 由调用方（通常是 auth store 或页面组件）决定怎么提示用户。
 */
import http, { tokenStore } from './http.js'

/** 注册。成功返回新用户信息。 */
export async function register({ username, password, email }) {
  const { data } = await http.post(
    '/auth/register/',
    { username, password, email },
    { skipAuth: true },
  )
  return data.user
}

/** 登录。成功后 token 已经存好，返回用户信息。 */
export async function login({ username, password }) {
  const { data } = await http.post(
    '/auth/login/',
    { username, password },
    { skipAuth: true },
  )
  tokenStore.save({ access: data.access, refresh: data.refresh })
  return data.user
}

/** 登出。把 refresh token 拉黑，并清空本地 token。 */
export async function logout() {
  const refresh = tokenStore.getRefresh()
  try {
    if (refresh) {
      await http.post('/auth/logout/', { refresh }, { skipAuth: true })
    }
  } finally {
    // 无论后端是否成功，本地都必须登出
    tokenStore.clear()
  }
}

/** 取当前登录用户；未登录会抛 401 的 ApiError。 */
export async function fetchCurrentUser() {
  const { data } = await http.get('/auth/me/')
  return data
}

/** 注销账号，需要重新输入密码确认。 */
export async function deleteAccount({ password }) {
  await http.delete('/auth/me/', { data: { password } })
  tokenStore.clear()
}
