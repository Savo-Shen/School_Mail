<script setup>
function open_linzidaren() {
    window.open(import.meta.env.BASE_URL + "linzidaren/linzidaren_static/linzidaren_static.html")
}
</script>

<template>
    <div class="_all">
        <div class="_US">
            <div class="_US_Logo"></div>
            <div class="_US_Doc">
                <div class="_link">
                    <a href="#">闽江学院</a> |
                    <a href="#">闽江学院国际数字经济学院</a> |
                    <!-- <a href="#">校函</a> | -->
                    <!-- <a href="#">国际学院计算机科学与技术</a> | -->
                    <a href="#">隐私政策</a> |
                    <a href="#">用户协议</a> |
                    <a href="#">问题反馈</a> |
                    <a href="#" @click="open_linzidaren">Linzidaren</a>
                </div>
            </div>
            <div class="_my"> 
                <div class="police">
                    <a href="https://beian.miit.gov.cn/#/Integrated/index">闽ICP备2023002176号</a>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
._all ._US {
    width: 100%;
    background-color: rgb(0, 0, 0, 0.3);
    display: flex;
    /* 统一高度 + 三块垂直居中。
       原来没有设高度，靠 logo 的 75px 撑着，三块高度分别是 75/75/51，
       备案号还靠 .police 的 margin-top:30px 硬怼位置。 */
    align-items: center;
    justify-content: space-between;
    height: 60px;
    padding: 0 40px;
    gap: 24px;
    box-sizing: border-box;
}
._all ._US ._US_Logo {
    width: 120px;
    height: 40px;
    flex: 0 0 auto;
    background-image: url(@img/IDEC_CE_Logo_With_Name.png);
    background-size: contain;
    background-position: left center;
    background-repeat: no-repeat;
}
._all ._US ._US_Doc {
    /* 占据中间剩余空间，让链接真正居中 */
    flex: 1 1 auto;
    display: flex;
    justify-content: center;
    min-width: 0;
}
._all ._US ._US_Doc ._link {
    color: #fcfcfc;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 4px;
    line-height: 1.6;
}
._all ._US ._US_Doc ._link a {
    font-size: 13px;
    color: #fcfcfc;
    text-decoration: none;
}
._all ._US ._US_Doc ._link a:hover {
    color: rgb(255, 255, 255, 0.7);
}
._all ._US ._my {
    /* 原来 float:right 在 flex 容器里是无效声明 */
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    font-size: 13px;
    color: #fcfcfc;
    white-space: nowrap;
}
._all ._US ._my a {
    font-size: 13px;
    color: #fcfcfc;
    text-decoration: none;
}
._all ._US ._my a:hover {
    color: rgb(255, 255, 255, 0.7);
}
.police {
    /* 原来用 margin-top:30px 假装垂直居中，现在由 align-items 处理 */
    margin-top: 0;
}

/* 窄屏下三块堆叠，高度自适应 */
@media (max-width: 860px) {
    ._all ._US {
        flex-direction: column;
        height: auto;
        padding: 16px;
        gap: 10px;
        text-align: center;
    }
    ._all ._US ._US_Doc ._link {
        font-size: 12px;
    }
}
</style>