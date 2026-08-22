<script setup>
/**
 * 课表日历生成。
 *
 * 上传教务系统导出的课表 -> 后端解析成结构化课程 -> 页面上校对、在虚拟日历里
 * 确认 -> 生成 .ics 导入手机日历。
 *
 * 两个接口都要求登录（路由 meta.requiresAuth + 后端 IsAuthenticated），
 * 这里再兜一层：token 中途失效时把界面切回登录提示，而不是让用户点了没反应。
 */
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { generateIcs, parseTimetable, saveBlob } from '@/api/timetable.js'
import {
  buildOccurrences,
  formatDate,
  mondayOf,
  parseDate,
} from '@/assets/js/timetable.js'
import { useAuthStore } from '@/stores/auth.js'
import CalendarPreview from '@/views/components/timetable/CalendarPreview.vue'
import CourseBoard from '@/views/components/timetable/CourseBoard.vue'
import Footer from '@/views/components/Footer.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// ---- 上传 ---- //
const fileInput = ref(null)
const fileName = ref('')
const dragging = ref(false)
const parsing = ref(false)
const parseError = ref('')

// ---- 解析结果 ---- //
const result = ref(null)
const courses = ref([])
const sections = ref([])
const defaultSections = ref([])
const warnings = ref([])

// ---- 生成选项 ---- //
const calendarName = ref('')
const firstMondayText = ref(formatDate(mondayOf(new Date())))
const mondaySnapped = ref(false)
const alarmBeforeClass = ref(true)
const alarmBeforeDay = ref(false)

// ---- 生成结果 ---- //
const generating = ref(false)
const generateError = ref('')
const generatedCount = ref(0)

// --------------------------------------------------------------------------- //
// 派生数据
// --------------------------------------------------------------------------- //

const firstMonday = computed(() => parseDate(firstMondayText.value))

const sectionMap = computed(() =>
  Object.fromEntries(sections.value.map((section) => [section.index, section])),
)

/** 只保留勾选中的课和勾选中的时段，后面预览和生成都用它 */
const selectedCourses = computed(() =>
  courses.value
    .filter((course) => course.selected)
    .map((course) => ({
      ...course,
      sessions: course.sessions.filter((session) => session.selected),
    }))
    .filter((course) => course.sessions.length),
)

const occurrences = computed(() =>
  buildOccurrences(selectedCourses.value, sectionMap.value, firstMonday.value),
)

const maxWeek = computed(() => result.value?.stats?.max_week || 1)

const maxUsedSection = computed(() =>
  courses.value.reduce(
    (max, course) =>
      course.sessions.reduce((inner, session) => Math.max(inner, session.end_section), max),
    0,
  ),
)

const selectedSessionCount = computed(() =>
  selectedCourses.value.reduce((total, course) => total + course.sessions.length, 0),
)

const canGenerate = computed(
  () => occurrences.value.length > 0 && !!firstMonday.value && !generating.value,
)

// --------------------------------------------------------------------------- //
// 上传 / 解析
// --------------------------------------------------------------------------- //

function pickFile() {
  fileInput.value?.click()
}

function onFileChange(event) {
  const file = event.target.files?.[0]
  if (file) handleFile(file)
  // 清空，保证选同一个文件也能再次触发 change
  event.target.value = ''
}

function onDrop(event) {
  dragging.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) handleFile(file)
}

async function handleFile(file) {
  fileName.value = file.name
  parseError.value = ''
  generateError.value = ''
  generatedCount.value = 0
  parsing.value = true

  try {
    const data = await parseTimetable(file)
    applyResult(data, file.name)
  } catch (error) {
    reset()
    parseError.value = error.message
  } finally {
    parsing.value = false
  }
}

