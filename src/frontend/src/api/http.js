/**
 * axios 实例 + 拦截器。
 *
 * 认证方式是 JWT：
 *   - access token 放在 Authorization 头里，有效期 30 分钟
 *   - 过期后自动用 refresh token 换新的，对调用方完全透明
 *   - refresh 也失效了就清空本地状态并广播 auth:expired 事件
 *
 * 不用 Cookie，所以前端部署在任何域名下都能正常工作。
 */
import axios from 'axios'

const ACCESS_TOKEN_KEY = 'school_mail.access_token'
const REFRESH_TOKEN_KEY = 'school_mail.refresh_token'

/** token 的本地存储。集中在一处，方便以后换成别的存储方式。 */
export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  save({ access, refresh }) {
    if (access) localStorage.setItem(ACCESS_TOKEN_KEY, access)
    if (refresh) localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  },
  clear() {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  },
}

/**
 * 统一的接口错误。
 * message 一定是一句可以直接展示给用户的中文，不会是 undefined。
 */
export class ApiError extends Error {
  constructor(message, { status = 0, code = 'error', errors = {}, retryAfter = null } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.errors = errors
    this.retryAfter = retryAfter
  }

  /** 取某个字段的第一条错误，用于表单下方的红字提示 */
  fieldError(field) {
    const messages = this.errors?.[field]
    return Array.isArray(messages) ? messages[0] : messages || null
  }
}

/** token 失效时广播，由 auth store 监听并重置状态 */
export const AUTH_EXPIRED_EVENT = 'school-mail:auth-expired'

function broadcastAuthExpired() {
  tokenStore.clear()
  window.dispatchEvent(new CustomEvent(AUTH_EXPIRED_EVENT))
}

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// 刷新 token 用的独立实例：不带拦截器，避免刷新失败时递归刷新
const refreshClient = axios.create({
  baseURL: http.defaults.baseURL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// --------------------------------------------------------------------------- //
// 请求拦截器：带上 access token
// --------------------------------------------------------------------------- //

http.interceptors.request.use((config) => {
  const access = tokenStore.getAccess()
  if (access && !config.skipAuth) {
    config.headers.Authorization = `Bearer ${access}`
  }
  return config
})

// --------------------------------------------------------------------------- //
// 响应拦截器：401 时自动刷新 token 并重放请求
// --------------------------------------------------------------------------- //

// 并发请求同时 401 时，只发起一次刷新，其余请求等这一次的结果
let refreshPromise = null

function refreshAccessToken() {
  if (refreshPromise) return refreshPromise

  const refresh = tokenStore.getRefresh()
  if (!refresh) return Promise.reject(new Error('no refresh token'))

  refreshPromise = refreshClient
    .post('/auth/refresh/', { refresh })
    .then(({ data }) => {
      // 后端开启了 refresh token 轮换，每次都会返回新的 refresh
      tokenStore.save({ access: data.access, refresh: data.refresh })
      return data.access
    })
    .finally(() => {
      refreshPromise = null
    })

  return refreshPromise
}

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error

    const canRetry =
      response?.status === 401 &&
      config &&
      !config._retried &&
      !config.skipAuth &&
      tokenStore.getRefresh()

    if (canRetry) {
      config._retried = true
      try {
        const access = await refreshAccessToken()
        config.headers.Authorization = `Bearer ${access}`
        return http(config)
      } catch {
        // refresh 也过期了，只能重新登录
        broadcastAuthExpired()
      }
    }

    throw toApiError(error)
  },
)

/** 把 axios 的各种失败形态统一成 ApiError */
function toApiError(error) {
  if (error.response) {
    const { status, data } = error.response
    const detail =
      (typeof data === 'string' ? null : data?.detail) ||
      (status === 404 ? '接口不存在，请检查 VITE_API_BASE_URL 配置' : null) ||
      (status >= 500 ? '服务器开小差了，请稍后重试' : '请求失败，请稍后重试')

    return new ApiError(detail, {
      status,
      code: data?.code ?? 'error',
      errors: data?.errors ?? {},
      retryAfter: data?.retry_after ?? null,
    })
  }

  if (error.code === 'ECONNABORTED') {
    return new ApiError('请求超时，请检查网络后重试', { code: 'timeout' })
  }

  // 没有 response：网络不通、DNS 失败、被 CORS 拦截等
  return new ApiError('无法连接服务器，请检查网络或稍后重试', { code: 'network' })
}

export default http
