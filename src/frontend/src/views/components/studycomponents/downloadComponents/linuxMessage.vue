<script setup>
import { ref } from 'vue';
import { linuxDownload } from '.';

const props = defineProps(['downloadId'])
const downloadId = ref(props.downloadId)
</script>

<template>
    <div class="download_information">
        <div class="text fl">
            <p>
                {{ linuxDownload[downloadId].classIntroduction }}
            </p>
        </div>
        <div class="picture fl">
            <img :src= linuxDownload[downloadId].IntroductionImage alt="">
        </div>
    </div>
</template>

<style scoped>
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
    /* *zoom: 1 */
}
.w {
    width: min(1300px, 100%);
    margin: 0 auto;
}
.download_information {
    position: relative;
    /* display: none; */
}
.text {
    width: min(700px, 100%);
    height: 400px;
    margin: 30px 20px;
}
.text p {
    font-size: 18px;
    text-align: justify;
    color: #fff;
}
.picture {
    position: absolute;
    overflow: hidden;
    left: 750px;
    top: 30px;
    width: min(450px, 100%);
    height: 300px;
    border-radius: 15px;
}
.picture img {
    width: min(450px, 100%);
    height: 300px;
}
</style>