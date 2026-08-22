<script setup>
import { ref } from 'vue'
import { getImgUrl } from '@/assets/js'

import {studyPageComponentsList} from '@/views/components/studycomponents/index.js'
import { useIntersectionObserver } from '@vueuse/core'

import Header_study from '@/views/components/header/Header_study.vue';
import Footer from '@/views/components/Footer.vue';

const isOpen = ref(null)
const isClicked = ref(false)

const Move = ref(null)
const TransitionLogo = ref(null)
const Crouse = ref(null)

const { stop }= useIntersectionObserver(
  
    Move,
    ([{ isIntersecting }], observerElement) => {
        if (isIntersecting) {
            Move.value.classList.add('animate__animated', 'animate__fadeInLeft')
            TransitionLogo.value.classList.add('animate__animated', 'animate__fadeInRight')
            Crouse.value.classList.add('animate__animated', 'animate__fadeInUp')
        }
    },
    {
        threshold: 0,
    },
)

function childShow(id) {
    isOpen.value = id
    isClicked.value = true
}

const class_name = ref([
    {
        id: 0,
        name: "C/C++编程原理",
        img: getImgUrl("学习资源/编程语言.png"),
        text: 'C语言是一门面向过程的计算机编程语言，与C++、C#、Java等面向对象编程语言有所不同。',
    },
    {
        id: 1,
        name: "高等数学",
        img: getImgUrl("学习资源/高等数学.png"),
        text: '高等数学以微积分理论为核心内容，以函数为基本研究对象，以极限作为贯穿微积分理论始终的基本思想。',
    },
    {
        id: 2,
        name: "线性代数",
        img: getImgUrl("学习资源/线性代数.png"),
        text: '线性代数是一门基础数学课程，它的基本概念、理论和方法，具有较强的逻辑性、抽象性和广泛的实用性。',
    },
    {
        id: 3,
        name: "数据结构",
        img: getImgUrl("学习资源/数据结构.png"),
        text: '数据结构是计算机科学教育中的一门必修课程。这门课程主要是介绍数据结构及其相关操作的算法。',
    },
    {
        id: 4,
        name: "数字系统",
        img: getImgUrl("学习资源/数字系统.png"),
        text: '数字系统课程目标是通过理论和实践学习可使学生掌握数字电路的基本概念、数制及编码、逻辑代数及逻辑函数。',
    },
    // {
    //     id: 5,
    //     name: "计算机科学写作",
    //     img: getImgUrl("学习资源/计算机写作.png"),
    //     text: '计算机科学写作是一门应用特殊的文本性代码进行文本的编写，十分锻炼学生的编程思想能力。',
    // },
    {
        id: 6,
        name: "电路与电子",
        img: getImgUrl("学习资源/电路与电子.png"),
        text: '电路与电子技术课程原理性较强，注重实验技能的培养。',
    },
    {
        id: 7,
        name: "离散结构",
        img: getImgUrl("学习资源/离散数学.png"),
        text: '离散数学是培养学生抽象思维和严密概括能力的素质训练课程。',
    },
    {
        id: 8,
        name: "Linux系统与应用",
        img: getImgUrl("学习资源/linux.png"),
        text: '由琳子大人倾力打造的Linux系统与应用课程，让你轻松学会Linux系统的使用。',
    }
])

</script>

