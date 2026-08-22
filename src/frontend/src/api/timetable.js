/**
 * 课表日历工具的接口封装。
 *
 * 两个接口都要求登录：上传的 Excel 在后端内存里解析，不落盘也不入库；
 * .ics 由后端生成，前端只负责把 Blob 存成文件。
 */
import http from './http.js'

// 解析 / 生成都比普通接口慢，单独放宽超时（http 默认 15s）
const SLOW_REQUEST_TIMEOUT = 60000

/**
 * 上传课表 Excel，返回解析出的课程、默认作息和统计信息。
 * @param {File} file
 */
export async function parseTimetable(file) {
  const form = new FormData()
  form.append('file', file)

  const { data } = await http.post('/timetable/parse/', form, {
    // 不手写 Content-Type：交给浏览器补上 multipart 的 boundary
    headers: { 'Content-Type': undefined },
    timeout: SLOW_REQUEST_TIMEOUT,
  })
  return data
}

/**
 * 生成 .ics。
 * @returns {Promise<{blob: Blob, count: number}>} count 是日程条数
 */
export async function generateIcs(payload) {
  const response = await http.post('/timetable/ics/', payload, {
    responseType: 'blob',
    timeout: SLOW_REQUEST_TIMEOUT,
  })

  return {
    blob: response.data,
    count: Number(response.headers['x-event-count']) || 0,
  }
}

/** 把 Blob 存成本地文件 */
export function saveBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  // 立刻 revoke 在部分浏览器上会打断下载，下一轮事件循环再释放
  setTimeout(() => URL.revokeObjectURL(url), 0)
}