function applyResult(data, name) {
  result.value = data
  warnings.value = data.warnings || []

  // 默认全选：导出的课表本来就是学生自己的课，逐个勾太累
  courses.value = data.courses.map((course, index) => ({
    ...course,
    colorIndex: index,
    selected: true,
    sessions: course.sessions.map((session) => ({ ...session, selected: true })),
  }))

  defaultSections.value = data.sections.map((section) => ({ ...section }))
  sections.value = data.sections.map((section) => ({ ...section }))
  calendarName.value = defaultCalendarName(data, name)
}

function defaultCalendarName(data, name) {
  const base = name.replace(/\.(xlsx|xlsm|xls)$/i, '').trim()
  const title = (data.title || '').split(/\s+/)[0]
  const candidate = title || base || '课程表'
  const full = /课表|课程表/.test(candidate) ? candidate : `${candidate}课程表`
  return full.slice(0, 80)
}

function reset() {
  result.value = null
  courses.value = []
  sections.value = []
  warnings.value = []
  generatedCount.value = 0
  generateError.value = ''
}

function startOver() {
  reset()
  fileName.value = ''
  parseError.value = ''
}

// --------------------------------------------------------------------------- //
// 校对区的各种编辑
// --------------------------------------------------------------------------- //

function findCourse(courseKey) {
  return courses.value.find((course) => course.key === courseKey)
}

function toggleCourse(courseKey) {
  const course = findCourse(courseKey)
  if (course) course.selected = !course.selected
}

function toggleSession(courseKey, sessionKey) {
  const session = findCourse(courseKey)?.sessions.find((item) => item.key === sessionKey)
  if (session) session.selected = !session.selected
}

function selectAll(value) {
  courses.value.forEach((course) => {
    course.selected = value
  })
}

function updateLocation(courseKey, sessionKey, value) {
  const session = findCourse(courseKey)?.sessions.find((item) => item.key === sessionKey)
  if (session) session.location = value.trim().slice(0, 200)
}

function updateSection(index, field, value) {
  if (!value) return
  const section = sections.value.find((item) => item.index === index)
  if (section) section[field] = value
}

function resetSections() {
  sections.value = defaultSections.value.map((section) => ({ ...section }))
}

/** 学期第一周只能从星期一算起，选到别的日子就往前对齐 */
function onFirstMondayChange(event) {
  const picked = parseDate(event.target.value)
  if (!picked) return
  const monday = mondayOf(picked)
  mondaySnapped.value = formatDate(monday) !== event.target.value
  firstMondayText.value = formatDate(monday)
}

// --------------------------------------------------------------------------- //
// 生成
// --------------------------------------------------------------------------- //

async function generate() {
  if (!canGenerate.value) return

  generating.value = true
  generateError.value = ''
  generatedCount.value = 0

  const alarmMinutes = []
  if (alarmBeforeClass.value) alarmMinutes.push(10)
  if (alarmBeforeDay.value) alarmMinutes.push(24 * 60)

  try {
    const { blob, count } = await generateIcs({
      calendar_name: calendarName.value.trim() || '课程表',
      first_monday: firstMondayText.value,
      sections: sections.value.map(({ index, start, end }) => ({ index, start, end })),
      alarm_minutes: alarmMinutes,
      courses: selectedCourses.value.map((course) => ({
        name: course.name,
        teacher: course.teacher,
        course_id: course.course_id,
        class_name: course.class_name,
        category: course.category,
        credit: course.credit,
        sessions: course.sessions.map((session) => ({
          weekday: session.weekday,
          start_section: session.start_section,
          end_section: session.end_section,
          weeks: session.weeks,
          location: session.location,
        })),
      })),
    })

    saveBlob(blob, `${calendarName.value.trim() || '课程表'}.ics`)
    generatedCount.value = count
  } catch (error) {
    generateError.value = error.message
  } finally {
    generating.value = false
  }
}

function goLogin() {
  router.push({ name: 'Login', query: { redirect: route.fullPath } })
}

function goHome() {
  router.push('/')
}