<template>
   <div class="all">
        <!-- Header -->
        <Header_study></Header_study>
        <!-- Main -->
        <div class="second-all">
            <Transition name="fade">
                <div class="main" v-if="!isClicked">
                    <!-- Title -->
                    <div class="title">
                       <div class="w">
                            <div class="move" ref="Move">
                                <!-- EnglishTitle -->
                                <h1 class="englishtitle">IDEC</h1> 
                                <!-- TitleFirst -->
                                <h1 class="titlefirst">欢迎开启计算机学习之旅</h1>
                                <!-- TitleSecond -->
                                <h1 class="titlesecond">
                                    为学习提供极为便捷的通道
                                    <span class="fr">v0.0.1</span>
                                </h1>
                            </div>
                            <!-- transitionLogo -->
                            <div class="transitionLogo" ref="TransitionLogo">
                                <div class="container">
                                    <div class="circle"></div>
                                    <div class="circle"></div>
                                    <div class="circle"></div>
                                    <div class="circle"></div>
                                    <div class="circle"></div>
                                    <div class="circle"></div>
                                </div>
                            </div>
                       </div>
                    </div>
                    <!-- Course -->
                    <div class="course" ref="Crouse">
                        <ul>
                            <li v-for="item in class_name" :key="item.id" @click="childShow(item.id)">
                                <a href="javascript:;" class="transitionmodel">
                                    <div class="img_bg">
                                        <img :src="item.img" alt="">
                                    </div>
                                    <h4>
                                        {{item.name}}
                                    </h4>
                                    <div class="introductiontext">
                                        {{ item.text }}
                                    </div>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="second-main" v-else-if="isClicked">
                    <div v-for="studycomponents in studyPageComponentsList" :key="studycomponents.id" >
                        <div v-if="isOpen === studycomponents.id" >
                            <component @Clicked="() => isClicked = false" class="course-detail" :is="studycomponents.components" :courseId=isOpen></component>
                        </div>
                    </div>
                </div>
            </Transition>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped>
.animate__animated .animate__fadeInLeft {
    animation-delay: 1s;
}
.animate__animated .animate__fadeInRight {
    animation-delay: 1s;
}
.animate__animated .animate__fadeInUp {
    animation-delay: 1s;
}
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
.fl {
    float: left;
}
.fr {
    float: right;
}
/* 把我们所有标签的内外边距清零 */
* {
    margin: 0;
    padding: 0;
    /* css3盒子模型 */
    /* css3的盒子模型不需要害怕padding值和边框的设置大小值撑大盒子的大小 */
    box-sizing: border-box;
}
/* em 和 i 斜体的文字不倾斜 */
em,
i {
    font-style: normal
}
/* 去掉li 的小圆点 */
li {
    list-style: none
}

img {
    /* border 0 照顾低版本浏览器 如果 图片外面包含了链接会有边框的问题 */
    border: 0;
    /* 取消图片底侧有空白缝隙的问题 */
    vertical-align: middle
}

button {
    /* 当我们鼠标经过button 按钮的时候，鼠标变成小手 */
    cursor: pointer
}

a {
    color: #666;
    text-decoration: none
}

a:hover {
    color: #c81623
}

button,
input {
    /* "\5B8B\4F53" 就是宋体的意思 这样浏览器兼容性比较好 */
    font-family: Microsoft YaHei, Heiti SC, tahoma, arial, Hiragino Sans GB, "\5B8B\4F53", sans-serif;
    /* 手动去除默认灰色边框 */
    border: 0; 
    outline: none;
}

body {
    /* CSS3 抗锯齿形 让文字显示的更加清晰 */
    -webkit-font-smoothing: antialiased;
    background-color: #fff;
    font: 12px/1.5 Microsoft YaHei, Heiti SC, tahoma, arial, Hiragino Sans GB, "\5B8B\4F53", sans-serif;
    color: #666
}

.hide,
.none {
    display: none
}
/* 清除浮动 */
.clearfix:after {
    visibility: hidden;
    clear: both;
    display: block;
    content: ".";
    height: 0
}

