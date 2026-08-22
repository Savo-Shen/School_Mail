/**
 * 课表日历页面用到的纯计算工具：日期换算、课程配色、周视图排版。
 *
 * 这里的日期一律用「本地时间的零点」表示（new Date(y, m, d)），
 * 不要用 new Date('2025-09-01')——那是 UTC 零点，在东八区会退回到前一天。
 */

export const WEEKDAY_LABELS = ['', '周一', '周二', '周三', '周四', '周五', '周六', '周日']

/** 课程配色。按课程顺序循环取，同一门课在周视图/月视图里颜色一致。 */
export const COURSE_COLORS = [
  { bg: '#e6f0fb', border: '#4a90d9', text: '#14406e' },
  { bg: '#e2f4ef', border: '#2fa38f', text: '#0e4a41' },
  { bg: '#eaf3e0', border: '#6ba63f', text: '#33501c' },
  { bg: '#fdf2da', border: '#d3a33a', text: '#6a4a07' },
  { bg: '#fbeadf', border: '#dd8049', text: '#6d3312' },
  { bg: '#fbe6e6', border: '#d15b57', text: '#6b2220' },
  { bg: '#f3e8f7', border: '#9a63c0', text: '#452363' },
  { bg: '#e6ecfa', border: '#5a6fd0', text: '#22306e' },
  { bg: '#e4f1f6', border: '#3f95b3', text: '#134354' },
  { bg: '#f0eee6', border: '#9c9276', text: '#463f2a' },
]

export function colorOf(index) {
  return COURSE_COLORS[index % COURSE_COLORS.length]
}

// --------------------------------------------------------------------------- //
// 日期
// --------------------------------------------------------------------------- //

/** 'YYYY-MM-DD' -> Date（本地零点）；解析不了返回 null */
export function parseDate(text) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec((text || '').trim())
  if (!match) return null
  const date = new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))
  return Number.isNaN(date.getTime()) ? null : date
}

/** Date -> 'YYYY-MM-DD' */
export function formatDate(date) {
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}-${month}-${day}`
}

export function addDays(date, days) {
  const next = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  next.setDate(next.getDate() + days)
  return next
}

/** 取所在自然周的星期一 */
export function mondayOf(date) {
  // getDay() 周日是 0，换算成「周一=0」的偏移
  const offset = (date.getDay() + 6) % 7
  return addDays(date, -offset)
}

export function formatMonthDay(date) {
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

export function isSameDay(left, right) {
  return (
    left.getFullYear() === right.getFullYear() &&
    left.getMonth() === right.getMonth() &&
    left.getDate() === right.getDate()
  )
}

/** 第 week 教学周的日期区间 */
export function weekRange(firstMonday, week) {
  const start = addDays(firstMonday, (week - 1) * 7)
  return { start, end: addDays(start, 6) }
}

/** 某个日期落在第几教学周；不在学期范围内返回 null */
export function weekOf(firstMonday, date, maxWeek) {
  const days = Math.round((mondayOf(date) - firstMonday) / 86400000)
  const week = Math.floor(days / 7) + 1
  return week >= 1 && week <= maxWeek ? week : null
}

// --------------------------------------------------------------------------- //
// 展开成一条条日程
// --------------------------------------------------------------------------- //

/**
 * 把「课程 + 时段 + 周次」展开成日历上的一条条日程。
 *
 * @param {Array}  courses     已经过滤成「勾选中的课程 + 勾选中的时段」
 * @param {Object} sectionMap  节次 -> { start, end } 字符串时间
 * @param {Date}   firstMonday 第 1 教学周的星期一
 */
export function buildOccurrences(courses, sectionMap, firstMonday) {
  if (!firstMonday) return []

  const occurrences = []

  courses.forEach((course) => {
    course.sessions.forEach((session) => {
      const begin = sectionMap[session.start_section]
      const finish = sectionMap[session.end_section]

      session.weeks.forEach((week) => {
        const date = addDays(firstMonday, session.weekday - 1 + (week - 1) * 7)
        occurrences.push({
          id: `${course.key}-${session.key}-${week}`,
          courseKey: course.key,
          colorIndex: course.colorIndex,
          name: course.name,
          teacher: course.teacher,
          location: session.location,
          weekday: session.weekday,
          week,
          startSection: session.start_section,
          endSection: session.end_section,
          startTime: begin ? begin.start : '',
          endTime: finish ? finish.end : '',
          date,
          dateKey: formatDate(date),
        })
      })
    })
  })

  return occurrences
}

// --------------------------------------------------------------------------- //
// 周视图排版
// --------------------------------------------------------------------------- //

/**
 * 同一天里节次重叠的课（比如体育选项课的几个平行班）要并排显示，
 * 这里给每条日程算出它在重叠簇里的位置：span 是簇里的总列数，slot 是第几列。
 */
export function layoutOverlaps(items) {
  const byWeekday = new Map()
  items.forEach((item) => {
    if (!byWeekday.has(item.weekday)) byWeekday.set(item.weekday, [])
    byWeekday.get(item.weekday).push(item)
  })

  const laid = []

  byWeekday.forEach((dayItems) => {
    dayItems.sort((a, b) => a.startSection - b.startSection || a.endSection - b.endSection)

    let cluster = []
    let clusterEnd = -1

    const flush = () => {
      cluster.forEach((item, index) => {
        laid.push({ ...item, span: cluster.length, slot: index })
      })
      cluster = []
      clusterEnd = -1
    }

    dayItems.forEach((item) => {
      if (cluster.length && item.startSection > clusterEnd) flush()
      cluster.push(item)
      clusterEnd = Math.max(clusterEnd, item.endSection)
    })
    flush()
  })

  return laid
}