async function logout() {
  await auth.logout()
  router.push('/')
}
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="brand" @click="goHome">
        <span class="logo" />
        <span class="brand-text">计算机科学与技术</span>
      </div>
      <nav class="topbar-nav">
        <a @click="goHome">返回首页</a>
        <template v-if="auth.isAuthenticated">
          <span class="who">{{ auth.username }}</span>
          <a @click="logout">退出登录</a>
        </template>
        <a v-else @click="goLogin">登录</a>
      </nav>
    </header>

    <section class="hero">
      <h1>课表日历生成</h1>
      <p>把教务系统导出的课表变成手机日历里的日程，上课前自动提醒。</p>
    </section>

    <main class="content">
      <!-- 未登录：路由守卫通常已经拦掉了，这里兜住 token 中途失效的情况 -->
      <div v-if="!auth.isAuthenticated" class="card gate">
        <h2>登录后即可生成</h2>
        <p>课表属于个人信息，需要登录后才能上传和生成日历文件。</p>
        <button class="primary" @click="goLogin">去登录</button>
      </div>

      <template v-else>
        <!-- ① 上传 -->
        <section class="card">
          <h2><i>1</i>上传课表</h2>

          <div
            class="dropzone"
            :class="{ dragging, busy: parsing }"
            @click="pickFile"
            @dragover.prevent="dragging = true"
            @dragleave.prevent="dragging = false"
            @drop.prevent="onDrop"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".xlsx,.xlsm,.xls"
              hidden
              @change="onFileChange"
            />
            <p v-if="parsing" class="drop-main">正在解析 {{ fileName }} …</p>
            <template v-else>
              <p class="drop-main">把课表文件拖到这里，或点击选择</p>
              <p class="drop-sub">支持 .xlsx / .xlsm / .xls，不超过 2MB</p>
            </template>
          </div>

          <p v-if="fileName && !parsing" class="filename">当前文件：{{ fileName }}</p>
          <p v-if="parseError" class="error">{{ parseError }}</p>

          <ul class="formats">
            <li>教务系统「学生个人课表」导出的网格课表</li>
            <li>「选课清单 / 我的课表」导出的一行一门课的清单（本科）</li>
            <li>研究生课表清单（带「上课教室」列的那种）</li>
          </ul>
        </section>

        <template v-if="result">
          <!-- ② 校对 -->
          <section class="card">
            <h2>
              <i>2</i>校对课程
              <span class="badge">{{ result.format_label }}</span>
              <button class="link right" @click="startOver">换一个文件</button>
            </h2>

            <p v-if="result.title" class="subtitle">{{ result.title }}</p>

            <div v-if="warnings.length" class="warn">
              <p>有 {{ warnings.length }} 处没能解析，已跳过：</p>
              <ul>
                <li v-for="(item, index) in warnings" :key="index">{{ item }}</li>
              </ul>
            </div>

            <CourseBoard
              :courses="courses"
              :sections="sections"
              :max-used-section="maxUsedSection"
              @toggle-course="toggleCourse"
              @toggle-session="toggleSession"
              @select-all="selectAll"
              @update-location="updateLocation"
              @update-section="updateSection"
              @reset-sections="resetSections"
            />
          </section>

          <!-- ③ 预览 -->
          <section class="card">
            <h2><i>3</i>虚拟日历预览</h2>

            <div class="options">
              <label>
                <span>第 1 教学周的星期一</span>
                <input type="date" :value="firstMondayText" @change="onFirstMondayChange" />
              </label>
              <label>
                <span>日历名称</span>
                <input v-model="calendarName" type="text" maxlength="80" />
              </label>
            </div>

            <p class="tip">
              日期全部由这一天推算，务必对照校历核对；选到非星期一会自动往前对齐到本周一。
              <span v-if="mondaySnapped" class="snapped">已自动对齐到 {{ firstMondayText }}</span>
            </p>

            <div class="stats">
              <span>已选 <b>{{ selectedCourses.length }}</b> 门课</span>
              <span><b>{{ selectedSessionCount }}</b> 个时段</span>
              <span>共 <b>{{ occurrences.length }}</b> 条日程</span>
              <span>覆盖 <b>{{ maxWeek }}</b> 个教学周</span>
            </div>

            <CalendarPreview
              :occurrences="occurrences"
              :sections="sections"
              :first-monday="firstMonday"
              :max-week="maxWeek"
            />
          </section>

          <!-- ④ 生成 -->
          <section class="card">
            <h2><i>4</i>生成日历文件</h2>

            <div class="alarms">
              <label class="check">
                <input v-model="alarmBeforeClass" type="checkbox" />
                上课前 10 分钟提醒
              </label>
              <label class="check">
                <input v-model="alarmBeforeDay" type="checkbox" />
                提前一天提醒
              </label>
            </div>

            <button class="primary" :disabled="!canGenerate" @click="generate">
              {{ generating ? '生成中…' : `生成 .ics（${occurrences.length} 条日程）` }}
            </button>

            <p v-if="generateError" class="error">{{ generateError }}</p>
            <p v-else-if="generatedCount" class="ok">
              已生成 {{ generatedCount }} 条日程，文件开始下载了。
            </p>

            <div class="howto">
              <h3>怎么导入</h3>
              <ul>
                <li><b>iPhone / iPad</b>：把 .ics 发到微信或邮件里，点开选「添加到日历」。</li>
                <li><b>macOS</b>：双击文件，日历会问你加到哪个日历，建议新建一个「课程表」。</li>
                <li><b>Google 日历</b>：网页版设置 → 导入与导出 → 导入，选这个文件。</li>
                <li>
                  日程的唯一标识由「课程 + 日期 + 节次」算出来，
                  改完课表重新生成再导入是<b>覆盖</b>，不会多出一份重复的。
                </li>
              </ul>
            </div>
          </section>
        </template>
      </template>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: #f2f5f6;
}

