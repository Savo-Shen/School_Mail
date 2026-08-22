import 'animate.css'

import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth.js'

import './assets/main.css'

// 校函 App
const app = createApp(App)

app.use(createPinia())
app.use(router)

// 启动时确认一次登录状态：本地有 token 就换取用户信息。
// 不阻塞挂载，避免首屏白屏；组件里用 isAuthenticated 响应式地渲染即可。
useAuthStore().initialize()

app.mount('#app')
