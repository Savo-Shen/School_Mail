<script setup>
/**
 * 虚拟日历：把即将写进 .ics 的日程先画出来，导入日历前肉眼校对一遍。
 *
 * 周视图是「节次 × 星期」的网格，和教务系统的课表长得一样；
 * 月视图按自然月排，用来确认单双周、集中周这类跳周的课有没有排错。
 */
import { computed, ref, watch } from 'vue'

import {
  WEEKDAY_LABELS,
  addDays,
  colorOf,
  formatDate,
  formatMonthDay,
  isSameDay,
  layoutOverlaps,
  weekOf,
  weekRange,
} from '@/assets/js/timetable.js'

const props = defineProps({
  occurrences: { type: Array, default: () => [] },
  sections: { type: Array, default: () => [] },
  firstMonday: { type: Date, default: null },
  maxWeek: { type: Number, default: 1 },
})

const view = ref('week')
const currentWeek = ref(1)
const monthCursor = ref(null)

const today = new Date()

// --------------------------------------------------------------------------- //
// 周视图
// --------------------------------------------------------------------------- //

// 只画到实际有课的最后一节，但至少画到第 8 节，免得网格短得不像课表
const visibleSections = computed(() => {
  const used = props.occurrences.reduce((max, item) => Math.max(max, item.endSection), 0)
  const limit = Math.max(used, 8)
  return props.sections.filter((section) => section.index <= limit)
})

const weekOccurrences = computed(() =>
  layoutOverlaps(props.occurrences.filter((item) => item.week === currentWeek.value)),
)

/**
 * 网格课表会把整个班的并列课程排在同一格（体育选项课一格七门），
 * 全导进日历会互相压住。这里把这种格子挑出来提醒用户去上一步取消勾选。
 */
const crowded = computed(() =>
  Object.values(
    weekOccurrences.value.reduce((groups, item) => {
      if (item.span < 3) return groups
      const key = `${item.weekday}-${item.startSection}`
      groups[key] = groups[key] || { weekday: item.weekday, section: item.startSection, count: 0 }
      groups[key].count += 1
      return groups
    }, {}),
  ),
)

const currentWeekRange = computed(() => {
  if (!props.firstMonday) return null
  return weekRange(props.firstMonday, currentWeek.value)
})

/** 周视图表头的日期：周一到周日 */
const weekDays = computed(() => {
  if (!currentWeekRange.value) return []
  return Array.from({ length: 7 }, (unused, index) => {
    const date = addDays(currentWeekRange.value.start, index)
    return { weekday: index + 1, date, isToday: isSameDay(date, today) }
  })
})

function blockStyle(item) {
  const color = colorOf(item.colorIndex)
  return {
    gridColumn: String(item.weekday + 1),
    gridRow: `${item.startSection} / span ${item.endSection - item.startSection + 1}`,
    width: `calc(${100 / item.span}% - 4px)`,
    // translateX 的百分比按元素自身宽度算，所以第 n 列正好平移 n 个身位
    transform: `translateX(calc(${item.slot} * 100%))`,
    backgroundColor: color.bg,
    borderLeftColor: color.border,
    color: color.text,
  }
}

/** 悬浮提示：格子里放不下的信息（完整教师名、地点）在这里给全 */
function tooltip(item) {
  return [
    item.name,
    item.teacher && `任课教师：${item.teacher}`,
    `${item.startTime}-${item.endTime}`,
    item.location || '未标注地点',
  ]
    .filter(Boolean)
    .join('\n')
}

function stepWeek(delta) {
  const next = currentWeek.value + delta
  if (next >= 1 && next <= props.maxWeek) currentWeek.value = next
}

// --------------------------------------------------------------------------- //
// 月视图
// --------------------------------------------------------------------------- //

const byDate = computed(() => {
  const map = new Map()
  props.occurrences.forEach((item) => {
    if (!map.has(item.dateKey)) map.set(item.dateKey, [])
    map.get(item.dateKey).push(item)
  })
  map.forEach((list) => list.sort((a, b) => a.startSection - b.startSection))
  return map
})

/** 月视图从当月 1 号所在周的星期一开始，铺满 6 周 */
const monthCells = computed(() => {
  const cursor = monthCursor.value
  if (!cursor) return []

  const first = new Date(cursor.getFullYear(), cursor.getMonth(), 1)
  const offset = (first.getDay() + 6) % 7
  const start = addDays(first, -offset)

  return Array.from({ length: 42 }, (unused, index) => {
    const date = addDays(start, index)
    const key = formatDate(date)
    return {
      key,
      date,
      day: date.getDate(),
      inMonth: date.getMonth() === cursor.getMonth(),
      isToday: isSameDay(date, today),
      teachingWeek: props.firstMonday ? weekOf(props.firstMonday, date, props.maxWeek) : null,
      items: byDate.value.get(key) || [],
    }
  })
})

const monthLabel = computed(() => {
  const cursor = monthCursor.value
  return cursor ? `${cursor.getFullYear()} 年 ${cursor.getMonth() + 1} 月` : ''
})

