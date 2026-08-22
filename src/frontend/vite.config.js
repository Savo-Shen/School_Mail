import { resolve } from 'node:path'

import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 第三个参数传 '' 表示加载所有环境变量（不只是 VITE_ 前缀的）
  const env = loadEnv(mode, __dirname, '')

  return {
    // 静态资源基地址：走 CDN 就填 CDN 地址，否则 '/'。
    // 注意这只影响 js/css/图片的加载地址，不影响接口请求的地址。
    base: env.VITE_ASSET_BASE || '/',

    plugins: [vue()],

    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '@img': resolve(__dirname, 'src/assets/imgs'),
        '@css': resolve(__dirname, 'src/assets/css'),
        '@icons': resolve(__dirname, 'src/assets/icons'),
        '@js': resolve(__dirname, 'src/assets/js'),
        '@video': resolve(__dirname, 'src/assets/video'),
      },
    },

    server: {
      host: true,
      port: 3000,
      open: false,
      proxy: {
        // 开发环境把 /api 转发到本地 Django，浏览器视角下是同源请求，
        // 不需要处理跨域。生产环境不走这里，见 .env.production。
        '/api': {
          target: env.VITE_DEV_API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
    },

    build: {
      outDir: resolve(__dirname, 'ideccs'),
      emptyOutDir: true,
      sourcemap: mode !== 'production',
      // 生产构建默认压缩；之前关掉 minify 会让产物体积大好几倍
    },
  }
})
