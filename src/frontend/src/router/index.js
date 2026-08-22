import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth.js'

// router 教程: https://router.vuejs.org/zh/guide/#javascript
const routes = [
    {
        path: '/',
        name: 'School_Mail',
        keepAlive: false,
        component: () => import('@/views/School_Mail.vue')
    },
    {
        path: '/login',
        name: 'Login',
        keepAlive: false,
        // 已登录的用户不需要再看登录页
        meta: { guestOnly: true },
        component: () => import('@/views/Login_Register.vue')
    },
    {
        path: '/register',
        name: 'Register',
        keepAlive: false,
        meta: { guestOnly: true },
        component: () => import('@/views/Register.vue'),
    },
    {
        path: '/footprint',
        name: 'Footprint',
        keepAlive: false,
        component: () => import('@/views/FootPrintWall.vue')
    },
    {
        path: '/timetable',
        name: 'Timetable',
        keepAlive: false,
        // 课表是个人信息，未登录直接跳登录页，登录完再跳回来
        meta: { requiresAuth: true },
        component: () => import('@/views/Timetable.vue')
    },
    {
        path: '/printcanvas',
        name: 'PrintCanvas',
        keepAlive: false,
        component: () => import('@/views/PrintCanvas.vue')
    },
    {
        path: '/404',
        name: '404',
        keepAlive: false,
        component: () => import('@/views/NotFound.vue')
    },
    {
        path: '/study',
        name: 'study',
        keepAlive: false,
        component: () => import('@/views/Study.vue')
    },
    {
        path: '/canvas',
        name: 'canvas',
        keepAlive: false,
        component: () => import('@/views/components/canvas.vue')
    },
    {
        path: '/:catchAll(.*)',
        redirect: '/404',
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 全局导航守卫
//   meta.requiresAuth  未登录时跳转到登录页，并记住原本要去的地址
//   meta.guestOnly     已登录时不再展示登录/注册页
router.beforeEach(async (to) => {
    const auth = useAuthStore()

    // 首次进入应用时等待一次登录状态确认，避免守卫读到还没初始化的状态
    await auth.initialize()

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { name: 'Login', query: { redirect: to.fullPath } }
    }

    if (to.meta.guestOnly && auth.isAuthenticated) {
        return { path: '/' }
    }

    return true
})

export default router