<script setup>
/**
 * 课程校对区：勾掉不上的课、改教室、调作息时间。
 *
 * 教务系统导出的课表里常有并列可选的课（体育选项课一格里排了七个班），
 * 全导进日历会互相压住，所以默认全选、由用户自己去掉多余的那几个。
 */
import { computed, ref } from 'vue'

import { WEEKDAY_LABELS, colorOf } from '@/assets/js/timetable.js'

const props = defineProps({
  courses: { type: Array, default: () => [] },
  sections: { type: Array, default: () => [] },
  maxUsedSection: { type: Number, default: 8 },
})

const emit = defineEmits([
  'toggle-course',
  'toggle-session',
  'select-all',
  'update-location',
  'update-section',
  'reset-sections',
])

const showAllSections = ref(false)

const visibleSections = computed(() =>
  showAllSections.value
    ? props.sections
    : props.sections.filter((section) => section.index <= Math.max(props.maxUsedSection, 8)),
)

const allSelected = computed(() => props.courses.every((course) => course.selected))

function sessionLabel(session) {
  const range =
    session.start_section === session.end_section
      ? `第${session.start_section}节`
      : `第${session.start_section}-${session.end_section}节`
  return `${WEEKDAY_LABELS[session.weekday]} ${range}`
}

function weeksLabel(session) {
  // 优先用原文（「1-15周(单)」比展开成 8 个数字好读），没有就退回周次范围
  if (session.weeks_text) return session.weeks_text
  const weeks = session.weeks
  return weeks.length === 1 ? `第${weeks[0]}周` : `第${weeks[0]}-${weeks[weeks.length - 1]}周`
}
</script>

<template>
  <div class="board">
    <section class="panel">
      <header class="panel-head">
        <h3>课程</h3>
        <label class="check all">
          <input type="checkbox" :checked="allSelected" @change="emit('select-all', !allSelected)" />
          全选
        </label>
      </header>

      <ul class="course-list">
        <li v-for="course in courses" :key="course.key" :class="{ off: !course.selected }">
          <div class="course-head">
            <label class="check">
              <input
                type="checkbox"
                :checked="course.selected"
                @change="emit('toggle-course', course.key)"
              />
              <span class="dot" :style="{ backgroundColor: colorOf(course.colorIndex).border }" />
              <span class="name">{{ course.name }}</span>
            </label>
            <span class="meta">
              <span v-if="course.teacher">{{ course.teacher }}</span>
              <span v-if="course.credit">{{ course.credit }} 学分</span>
              <span v-if="course.category">{{ course.category }}</span>
            </span>
          </div>

          <ul class="session-list">
            <li v-for="session in course.sessions" :key="session.key">
              <label class="check">
                <input
                  type="checkbox"
                  :checked="session.selected"
                  :disabled="!course.selected"
                  @change="emit('toggle-session', course.key, session.key)"
                />
                <span class="when">{{ sessionLabel(session) }}</span>
              </label>
              <span class="weeks">{{ weeksLabel(session) }}</span>
              <span class="count">{{ session.weeks.length }} 次</span>
              <input
                class="location"
                type="text"
                placeholder="上课地点"
                :value="session.location"
                :disabled="!course.selected || !session.selected"
                @change="emit('update-location', course.key, session.key, $event.target.value)"
              />
            </li>
          </ul>
        </li>
      </ul>
    </section>

    <section class="panel">
      <header class="panel-head">
        <h3>作息时间</h3>
        <div class="head-actions">
          <label class="check">
            <input v-model="showAllSections" type="checkbox" />
            显示全部节次
          </label>
          <button type="button" class="link" @click="emit('reset-sections')">恢复默认</button>
        </div>
      </header>

      <p class="hint">各校区、冬夏令时的作息可能不同，导入前请对照一下。</p>

      <table class="sections">
        <thead>
          <tr>
            <th>节次</th>
            <th>开始</th>
            <th>结束</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in visibleSections" :key="section.index">
            <td>第 {{ section.index }} 节</td>
            <td>
              <input
                type="time"
                :value="section.start"
                @change="emit('update-section', section.index, 'start', $event.target.value)"
              />
            </td>
            <td>
              <input
                type="time"
                :value="section.end"
                @change="emit('update-section', section.index, 'end', $event.target.value)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<style scoped>
.board {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}

.panel {
  background: #fff;
  border: 1px solid #e3e7ea;
  border-radius: 10px;
  overflow: hidden;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #edf0f2;
  background: #f7f9fa;
}

.panel-head h3 {
  font-size: 15px;
  font-weight: 600;
  color: #21323c;
}

.head-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.check {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #4a5b66;
  cursor: pointer;
}

.check input {
  cursor: pointer;
}

.link {
  border: none;
  background: none;
  color: #4a90d9;
  font-size: 13px;
  cursor: pointer;
  padding: 0;
}

.course-list {
  list-style: none;
  max-height: 520px;
  overflow-y: auto;
}

.course-list > li {
  padding: 10px 16px;
  border-bottom: 1px solid #f2f5f6;
}

.course-list > li.off {
  opacity: 0.45;
}

.course-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex: 0 0 auto;
}

.name {
  font-size: 14px;
  color: #21323c;
  font-weight: 500;
}

.meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #93a2ab;
}

.session-list {
  list-style: none;
  margin-top: 6px;
  padding-left: 22px;
}

.session-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 3px 0;
  font-size: 12px;
  color: #6c7c86;
}

.when {
  color: #4a5b66;
}

.weeks {
  color: #93a2ab;
}

.count {
  color: #b3bfc6;
}

.location {
  flex: 1 1 120px;
  min-width: 100px;
  border: 1px solid transparent;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 12px;
  color: #4a5b66;
  background: #f5f7f8;
}

.location:hover:not(:disabled) {
  border-color: #d6dde2;
}

.location:focus {
  outline: none;
  border-color: #4a90d9;
  background: #fff;
}

.hint {
  padding: 10px 16px 0;
  font-size: 12px;
  color: #93a2ab;
}

.sections {
  width: 100%;
  border-collapse: collapse;
  /* main.css 里把 table 设成了 display:block + 横向滚动，这里恢复成表格 */
  display: table;
}

.sections th,
.sections td {
  padding: 5px 16px;
  text-align: left;
  font-size: 13px;
  color: #4a5b66;
  border-bottom: 1px solid #f2f5f6;
}

.sections th {
  font-weight: 500;
  color: #93a2ab;
  font-size: 12px;
}

.sections input {
  border: 1px solid #e3e7ea;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 13px;
  color: #21323c;
  background: #fff;
}

@media (max-width: 900px) {
  .board {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
