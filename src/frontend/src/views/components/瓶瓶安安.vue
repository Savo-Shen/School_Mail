<script setup>

</script>

<template>
    <div></div>
    <div class="main">
        <div class="Box1">
            <p id="Title">
                <strong>"瓶瓶安安"资源回收项目</strong>
            </p>
            <p id="Title1">
                <strong>项目负责人:</strong>
            </p>
            <p id="Text">21级计算机科学与技术-唐雷锘</p>
            <p id="Title1">
                <strong>项目核心成员:</strong>
            </p>
            <p id="Text">21级计算机科学与技术-沈逸帆</p>
            <p id="Text">21级计算机科学与技术-林炜政</p>
            <p id="Title1">
                <strong>获奖情况:</strong>
            </p>
            <p id="Text">闽江学院校级三等奖</p>
            <div id="Photo"></div>
        </div>
        <div class="Box2">
            <video class="BoxVideeo" controls="controls" width="450px" height="300px">
                <source src="@video/瓶瓶安安资源回收.mp4">
            </video>
        </div>
        <div class="Box3">
            <p id="Title">
                <strong>项目简介</strong>
            </p>
            <p id="Text1">
                该项目主要打造智能资源回收器及辅助回收的智能资源回收平台，目的在于助力国家解决垃圾回收的痛点，缓解垃圾处理后端压力。用户可通过自主进行资源回收获得一定的积分在智能资源回收平台上兑换商品优惠券，以此来激励大众自主进行资源回收。
            </p>
            <div id="occupy"></div>
        </div>
    </div>
</template>

<style scoped>
.main {
    height: 700px;
    /* background-image: linear-gradient(to left bottom, #6bd17b, #60d696, #5bdbae, #5fdec3, #6ce1d5, #6ae5d9, #68e8dc, #65ece0, #51f1d5, #47f5c5, #4df9b0, #5ffb97); */
    /* background-image: linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%); */
    /* background-image: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%); */
    background-color: rgba(20, 42, 49);
    /* background-color: pink; */
    display: flex;
    justify-content: space-between;
}
.main .Box1 {
    width: 300px;
    height: 500px;
    /* background-color: rgb(138, 202, 218); */
    background-color: aliceblue;
    margin-left: 100px;
    border: 2px solid #fdeac9;
    margin-top: 50px;
    animation-duration: 2s;
    animation-name: slidein1;
}
.main .Box2 {
    width: min(450px, 100%);
    height: 300px;
    margin-top: 180px;
    animation-duration: 2s;
    animation-name: slidein;
}
@keyframes slidein {
    from {
        margin-left: 100%;
        width: min(450px, 100%);
    }
    to {
        width: min(450px, 100%);
    }
}
.main .Box3 {
    width: 300px;
    height: 500px;
    /* background-color: rgb(138, 202, 218); */
    background-color: aliceblue;
    margin-top: 150px;
    margin-right: 100px;
    border: 2px solid #fdeac9;
    animation-duration: 2s;
    animation-name: slidein1;
}
@keyframes slidein1 {
    from {
        margin-left: 100%;
        width: 300px;
    }
    to {
        width: 300px;
    }
}
#occupy {
    height: 200px;
    width: 300px;
    /* background-color: #6b8e23; */
}
#Title {
    /* 深藏青色 */
    /* color: #00009c; */
    color: #6b8e23;
    font-size: 20px;
    text-align: center;
    margin-top: 20px;
    font-weight: 900;
}
#Title1 {
    color: #6b8e23;
    font-size: 18px;
    font-weight: 900;
    margin-left: 15px;
    margin-top: 10px;
}
#Text {
    color: #6b8e23;
    font-size: 18px;
    margin-left: 27px;
    line-height: 1.5em;
}
#Text1 {
    color: #6b8e23;
    font-size: 18px;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 20px;
    line-height: 1.5em;
    text-align: justify;
}
#Photo {
    width: 290px;
    height: 193px;
    background-image: url('@img/学生风采/瓶瓶安安获奖证书.jpg');
    background-size: 290px 193px;
    margin-top: 17px;
    margin-left: 3px;
    background-repeat: no-repeat;
    background-position: center;

    border-style: solid;
    display: block;
    -webkit-transition: width 2s, height 2s, -webkit-transform 2s;
    transition: width 2s, height 2s, transform 2s;
}
#Photo:hover {
    width: 390px;
    height: 293px;
    background-size: 390px 293px;
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
}

/* 响应式：.main 是「简介 300px + 视频 450px + 项目信息 300px」三栏，
   加上左右各 100px 边距共约 1250px，窄屏放不下。改为纵向堆叠。
   视频元素自身带 width/height 属性，需要用 CSS 覆盖成自适应。 */
@media (max-width: 1100px) {
    .main {
        flex-direction: column;
        align-items: center;
        height: auto;
        gap: 24px;
        padding: 32px 16px;
    }
    .main .Box1,
    .main .Box2,
    .main .Box3 {
        margin: 0;
        width: min(520px, 100%);
        height: auto;
        min-height: 0;
    }
    .main .Box1,
    .main .Box3 {
        padding-bottom: 16px;
    }
    .main .BoxVideeo {
        width: 100%;
        height: auto;
    }
}
</style>