.clearfix {
}
.w {
    width: min(1300px, 100%);
    margin: 0 auto;
}
.all {
    width: 100%;
    height: 100%;
    background-color: #1e1e20;
    display: flex;
    flex-direction: column;
}
.second-all {
    position: relative;
    width: 100%;
    min-height: 960px;
    /* 用 grid 让课程列表和课程详情叠在同一个格子里。
       原来两者都是 position:absolute（为了淡入淡出时不互相顶开），
       但绝对定位不参与父容器高度计算 —— 容器停在写死的 960px，
       而课程列表实际有 1006px，溢出的 46px 直接压到了 footer 上。
       grid 同格叠放既保留交叉淡化，又能让容器按最高的子元素撑开。 */
    display: grid;
    grid-template-columns: 1fr;
    justify-items: center;
    align-items: start;
}
.second-all > * {
    grid-area: 1 / 1;
}
.header {
    height: 50px;
    /* background-color: pink; */
    border-bottom: 1px solid #ccc;
}
.header a img {
    width: 50px;
    height: 50px;
}
.header a h4 {
    text-align: center;
    line-height: 50px;
    font-size: 18px;
}
.nav ul {
    margin-left: 270px;
}
.nav ul li {
    float: left;
    margin-top: 10px;
    /* line-height: 50px; */
    font-size: 18px;
    padding: 0 15px;
}
.nav ul li input {
    padding: 0 10px;
    height: 20px;
    width: 180px;
    border-radius: 10px;
    border: 1px solid #000;
}
.login {
    margin-right: 10px;
}
.login a h4 {
    font-size: 16px;
}
.login a img {
    margin-top: 10px;
    width: 30px;
    height: 30px;
}
.main {
    /* display: none; */
    margin: 50px auto;
    /* 不再需要 absolute —— 由 .second-all 的 grid 同格叠放来处理 */
    position: relative;
}
.second-main {
    position: relative;
}
.title {
    width: 100%;
    /* background-color: pink; */
}
.title .w {
    position: relative;
}
.englishtitle {
    font-size: 56px;
    color: #c99a55;
    font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
}
.titlefirst {
    font-size: 60px;
    margin-top: -20px;
    color: rgba(255, 255, 245, .86);
}
.titlesecond {
    font-size: 24px;
    color: rgba(235, 235, 245, .6);
}
.titlesecond span {
    position: absolute;
    left: 300px;
    bottom: 2px;
    display: block;
    width: 80px;
    height: 30px;
    border-radius: 10px;
    font-size: 20px;
    font-family: "Lucida Calligraphy", cursive, serif, sans-serif;
    text-align: center;
    line-height: 30px;
    color: rgba(255, 255, 245, .86);
    background-color: #c99a55;
}
.transitionLogo {
    position: absolute;
    right: 17px;
    top: 0;
    width: 310px;
    height: 204px;
    /* background-color: #fff; */
}
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 107px;
    top: 110px;
}
.circle {
    position: absolute;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    animation: pulse 3s ease-in-out infinite;
    background-color: aliceblue;
}
.circle:nth-child(1) {
    width: calc(50px * 1);
    height: calc(50px * 1);
    opacity: 1;
    animation-delay: 0.12s;
}
.circle:nth-child(2) {
    width: calc(50px * 2);
    height: calc(50px * 2);
    opacity: 0.5;
    animation-delay: 0.24s;
}
.circle:nth-child(3) {
    width: calc(50px * 3);
    height: calc(50px * 3);
    opacity: 0.33;
    animation-delay: 0.36s;
}
.circle:nth-child(4) {
    width: calc(50px * 4);
    height: calc(50px * 4);
    opacity: 0.25;
    animation-delay: 0.48s;
}
.circle:nth-child(5) {
    width: calc(50px * 5);
    height: calc(50px * 5);
    opacity: 0.2;
    animation-delay: 0.6s;
}
.circle:nth-child(6) {
    width: calc(50px * 6);
    height: calc(50px * 6);
    opacity: 0.16;
    animation-delay: 0.72s;
}
@keyframes pulse {
    0% {
        transform: scale(1);
    }
    25% {
        transform: scale(1.3);
    }
    50% {
        transform: scale(0.7);
    }
    75% {
        transform: scale(1);
    }
}
.course {
    position: relative;
    margin-top: 100px;
    width: 100%;
}
.course ul {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
}
.course ul li {
    margin-top: 0;
    margin-left: 10px;
    margin-right: 30px;
    margin-bottom: 30px;
    transition: all .5s;
}
.course ul li .img_bg {
    position: absolute;
    left: 30px;
    top: 30px;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    background-color: #1e1e20;
}
.course ul li:hover {
    transform: translate(10px, -10px);
}
.course ul li a {
    position: relative;
    display: block;
    width: 360px;
    height: 204px;
    border-radius: 15px;
    background-color: #252529;
}
.course ul li a img {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    width: 35px;
    height: 35px;
}
.course ul li a h4 {
    height: 100%;
    line-height: 204px;
    padding-left: 30px;
    font-size: 16px;
    font-weight: 600;
    color: rgba(255, 255, 245, .86);;
}
.course ul li a .introductiontext {
    position: absolute;
    top: 125px;
    left: 25px;
    font-size: 14px;
    font-weight: 500;
    color: rgba(235, 235, 245, .6);
    height: 65px;
    width: 315px;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>