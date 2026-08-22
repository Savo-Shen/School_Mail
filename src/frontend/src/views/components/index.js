/*

componentsList说明：
homePageComponentsList是用来存放需要展示在home page页面中的所有组件。

*/

// import.meta.globEager('@/views/components/*.vue')

import { ref } from 'vue'

import News from './News.vue'
import FootprintWall from './FootprintWall.vue'
import PhotoWall from './PhotoWall.vue'
import Welcome from './Welcome.vue'
import StudyEntrance from './StudyEntrance.vue'
import SavoGameShortcut from './SavoGameShortcut.vue'

import Introduction from './Introduction.vue'
import ClassView from './ClassView.vue'
import Teachers from './Teachers.vue'

import AboutUs from '@/views/components/AboutUs.vue'
import AboutUs1 from './关于我们.vue'
import AboutUs2 from './高德地图.vue'

import Introduction1 from './专业导读.vue'
import Introduction2 from './专业优势.vue'

import Safety from './瓶瓶安安.vue'

import View from './班级风光.vue'

export const homePageComponentsList = ref([
  {
    id: 0,
    name: "主页",
    components: {
      // News,
      // FootprintWall,
      // StudyEntrance,
      PhotoWall,
      SavoGameShortcut,
      Welcome,
    }
  },
  {
    id: 1,
    name: "专业概况",
    components: {
      Introduction1,
      Introduction2,
    }
  },
  {
    id: 2,
    name: "关于我们",
    components: {
      AboutUs1,
      AboutUs2,
    }
  },
  {
    id: 3,
    name: "班级风光",
    components: {
      View,
    }
  },
  {
    id: 5,
    name: "学生风采",
    components: {
      Safety,
    }
  },
  {
    id: 6,
    name: "社区互动",
    components: {
    }
  },
  {
    id:7,
    name: "共创营地",
    components: {
    }
  }
])