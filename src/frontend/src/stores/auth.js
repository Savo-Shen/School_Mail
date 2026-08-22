/**
 * 登录状态。
 *
 * 之前每个组件各自调一次 is_login 接口，既浪费请求又容易出现
 * 「header 显示已登录、页面显示未登录」的不一致。现在统一收敛到这里，
 * 整个应用只需要在启动时确认一次。
 */
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import * as authApi from '@/api/auth.js'
import { AUTH_EXPIRED_EVENT, tokenStore } from '@/api/http.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const initialized = ref(false)
  const loading = ref(false)

  const isAuthenticated = computed(() => user.value !== null)
  const username = computed(() => user.value?.username ?? '')

  // 保存正在进行中的初始化请求。
  // main.js 和路由守卫会几乎同时调用 initialize()，必须让它们 await 到
  // 同一个 promise —— 否则守卫会在用户信息还没拿到时就放行，导致
  // 「已登录却被当成游客」。
  let initPromise = null

  /** 应用启动时调用；重复调用会复用同一次请求 */
  function initialize() {
    if (initPromise) return initPromise

    initPromise = (async () => {
      if (!tokenStore.getRefresh()) {
        user.value = null
        return
      }
      try {
        user.value = await authApi.fetchCurrentUser()
      } catch {
        // token 失效：静默当作未登录，不打扰用户
        user.value = null
        tokenStore.clear()
      }
    })().finally(() => {
      initialized.value = true
    })

    return initPromise
  }

  async function login(credentials) {
    loading.value = true
    try {
      user.value = await authApi.login(credentials)
      return user.value
    } finally {
      loading.value = false
    }
  }

  async function register(payload) {
    loading.value = true
    try {
      return await authApi.register(payload)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
    }
  }

  async function deleteAccount(payload) {
    await authApi.deleteAccount(payload)
    user.value = null
  }

  // token 彻底失效时（refresh 也过期了）同步重置状态
  window.addEventListener(AUTH_EXPIRED_EVENT, () => {
    user.value = null
  })

  return {
    user,
    loading,
    initialized,
    isAuthenticated,
    username,
    initialize,
    login,
    register,
    logout,
    deleteAccount,
  }
})
