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
    justify-content: space-around;
    bottom: 0;
    margin-top: 0px;
}
._all ._US ._US_Logo {
    width: 150px;
    height: 75px;
    /* margin-left: 250px; */
    /* background-color: #fff; */
    background-image: url(@img/IDEC_CE_Logo_With_Name.png);
    background-size: 150px 75px;
    background-repeat: no-repeat;
    float: left;
}
._all ._US ._US_Doc {
    /* width: min(700px, 100%); */
    /* background-color: #fff; */
    display: flex;

}
._all ._US ._US_Doc ._link {
    /* width: min(700px, 100%); */
    height: 75px;
    color: #fcfcfc;
    display: flex;
    justify-content: center;
    align-items: center;
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
    height: 100%;
    font-size: 13px;
    color: #fcfcfc;
    float:right;
    align-items: center;
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
    margin-top: 30px;
}
</style>