/* ---------------- 顶栏 / 标题 ---------------- */

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 40px;
  height: 64px;
  background: rgb(20, 42, 49);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  min-width: 0;
}

.logo {
  width: 96px;
  height: 44px;
  flex: 0 0 auto;
  background-image: url(@img/IDEC_CE_Logo_With_Name.png);
  background-size: contain;
  background-position: left center;
  background-repeat: no-repeat;
}

.brand-text {
  color: #e8eef0;
  font-size: 16px;
  letter-spacing: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.topbar-nav {
  display: flex;
  align-items: center;
  gap: 18px;
  flex: 0 0 auto;
}

.topbar-nav a {
  color: #cfdadd;
  font-size: 14px;
  cursor: pointer;
}

.topbar-nav a:hover {
  color: #fff;
}

.who {
  color: #8fa3aa;
  font-size: 14px;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero {
  padding: 34px 40px 26px;
  background: linear-gradient(180deg, rgb(20, 42, 49) 0%, rgb(31, 62, 71) 100%);
  border-bottom: 3px solid #cbebf4;
}

.hero h1 {
  color: #fff;
  font-size: 30px;
  font-weight: 300;
  letter-spacing: 3px;
}

.hero p {
  margin-top: 8px;
  color: #a9bcc2;
  font-size: 14px;
}

/* ---------------- 内容区 ---------------- */

.content {
  flex: 1 1 auto;
  width: min(1180px, 100%);
  margin: 0 auto;
  padding: 24px 20px 40px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.card {
  background: #fbfcfc;
  border: 1px solid #e3e7ea;
  border-radius: 12px;
  padding: 20px;
}

.card h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 600;
  color: #21323c;
  margin-bottom: 14px;
}

.card h2 i {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgb(20, 42, 49);
  color: #fff;
  font-size: 13px;
  font-style: normal;
}

.badge {
  padding: 2px 9px;
  border-radius: 20px;
  background: #e4eef2;
  color: #3d6270;
  font-size: 12px;
  font-weight: 400;
}

.right {
  margin-left: auto;
}

.link {
  border: none;
  background: none;
  color: #4a90d9;
  font-size: 13px;
  cursor: pointer;
  padding: 0;
}

.subtitle {
  margin: -6px 0 12px;
  font-size: 13px;
  color: #7b8b95;
}

/* ---------------- 上传 ---------------- */

.dropzone {
  border: 2px dashed #cdd7dc;
  border-radius: 10px;
  background: #fff;
  padding: 34px 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background-color 0.2s;
}

.dropzone:hover,
.dropzone.dragging {
  border-color: #4a90d9;
  background: #f4f9fe;
}

.dropzone.busy {
  cursor: progress;
  opacity: 0.7;
}

.drop-main {
  font-size: 15px;
  color: #35505c;
}

.drop-sub {
  margin-top: 6px;
  font-size: 12px;
  color: #93a2ab;
}

.filename {
  margin-top: 10px;
  font-size: 13px;
  color: #4a5b66;
}

.formats {
  margin-top: 14px;
  padding-left: 18px;
  font-size: 12px;
  color: #93a2ab;
  line-height: 1.9;
}

/* ---------------- 提示 ---------------- */

.error {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  background: #fdeceb;
  color: #a8302c;
  font-size: 13px;
}

.ok {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  background: #eaf5e6;
  color: #3d6b2c;
  font-size: 13px;
}

.warn {
  margin-bottom: 14px;
  padding: 10px 14px;
  border-radius: 8px;
  background: #fdf5e2;
  border: 1px solid #f0e0b6;
  color: #7a5b12;
  font-size: 12px;
}

.warn ul {
  margin-top: 4px;
  padding-left: 18px;
  line-height: 1.8;
}

/* ---------------- 选项 ---------------- */

.options {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-bottom: 8px;
}

.options label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 13px;
  color: #4a5b66;
}

.options input {
  border: 1px solid #d6dde2;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 14px;
  color: #21323c;
  background: #fff;
  min-width: 220px;
}

.tip {
  font-size: 12px;
  color: #93a2ab;
  margin-bottom: 12px;
}

.snapped {
  color: #c07b26;
  margin-left: 6px;
}

.stats {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #6c7c86;
}

.stats b {
  color: #21323c;
  font-weight: 600;
}

/* ---------------- 生成 ---------------- */

.alarms {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.check {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #4a5b66;
  cursor: pointer;
}

.primary {
  border: none;
  border-radius: 8px;
  background: rgb(20, 42, 49);
  color: #fff;
  font-size: 15px;
  padding: 10px 26px;
  cursor: pointer;
}

.primary:hover:not(:disabled) {
  background: rgb(31, 62, 71);
}

.primary:disabled {
  background: #b7c2c7;
  cursor: not-allowed;
}

.howto {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #edf0f2;
}

.howto h3 {
  font-size: 14px;
  font-weight: 600;
  color: #35505c;
  margin-bottom: 6px;
}

.howto ul {
  padding-left: 18px;
  font-size: 12px;
  color: #7b8b95;
  line-height: 2;
}

.howto b {
  color: #4a5b66;
  font-weight: 600;
}

/* ---------------- 未登录 ---------------- */

.gate {
  text-align: center;
  padding: 46px 20px;
}

.gate h2 {
  justify-content: center;
  font-size: 20px;
}

.gate p {
  margin-bottom: 18px;
  color: #7b8b95;
  font-size: 14px;
}

/* ---------------- 响应式 ---------------- */

@media (max-width: 700px) {
  .topbar {
    padding: 0 16px;
    height: 56px;
  }

  .brand-text {
    display: none;
  }

  .hero {
    padding: 24px 16px 20px;
  }

  .hero h1 {
    font-size: 22px;
  }

  .content {
    padding: 16px 12px 30px;
    gap: 14px;
  }

  .card {
    padding: 16px 14px;
  }

  .options input {
    min-width: 0;
    width: 100%;
  }

  .options label {
    flex: 1 1 100%;
  }
}
</style>
