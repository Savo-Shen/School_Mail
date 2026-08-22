<script setup>
    
</script>

<template>
    <div class="main">
        <div class="Box0">
            <div class="Box0_Photo">
                <div class="front"></div>
                <div class="brack"></div>
                <div class="left"></div>
                <div class="right"></div>
                <div class="top"></div>
                <div class="bottom"></div>
            </div>
        </div>
        <div class="Box1">
            <div class="Text">
                <div class="title">
                    <p>计算机科学与技术专业实践</p>
                </div>
                <div class="title_English">
                    <p>Professional Practice of Computer Science and Technology</p>
                </div>
                <div class="Doc">
                    <p>
                        在余根平老师的带领下,21级计科的同学们前往网龙网络公司进行了为期一周的专业实践活动。同学们在网龙公司体验了各式各样的VR设备,感受到了新时代的高科技设备带来的冲击力。同时网龙网络公司的高管们也亲自下场为国际学院的学生们进行授课，其中包括人力资源总监的职业生涯规划课，技术总监帮助同学们深入了解计算机行业现状及未来的课程，还有锻炼大家团队协作能力的异域文化体验课程。
                    </p>
                    <p>
                        一周下来干货满满的课程让同学们受益匪浅，最后一天各个小组的成果汇报也是精彩纷呈，大家通过不同的演绎方式表达出了一周的学习之后自己的收获，相信通过这一次的专业实践，计科班级的同学们对自己接下来的大学生涯乃至未来的职业发展都有了更加清晰的定位和认知。
                    </p>
                </div>
            </div>
            <div class="Photo"></div>
        </div>
        <div class="Box2">
            <div class="Photo2"></div>
            <div class="Text2">
                <div class="title2">
                    <p>计科专业学生接受国防教育</p>
                </div>
                <div class="title2_English">
                    <p>Students majoring in engineering receive national defense education</p>
                </div>
                <div class="Doc2">
                    <p>在2021年的12月份国际数字经济学院的学生们迎来了军训。计科专业的同学们被分为了走队列和军体拳两个方阵,在教官的严格教导下，通过十天的训练同学们组成的队列从一开始的歪七扭八变成了训练有素、整齐划一，而军体拳科目的同学打起拳来也是虎虎生风，颇有一番“国家兴亡，匹夫有责”的威猛气势。</p>
                    <p>最后，在汇报展示上同学们也顺利地展示了各自科目的训练成果，这也寓意着这次的军训锻炼大家勇于面对挫折，挑战困难的目的顺利达成。</p>
                </div>
            </div>
        </div>
        <div class="Box3">
            <div class="card" id="card1">
                <p class="title3">团日活动-篮球赛</p>
                <div class="doc">
                    <p>这是一场计算机科学与技术专业与电子商务专业的友谊赛，但特别的是我们邀请来了我们学院的外国教授。大家因为对篮球的热爱聚到了一起，秉承着“友谊第一，比赛第二”的原则为大家献上了一场精彩而富有竞技性的比赛。</p>
                </div>
            </div>
            <div class="card" id="card2">
                <p class="title3">团日活动-制作口罩</p>
                <div class="doc">
                    <p>在新冠疫情的大背景下口罩早已成为每个人形影不离的“时尚单品”，如今在生活中也出现了许多独具一格的口罩样式，所以我们举办这次活动。在保证实用性的前提下让大家制作自己的创意口罩。</p>
                </div>
            </div>
            <div class="card" id="card3">
                <p class="title3">团日活动-红色剧本杀</p>
                <div class="doc">
                    <p>21级计科专业的同学们跟随红色潮流,创新团日活动形式，选择了最近流行的红色剧本杀来举办本次活动。此次选取的剧本改编自真实的历史事件，讲述的是解放战争期间，中共地下党为解放天津作出不懈努力和牺牲的故事。参与的同学们穿越历史时空，走进峥嵘岁月，通过沉浸式演绎自己的角色来感受那一段先烈们的艰辛岁月，致敬革命先辈，汲取奋进力量。</p>
                </div>
            </div>
            <div class="card" id="card4">
                <p class="title3">团日活动-晨跑</p>
                <div class="doc">
                    <p>在“请党放心,强国有我”主题团日活动中,21计科班级的同学们抖擞精神,展示积极向上、气宇轩昂的精神面貌举办了本次的晨跑活动。团支书领头高举班旗迎风奔跑，后面的同学们人手一面五星红旗组成整齐的方阵紧随其后，在清晨的致远田径场形成了一道动人的风景线。</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.Box0 {
    background-color: #F5FFFA;
    height: 600px;
    -moz-user-select:none; 
    -webkit-user-select:none; 
    -ms-user-select:none; 
    -khtml-user-select:none; 
    user-select:none; 
    display: flex;
    justify-content: center;
}
.Box0 .Box0_Photo {
    position: relative;
    width: min(400px, 100%);
    height: 400px;
    margin-top: 100px;
    /* background-color: pink; */
    /*保留子元素3D动画效果*/
    transform-style:preserve-3d;
    /*俯角预览效果预设，方便查看3D效果*/
    transform:rotate3d(1,1,0,-30deg);
    /*定义动画执行时间*/
    transition:transform 5s;
}
.Box0 .Box0_Photo>div {
    position:absolute;
    width: min(400px, 100%);
    height: 400px;
    line-height: 100px;
    text-align: center;
    /*设置透明度*/
    opacity: 0.9;
}
.front {
    /* background-color: red; */
    background-image: url(@img/专业实践/专业实践.jpg);
    background-size: 400px 400px;
    transform:translateZ(200px);
}
.brack {
    /* background-color: green; */
    background-image: url(@img/basketball_game/bg0.jpeg);
    background-size: 400px 400px;
    transform:translateZ(-200px);
}
.left {
    /* background-color: blue; */
    background-image: url(@img/军训.jpg);
    background-size: 400px 400px;
    transform:translateX(-200px) rotateY(-90deg);
}
.right {
    /* background-color: cyan; */
    background-image: url(@img/专业实践/专业实践5.jpg);
    background-size: 400px 400px;
    transform:translateX(200px) rotateY(90deg);
}
.top {
    /* background-color: pink; */
    background-image: url(@img/专业风光/专业风光2.jpg);
    background-size: 400px 400px;
    transform:translateY(-200px) rotateX(90deg);
}
.bottom {
    /* background-color: purple; */
    background-image: url(@img/专业风光/专业风光1.jpg);
    background-size: 400px 400px;
    transform:translateY(200px) rotateX(-90deg);
}.Box0_Photo:active{
    transform:rotate3d(1,1,0,360deg) rotate3d(0,1,1,360deg);
}
.main .Box1 {
    height: 700px;
    background-color: rgba(20, 42, 49);
    display: flex;
    justify-content: space-around;
}
.main .Box1 .Text {
    height: 600px;
    width: min(650px, 100%);
    /* background-color: antiquewhite; */
}
.main .Box1 .Text .title {
    float: left;
    width: min(650px, 100%);
    margin-top: 80px;
}
.main .Box1 .Text .title p {
    text-align: center;
    font-size: 28px;
    margin-top: 40px;
    color: white;
}
.main .Box1 .Text .title_English {
    width: min(650px, 100%);
    float: left;
}
.main .Box1 .Text .title_English p {
    text-align: center;
    font-size: 20px;
    margin-top: 15px;
    color: rgba(235, 235, 235, 0.64);
}
.main .Box1 .Text .Doc {
    width: min(630px, 100%);
    /* height: 100px; */
    margin-top: 10px;
    margin-left: 10px;
    /* background-color: pink; */
    float: left;
}
.main .Box1 .Text .Doc p {
    text-align: justify;
    text-indent: 2em;
    font-size: 18px;
    margin-top: 30px;
    color: rgb(138, 202, 218);;
}
.main .Box1 .Photo {
    height: 500px;
    width: min(650px, 100%);
    margin-top: 76px;
    border-radius: 15px;
    /* background-color: aliceblue; */
    background-image: url(@img/专业实践/专业实践.jpg);
    background-size: 650px 500px;
    background-position: center;
    background-repeat: no-repeat;

    /* border-style: solid; */
    display: block;
    -webkit-transition:width 2s, height 2s, -webkit-transform 2s;
    transition:width 2s, height 2s, transform 2s;
}
.main .Box1 .Photo:hover {
    width: min(750px, 100%);
    height: 600px;
    background-size: 750px 600px;
    -webkit-transform:rotate(360deg);
    transform:rotate(360deg);
}
.main .Box2 {
    height: 700px;
    background-color: #F5FFFA;
    display: flex;
    justify-content: space-around;
}
.main .Box2 .Photo2 {
    height: 500px;
    width: min(650px, 100%);
    margin-top: 76px;
    border-radius: 15px;
    /* background-color: aliceblue; */
    background-image: url(@img/军训.jpg);
    background-size: 650px 500px;
    background-position: center;
    background-repeat: no-repeat;

    /* border-style: solid; */
    display: block;
    -webkit-transition:width 2s, height 2s,-webkit-transform 2s;
    transition:width 2s, height 2s, transform 2s;
}
.main .Box2 .Photo2:hover {
    width: min(750px, 100%);
    height: 600px;
    background-size: 750px 600px;
    -webkit-transform:rotate(360deg);
    transform:rotate(360deg);
}
.main .Box2 .Text2 {
    height: 600px;
    width: min(650px, 100%);
}
.main .Box2 .Text2 .title2 {
    float: left;
    width: min(650px, 100%);
    margin-top: 120px;
}
.main .Box2 .Text2 .title2 p {
    text-align: center;
    font-size: 28px;
    margin-top: 40px;
    color: 	#BDB76B;
}
.main .Box2 .Text2 .title2_English {
    width: min(650px, 100%);
    float: left;
}
.main .Box2 .Text2 .title2_English p {
    text-align: center;
    font-size: 20px;
    margin-top: 15px;
    color:  #F0E68C;
}
.main .Box2 .Text2 .Doc2 {
    width: min(630px, 100%);
    margin-top: 10px;
    margin-left: 10px;    
    float: left;
}
.main .Box2 .Text2 .Doc2 p {
    text-align: justify;
    text-indent: 2em;
    font-size: 18px;
    margin-top: 30px;
    color: #808000;
}
.main .Box3 {
    height: 600px;
    width: 100%;
    background-color: rgba(20, 42, 49);
    display: flex;
    justify-content: space-around;
}
.main .Box3 .card {
    width: 250px;
    height: 410px;
    margin-top: 110px;
    border: 1.5008px solid rgb(138, 202, 218);
    background-color: aliceblue;
}
.main .Box3 .card .doc {
    width: 220px;
    margin-left: 15px;
    margin-top: 10px;
    text-align: justify;
    font-size: 16px;
    color: black;
    margin-top: 10px;
    text-indent: 2em;
}
.main .Box3 .card .title3 {
    text-align: center;
    font-size: 20px;
    color: rgb(138, 202, 218);
    margin-top: 25px;
}
#card1 {
    animation-duration: 2s;
    animation-name: transform1;
}
@keyframes transform1 {
    from {
        margin-top: 100%;
        height: 410px;
    }
    to {
        height: 410px;
    }
}
#card2 {
    animation-duration: 2.5s;
    animation-name: transform2;
}
@keyframes transform2 {
    from {
        margin-top: 100%;
        height: 410px;
    }
    to {
        height: 410px;
    }
}
#card3 {
    animation-duration: 3s;
    animation-name: transform3;
}
@keyframes transform3 {
    from {
        margin-top: 100%;
        height: 410px;
    }
    to {
        height: 410px;
    }
}
#card4 {
    animation-duration: 3.5s;
    animation-name: transform4;
}
@keyframes transform4 {
    from {
        margin-top: 100%;
        height: 410px;
    }
    to {
        height: 410px;
    }
}
/* .main .Box4 {
    height: 100px;
    background-color: rgba(20, 42, 49);
} */

