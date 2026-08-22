<script setup>

</script>

<template>

<div></div>
<div id="main">
    <div class="animate__animated animate__fadeIn" id="text">
        <div id="title">
            <h1>计算机科学与技术专业</h1>
            <h2>Introduction to Computer Science and Technology</h2>
        </div>
        <div id="content">
            <p>计算机科学与技术是为了适应国家数字经济发展的战略需要，培养掌握计算机软硬件系统设计、人工智能和大数据分析以及产业数字化规划与建设能力的高素质复合型人才的专业。本专业将教会同学们信息与计算的理论基础以及其在计算机系统中的实现与应用。</p>
            <p style="margin-top:20px;">通俗地说，我们要学习信息如何在计算机中进行表示和处理，如何通过算法和程序解决我们日常生活中的各种问题，还将学习这些方法在本学科前沿领域如人工智能、嵌入式系统、信息安全、云计算等的应用案例。我们的课程将带领同学们一步步走进丰富多彩的计算机世界，让你从“计算机小白”成长为一名有着扎实理论基础和一定实践经验的计算机工程师。</p>
        </div>
    </div>
    <div class="animate__animated animate__fadeInRight"  id="image">

    </div>
</div>

</template>

<style scoped>

#main {
    min-height: 600px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: white;
    /* 文字 600px + 图片 + 两侧各 100px 边距在 1440 视口下正好占满，
       space-around 分不出空隙，文字和图片会贴在一起 */
    gap: 60px;
    padding: 0 24px;
}

#text {
    max-width: 600px;
    margin-left: 100px;
    display: flex;
    flex-direction: column;
}

#title {
    color:black;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

#content {
    margin-top: 80px;
}

#content p {
    font-size: 16px;
    color: black;
    line-height: 30px;
    text-align: justify;
    text-indent: 2em;
}

#image {
    margin-right: 100px;
    width: min(700px, 100%);
    height: 500px;
    background-image: url("@img/CE.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    border-radius: 25px;
    border: 2px solid #ccc;
    box-shadow: 10px 10px 10px #ccc;
}


/* 响应式：#main 是 文字 + 图片 的双栏 flex，窄屏下会把文字挤成窄条、
   图片被裁。改为纵向堆叠，并把写死的 100px 边距换成自适应内边距。 */
@media (max-width: 900px) {
    #main {
        flex-direction: column;
        min-height: 0;
        padding: 40px 16px;
        gap: 28px;
    }
    #text {
        max-width: 100%;
        margin-left: 0;
    }
    #image {
        margin-right: 0;
        max-width: 100%;
    }
    #content {
        margin-top: 24px;
    }
}
</style>
