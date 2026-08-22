<script setup>

</script>

<template>
    <div class="main">
        <div class="Box1" id="box1">
            <strong>
                <p id="Title">团队成员</p>
            </strong>
            <p id="Text">来自21级计算机科学与技术专业的 Savo Shen, Ethan(雷锘)以及 Shark(奇杭)组成的小团队。</p>
            <div id="occupy1"></div>
        </div>
        <div class="Box" id="box2">
            <strong>
                <p id="Title">创立初衷</p>
            </strong>
            <p id="Text">为部分有想法、有自主学习能力的同学建立的一个团队合作小项目，以规范的项目开发模式，让大家一起努力学习，创立了这个网站。</p>
            <div id="occupy2"></div>
        </div>
        <div class="Box" id="box3">
            <strong>
                <p id="Title">创作理念</p>
            </strong>
            <ul id="Text1">
                <li>用最新的网站开发技术,vue + Django 前后端分离开发。</li>
                <li>学习使用git代码管理,完成团队协作。</li>
            </ul>
            <div id="occupy3"></div>
        </div>
        <div class="Box" id="box4">
            <strong>
                <p id="Title">团队目标</p>
            </strong>
            <ul id="Text1">
                <li>为计科专业的同学们打造一个可以交流学习、生活以及各个方面问题的平台。</li>
                <li>完成网站框架制作。</li>
                <li>制作"学习二十大"主题活动页面。</li>
            </ul>
            <div id="occupy4"></div>
        </div>
        <div class="Box2" id="box5">
            <strong>
                <p id="Title">加入我们</p>
            </strong>
            <p id="Text">诚邀各位有热情，对编程有兴趣的小伙伴们加入我们的项目。为我们的网站添砖加瓦，贡献属于自己的力量！</p>
            <div id="occupy5"></div>
        </div>
    </div>
</template>

<style scoped>
.main {
    height: 500px;
    background-color: rgba(20, 42, 49);
    display: flex;
    justify-content: space-around;
}
.main .Box {
    width: 200px;
    height: 300px;
    margin-top: 100px;
    background-color: aliceblue;
    border: 2px solid rgb(138, 202, 218);
    /* box-shadow: 10px black; */
    animation-duration: 2s;
    animation-name: transform;
}
.main .Box1 {
    width: 200px;
    height: 300px;
    margin-top: 100px;
    margin-left: 15px;
    background-color: aliceblue;
    border: 2px solid rgb(138, 202, 218);
    animation-duration: 2s;
    animation-name: transform;
}
.main .Box2 {
    width: 200px;
    height: 300px;
    margin-top: 100px;
    margin-right: 15px;
    background-color: aliceblue;
    border: 2px solid rgb(138, 202, 218);
    /* animation-duration: 2s;
    animation-name: transform; */
}
/* @keyframes transform {
    from {
        margin-left: 100%;
        width: 200px;
    }
    to {
        width: 200px;
    }
} */
#box1 {
    animation-duration: 1s;
    animation-name: transform1;
}
@keyframes transform1 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#box2 {
    animation-duration: 1.5s;
    animation-name: transform2;
}
@keyframes transform2 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#box3 {
    animation-duration: 2s;
    animation-name: transform3;
}
@keyframes transform3 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#box4 {
    animation-duration: 2.5s;
    animation-name: transform4;
}
@keyframes transform4 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#box5 {
    animation-duration: 3s;
    animation-name: transform5;
}
@keyframes transform5 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#box1 {
    animation-duration: 1s;
    animation-name: transform1;
}
@keyframes transform1 {
    from {
        margin-top: 100%;
        height: 300px;
    }
    to {
        height: 300px;
    }
}
#occupy1 {
    width: 193px;
    height: 100px;
    /* background-color: pink; */
}
#occupy2 {
    width: 193px;
    height: 80px;
    /* background-color: pink; */
}
#occupy3 {
    width: 193px;
    height: 110px;
    /* background-color: pink; */
}
#occupy4 {
    width: 193px;
    height: 65px;
}
#occupy5 {
    width: 193px;
    height: 100px;
    /* background-color: pink; */
}
#Title {
    /* color: #fdeac9; */
    color: rgb(138, 202, 218);
    font-size: 20px;
    text-align: center;
    margin-top: 20px;
}
#Text {
    color: rgb(0, 0, 0);
    margin: 10px 15px;
    text-align: justify;
}
#Text1 {
    color: rgb(0, 0, 0);
    margin-top: 10px;
    margin-right: 10px;
    text-align: justify;
}

/* 响应式：.main 是一行 flex，里面 5 个 200px 的盒子（共 1000px），
   窄屏下后面几个会被裁到视口外。改为换行 + 高度自适应
   （原来 height 写死 500px / 300px，换行后内容会溢出）。 */
@media (max-width: 900px) {
    .main {
        flex-wrap: wrap;
        justify-content: center;
        align-content: flex-start;
        height: auto;
        gap: 20px;
        padding: 40px 16px;
    }
    .main .Box,
    .main .Box1,
    .main .Box2 {
        margin: 0;
        height: auto;
        min-height: 240px;
        flex: 0 1 240px;
        padding-bottom: 16px;
    }
}

@media (max-width: 560px) {
    .main .Box,
    .main .Box1,
    .main .Box2 {
        flex: 1 1 100%;
        width: 100%;
    }
}
</style>