/* 响应式：
   .Box2 是「照片 650px + 文字 650px」双栏，.Box3 是四张 250px 卡片一行，
   窄屏都放不下。改为堆叠/换行，并把写死的容器高度改成自适应
   （否则内容换行后会溢出容器）。 */
@media (max-width: 1100px) {
    .main .Box2 {
        flex-direction: column;
        align-items: center;
        height: auto;
        gap: 24px;
        padding: 32px 16px;
    }
    .main .Box2 .Photo2,
    .main .Box2 .Text2 {
        width: min(650px, 100%);
        height: auto;
        margin-top: 0;
    }
    .main .Box2 .Text2 .title2 {
        float: none;
        width: 100%;
        margin-top: 0;
    }
    .main .Box2 .Text2 .Doc2 {
        float: none;
        width: 100%;
        margin-left: 0;
    }

    .main .Box3 {
        flex-wrap: wrap;
        justify-content: center;
        height: auto;
        gap: 20px;
        padding: 40px 16px;
    }
    .main .Box3 .card {
        margin-top: 0;
        height: auto;
        min-height: 340px;
        flex: 0 1 250px;
        padding-bottom: 16px;
    }
}

@media (max-width: 560px) {
    .main .Box3 .card {
        flex: 1 1 100%;
        width: 100%;
    }
    .main .Box3 .card .doc {
        width: auto;
        margin-left: 15px;
        margin-right: 15px;
    }
}
</style>
