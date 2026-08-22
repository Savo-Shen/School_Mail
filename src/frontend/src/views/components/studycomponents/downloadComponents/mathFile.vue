<script setup>
import { ref } from 'vue';

const fileDownload = ref([
    {
        id: 0,
        filename: "文件名称1",
        download: '下载',
        information: '详情'
    },
    {
        id: 1,
        filename: "文件名称2",
        download: '下载',
        information: '详情'
    },
    {
        id: 2,
        filename: "文件名称3",
        download: '下载',
        information: '详情'
    },
    {
        id: 3,
        filename: "文件名称4",
        download: '下载',
        information: '详情'
    },
    {
        id: 4,
        filename: "文件名称5",
        download: '下载',
        information: '详情'
    }
])
</script>

<template>
    <div class="download_file">
        <div class="window">
            <ul>
                <li v-for="item in fileDownload" :key="item.id" class="file">
                    <div class="filename fl">
                        {{ item.filename }}
                    </div>
                    <div class="download_btn fr">
                        <a href="javascript:;">{{ item.download }}</a>
                        <a href="javascript:;">{{ item.information }}</a>
                    </div>
                </li>
            </ul>
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
}
.w {
    width: 1300px;
    margin: 0 auto;
}
.download_file ul li {
    position: relative;
    width: 100%;
    height: 70px;
    border-radius: 15px;
    margin: 20px 0;
    font-size: 24px;
    line-height: 70px;
    background-color: #ccc;
}
.download_file ul li:hover {
    border: 2px solid #ff6700;
}
.filename {
    position: absolute;
    left: 0;
    top: 0;
    padding-left: 15px;
    color: #000;
}
.download_btn a {
    padding: 0 15px;
    color: rgba(42, 130, 228, 98%);
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
</style>