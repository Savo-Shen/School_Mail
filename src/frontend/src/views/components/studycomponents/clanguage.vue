<script setup>
import {ref} from 'vue';
import { studyPageComponentsList } from '.';
import { clanguageDownload } from './downloadComponents/index.js';

const emit = defineEmits('Clicked')
const isShow = ref(0)

const props = defineProps(['courseId'])
const courseId = ref(props.courseId)

const nav_name = ref([
    {
        id: 0,
        name: '课程简介'
    },
    {
        id: 1,
        name: '课程文件'
    }
])

function close() {
    emit('Clicked')
}

function downloadShow(id) {
    isShow.value = id
}

</script>

<template>
    <div class="clanguage">
        <div class="window">
            <!-- header -->
            <div class="clanguage_header">
                <!-- logo -->
                <a href="javascript:;" class="fl title_btn" @click="close">
                    <div class="clogo fl">
                        <img :src=studyPageComponentsList[courseId].backgroundImage alt="">
                    </div>
                    <div class="ctitle fl">
                        <h4>{{ studyPageComponentsList[courseId].name }}</h4>
                        <h5>{{ studyPageComponentsList[courseId].classId }}</h5>
                    </div>
                </a>
                <a href="javascript:;" class="fr">
                    <div class="shutdown" @click="close">
                        <img src="@img/叉叉.png" alt="">
                    </div>
                </a>
            </div>
            <!-- main -->
            <div class="cmain">
                <!-- Teacher -->
                <div class="teacher fl">
                    <div class="information">
                        <img src="@img/个人信息.png" alt="" class="fl">
                        <h3>{{ studyPageComponentsList[courseId].teacher }}</h3>
                    </div>
                </div>
                <!-- Download -->
                <div class="download">
                    <div class="download_nav">
                        <ul>
                            <li v-for="nav in nav_name" :key="nav.id">
                                <a @click="downloadShow(nav.id)" style="cursor: pointer;">{{ nav.name }}</a>
                            </li>
                        </ul>
                    </div>
                    <div v-for="dldcomponents in clanguageDownload" :key="dldcomponents.id">
                        <Transition name="slide-up">
                            <div v-if="isShow === dldcomponents.id">
                                <component :is="dldcomponents.components" :downloadId=isShow></component>
                            </div>
                        </Transition>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s ease-out;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
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
.clanguage,
.math {
    /* display: none; */
    margin: 50px auto;
    width: min(1600px, 100%);
    height: 734px;
    border-radius: 15px;
    background-position: center;
}
.clanguage {
    background-image: url("@img/编程.png");
    background-size: 1600px 743px;
}
.math {
    background-image: url("@img/高等数学背景.jpg");
}
.window {
    width: 100%;
    height: 100%;
    border-radius: 15px;
    /* Chrome 浏览器毛玻璃 */
    backdrop-filter: blur(5px);
    /* Safari 浏览器毛玻璃 */
    -webkit-backdrop-filter: blur(5px);
}
.clanguage_header {
    width: 100%;
    height: 70px;
    border-radius: 15px 15px 0 0;
    border-bottom: 1px solid #a6a6a6;
}
.clogo {
    position: relative;
    width: 60px;
    height: 60px;
    border-radius: 15px;
    margin-left: 15px;
    margin-top: 5px;
    background-color: #fff;
}
.clogo img {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 50px;
    height: 50px;
}
.ctitle {
    margin-left: 10px;
}
.ctitle h4 {
    padding-top: 7px;
    font-size: 20px;
}
.ctitle h5 {
    font-size: 14px;
}
.shutdown {
    width: 40px;
    height: 40px;
    margin: 17px;
}
.shutdown img {
    width: 38px;
    height: 38px;
}
.cmain {
    width: min(1550px, 100%);
    height: 650px;
    margin: 0 auto;
}
.teacher {
    height: 100%;
    width: 300px;
    border-right: 1px solid #a6a6a6;
}
.information {
    margin-top: 20px;
}
.information img {
    width: 60px;
    height: 60px;
}
.information h3 {
    float: left;
    margin-top: 6px;
    margin-left: 50px;
    font-size: 30px;
    color: #fff;
}
.download {
    float: left;
    width: min(1210px, 100%);
    height: 100%;
    margin-left: 20px;
}
.download_nav {
    width: 100%;
    height: 50px;
    border-bottom: 1px solid #a6a6a6;
}
.download_nav ul li {
    float: left;
    line-height: 50px;
    padding: 0 20px;
    font-size: 18px;
}
.download_nav ul li a {
    color: #fff;
}
.download_nav ul li a:hover {
    color: #c81623;
}
</style>