function stepMonth(delta) {
  const cursor = monthCursor.value
  if (!cursor) return
  monthCursor.value = new Date(cursor.getFullYear(), cursor.getMonth() + delta, 1)
}

// --------------------------------------------------------------------------- //

// 换了学期起始日或者重新解析了文件，把周次拉回到有效范围，
// 并让月视图跳到开学当月，否则用户会看到一个空日历以为没生成成功
watch(
  () => [props.firstMonday, props.maxWeek],
  () => {
    if (currentWeek.value > props.maxWeek) currentWeek.value = Math.max(props.maxWeek, 1)
    if (props.firstMonday) {
      monthCursor.value = new Date(props.firstMonday.getFullYear(), props.firstMonday.getMonth(), 1)
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="preview">
    <div class="toolbar">
      <div class="tabs">
        <button :class="{ active: view === 'week' }" @click="view = 'week'">周视图</button>
        <button :class="{ active: view === 'month' }" @click="view = 'month'">月视图</button>
      </div>

      <div v-if="view === 'week'" class="stepper">
        <button :disabled="currentWeek <= 1" @click="stepWeek(-1)">‹</button>
        <span class="stepper-label">
          第 {{ currentWeek }} 周
          <em v-if="currentWeekRange">
            {{ formatMonthDay(currentWeekRange.start) }} —
            {{ formatMonthDay(currentWeekRange.end) }}
          </em>
        </span>
        <button :disabled="currentWeek >= maxWeek" @click="stepWeek(1)">›</button>
      </div>

      <div v-else class="stepper">
        <button @click="stepMonth(-1)">‹</button>
        <span class="stepper-label">{{ monthLabel }}</span>
        <button @click="stepMonth(1)">›</button>
      </div>
    </div>

    <!-- 周视图 -->
    <div v-if="view === 'week'" class="scroll">
      <div class="week-head">
        <div class="corner">节次</div>
        <div v-for="day in weekDays" :key="day.weekday" class="day" :class="{ today: day.isToday }">
          <span class="day-name">{{ WEEKDAY_LABELS[day.weekday] }}</span>
          <span class="day-date">{{ day.date.getMonth() + 1 }}/{{ day.date.getDate() }}</span>
        </div>
      </div>

      <div class="week-grid" :style="{ '--rows': visibleSections.length }">
        <!-- 底层：时间列 + 空格子 -->
        <div
          v-for="section in visibleSections"
          :key="'t' + section.index"
          class="time-cell"
          :class="{ divider: section.index === 4 || section.index === 8 }"
          :style="{ gridRow: String(section.index) }"
        >
          <b>{{ section.index }}</b>
          <span>{{ section.start }}</span>
          <span>{{ section.end }}</span>
        </div>

        <template v-for="section in visibleSections" :key="'r' + section.index">
          <div
            v-for="weekday in 7"
            :key="section.index + '-' + weekday"
            class="slot"
            :class="{ divider: section.index === 4 || section.index === 8 }"
            :style="{ gridRow: String(section.index), gridColumn: String(weekday + 1) }"
          ></div>
        </template>

        <!-- 上层：课程块 -->
        <div
          v-for="item in weekOccurrences"
          :key="item.id"
          class="block"
          :class="{ narrow: item.span >= 3 }"
          :style="blockStyle(item)"
          :title="tooltip(item)"
        >
          <strong>{{ item.name }}</strong>
          <span v-if="item.teacher" class="teacher">{{ item.teacher }}</span>
          <span v-if="item.location" class="place">{{ item.location }}</span>
          <span class="time">{{ item.startTime }}-{{ item.endTime }}</span>
        </div>
      </div>

      <p v-if="!weekOccurrences.length" class="empty">这一周没有课</p>
      <p v-for="slot in crowded" :key="slot.weekday + '-' + slot.section" class="crowded">
        {{ WEEKDAY_LABELS[slot.weekday] }}第 {{ slot.section }} 节挤了 {{ slot.count }} 门并列课程
        —— 体育、通识这类选项课导出时会把全班的可选项都列上，
        请回到上一步只勾选你实际上的那一门。
      </p>
    </div>

    <!-- 月视图 -->
    <div v-else class="scroll">
      <div class="month-head">
        <div v-for="weekday in 7" :key="weekday">{{ WEEKDAY_LABELS[weekday] }}</div>
      </div>
      <div class="month-grid">
        <div
          v-for="cell in monthCells"
          :key="cell.key"
          class="month-cell"
          :class="{ muted: !cell.inMonth, today: cell.isToday }"
        >
          <div class="month-cell-head">
            <span class="num">{{ cell.day }}</span>
            <span v-if="cell.teachingWeek && cell.date.getDay() === 1" class="week-tag">
              第{{ cell.teachingWeek }}周
            </span>
          </div>
          <div
            v-for="item in cell.items.slice(0, 3)"
            :key="item.id"
            class="chip"
            :style="{
              backgroundColor: colorOf(item.colorIndex).bg,
              color: colorOf(item.colorIndex).text,
            }"
            :title="tooltip(item)"
          >
            {{ item.name }}
          </div>
          <div v-if="cell.items.length > 3" class="more">+{{ cell.items.length - 3 }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview {
  background: #fff;
  border: 1px solid #e3e7ea;
  border-radius: 10px;
  overflow: hidden;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px 16px;
  border-bottom: 1px solid #edf0f2;
  background: #f7f9fa;
}

.tabs {
  display: flex;
  gap: 6px;
}

.tabs button {
  border: 1px solid #d6dde2;
  background: #fff;
  color: #4a5b66;
  border-radius: 6px;
  padding: 6px 16px;
  font-size: 14px;
  cursor: pointer;
}

.tabs button.active {
  background: rgb(20, 42, 49);
  border-color: rgb(20, 42, 49);
  color: #fff;
}

.stepper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stepper button {
  width: 30px;
  height: 30px;
  border: 1px solid #d6dde2;
  background: #fff;
  border-radius: 6px;
  font-size: 18px;
  line-height: 1;
  color: #4a5b66;
  cursor: pointer;
}

.stepper button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.stepper-label {
  font-size: 14px;
  color: #21323c;
  white-space: nowrap;
}

.stepper-label em {
  font-style: normal;
  color: #7b8b95;
  margin-left: 6px;
}

.scroll {
  overflow-x: auto;
}

/* ---------------- 周视图 ---------------- */

.week-head,
.week-grid {
  display: grid;
  grid-template-columns: 64px repeat(7, minmax(96px, 1fr));
  min-width: 720px;
}

.week-head {
  border-bottom: 1px solid #edf0f2;
}

.corner,
.day {
  padding: 8px 4px;
  text-align: center;
  font-size: 14px;
  color: #4a5b66;
}

.day {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.day-date {
  font-size: 12px;
  color: #93a2ab;
}

.day.today .day-name {
  color: rgb(20, 42, 49);
  font-weight: 600;
}

.day.today .day-date {
  color: #d1704a;
}

.week-grid {
  /* 一格要放课名 + 教师 + 地点 + 时间四行；跨两节的课有两倍高度，
     只占一节的课会裁掉最后一行的时间 —— 左边时间列本来就写着，不影响判读 */
  grid-template-rows: repeat(var(--rows), 60px);
}

.time-cell {
  grid-column: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  font-size: 11px;
  color: #93a2ab;
  border-right: 1px solid #edf0f2;
  border-bottom: 1px solid #f2f5f6;
}

.time-cell b {
  font-size: 13px;
  color: #4a5b66;
  font-weight: 600;
}

.slot {
  border-right: 1px solid #f2f5f6;
  border-bottom: 1px solid #f2f5f6;
}

/* 上午/下午/晚上之间加一条重一点的分隔线 */
.divider {
  border-bottom: 1px solid #dfe5e9;
}

.block {
  /* 和底层格子放在同一批网格坐标上，靠 z-index 浮在上面 */
  z-index: 1;
  margin: 2px;
  padding: 6px 7px;
  border-left: 3px solid;
  border-radius: 5px;
  font-size: 12px;
  line-height: 1.35;
  overflow: hidden;
  cursor: default;
}

.block strong {
  display: block;
  font-weight: 600;
  font-size: 13px;
}

.block .teacher,
.block .place,
.block .time {
  display: block;
  opacity: 0.75;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 教师比地点和时间更常被找，压得轻一点 */
.block .teacher {
  opacity: 0.9;
}

/* 三门以上并排时格子只剩几十像素，只留课程名，别再挤地点和时间 */
.block.narrow {
  padding: 4px 3px;
  border-left-width: 2px;
}

.block.narrow strong {
  font-size: 11px;
  line-height: 1.2;
}

.block.narrow .teacher,
.block.narrow .place,
.block.narrow .time {
  display: none;
}

.crowded {
  padding: 8px 16px;
  font-size: 12px;
  line-height: 1.7;
  color: #7a5b12;
  background: #fdf5e2;
  border-top: 1px solid #f0e0b6;
}

.empty {
  padding: 20px;
  text-align: center;
  color: #93a2ab;
  font-size: 14px;
}

/* ---------------- 月视图 ---------------- */

.month-head,
.month-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(96px, 1fr));
  min-width: 700px;
}

.month-head {
  border-bottom: 1px solid #edf0f2;
}

.month-head div {
  padding: 8px 0;
  text-align: center;
  font-size: 14px;
  color: #4a5b66;
}

.month-cell {
  min-height: 92px;
  padding: 4px 5px 6px;
  border-right: 1px solid #f2f5f6;
  border-bottom: 1px solid #f2f5f6;
}

.month-cell.muted {
  background: #fafbfc;
}

.month-cell.muted .num {
  color: #c3ccd2;
}

.month-cell-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  margin-bottom: 3px;
}

.num {
  font-size: 13px;
  color: #4a5b66;
}

.month-cell.today .num {
  background: rgb(20, 42, 49);
  color: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.week-tag {
  font-size: 10px;
  color: #93a2ab;
}

.chip {
  margin-bottom: 2px;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 11px;
  line-height: 1.5;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more {
  font-size: 10px;
  color: #93a2ab;
  padding-left: 5px;
}

@media (max-width: 560px) {
  .toolbar {
    justify-content: center;
  }
}
</style>
