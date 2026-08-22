/**
 * 按相对路径取 imgs/ 下的图片 URL。
 *
 * 之前的写法是：
 *     new URL(`../imgs/${name}`, import.meta.url).href
 *
 * 这在 Vite 里有个坑：变量部分**只能代表一级文件名**。Vite 会把它编译成
 * 一张 `../imgs/*` 的静态映射表（只含 imgs/ 根目录下的文件），
 * 于是 `basketball_game/bg0.jpeg`、`学习资源/编程语言.png` 这类带子目录的
 * 路径查不到 → 返回 undefined → new URL(undefined, base) 得到
 * ".../assets/js/undefined" → 图片全部裂开，而且不报错、静默失败。
 *
 * 这里改成显式用 import.meta.glob + `**`，可以匹配任意层级的子目录。
 * 查不到时打一条 warning，避免再出现「静默裂图」。
 */

const images = import.meta.glob('../imgs/**/*.{png,jpg,jpeg,gif,svg,webp,avif,ico}', {
  eager: true,
  import: 'default',
  query: '?url',
})

// imgUrl: 相对 imgs/ 的路径，例如 'basketball_game/bg0.jpeg'、'学习资源/编程语言.png'
export function getImgUrl(imgUrl) {
  const url = images[`../imgs/${imgUrl}`]
  if (!url) {
    console.warn(`[getImgUrl] 找不到图片: imgs/${imgUrl}`)
    return ''
  }
  return url
}
