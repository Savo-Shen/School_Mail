<script setup>

</script>

<template>
    <div class="main">
        <div class="Y_All">
            <div class="Y_Navigation">
                <h3 class="Y_Navigation_Title">关于我们</h3>
            </div>
            <div class="Y_Doc">
                <div class="Y_Doc_Navigation">
                    <h4>关于我们</h4>
                    <div class="empty">
                        <h3>当前位置 | <a href="#">关于我们</a></h3>
                    </div>
                </div>
                <div class="Y_Doc_Line"></div>
                <div class="Y_Doc_Text">
                    <p class="Text_Title">
                        <strong>关于我们</strong>
                    </p>
                    <!-- <p class="Text_Title_English">
                        <strong>About us</strong>
                    </p> -->
                    <div class="Text_Map"></div>
                    <div class="DOC">
                        <p class="Member">
                            <strong style="color: #ff8500;">团队成员</strong>
                        </p>
                        <p class="Member_Text">
                            来自21级计算计科学与技术专业的Savo Shen,Ethan(雷锘)以及Shark(奇杭)组成的小团队。
                        </p>
                        <p class="Intention">
                            <strong style="color: #ff8500;">创立初衷</strong>
                        </p>
                        <p class="Intention_Text">
                            为部分有想法、有自主学习能力的同学建立的一个团队合作小项目，以规范的项目开发模式，让大家一起努力学习，创立了这个网站。
                        </p>
                        <p class="Idea">
                            <strong style="color: #ff8500;">创作理念</strong>
                        </p>
                        <ul class="Idea_Text">
                            <li>
                                用最新的网站开发技术,vue + Django 前后端分离开发。
                            </li>
                            <li>
                                学习使用git代码管理,完成团队协作。
                            </li>
                        </ul>
                        <p class="Target">
                            <strong style="color: #ff8500;">团队目标</strong>
                        </p>
                        <ul class="Target_Text">
                            <li>
                                为计科专业的同学们打造一个可以交流学习、生活以及各个方面问题的平台。
                            </li>
                            <li>
                                完成网站框架制作。
                            </li>
                            <li>
                                制作"学习二十大"主题活动页面。
                            </li>
                        </ul>
                        <p class="Join">
                            <strong style="color: #ff8500;">加入我们
                            </strong>
                        </p>
                        <p class="Join_Text">
                            诚邀各位有热情，对编程有兴趣的小伙伴们加入我们的项目。为我们的网站添砖加瓦，贡献属于自己的力量！
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
* {
    margin: 0;
    padding: 0;
}
.main {
    width: 100%;
    /* height: 1110px; */
    background-color: rgb(225, 225, 225, 0.9);
    /* background-color: pink; */
    display: flex;
    justify-content: center;
}
.main .Y_All {
    width: min(1200px, 100%);
    height: 800px;
    margin-bottom: 100px;
    /* background-color: pink; */
    /* margin: 20px auto; */
}
.main .Y_All .Y_Navigation {
    width: 240px;
    height: 52px;
    border-radius: 20px 20px 20px 20px;
    box-shadow: 5px 5px 5px 5px rgb(0, 0, 0, 0.3);
    background-color:  rgb(0, 0, 0, 0.7);
    border-bottom: 2px solid #ff8500;
    position: fixed;
    float: left;
}
.main .Y_All .Y_Navigation h3 {
    /* width: 240px; */
    height: 50px;
    font-size: 20px;
    font-weight: 400;
    line-height: 50px;
    padding-left: 25px;
    /* background-color: #ff8500; */
    /* border-bottom: 2px solid #ff8500; */
    color: #fcfcfc;
}
li {
    list-style: none;
}
.main .Y_All .Y_Navigation ul li {
    height: 43px;
    line-height: 43px;
    padding-left: 20px;
    font-weight: 200;
}
.main .Y_All .Y_Navigation ul li a {
    font-size: 18px;
    color: #fcfcfc;
    text-decoration: none;
}
.main .Y_All .Y_Navigation ul li a:hover {
    color: #ff8500;
    text-decoration: underline;
}
.main .Y_All .Y_Doc {
    width: min(940px, 100%);
    height: 800px;
    /* border-radius: 20px 20px 20px 20px; */
    box-shadow: 5px 5px 5px 5px rgb(0, 0, 0, 0.3);
    background-color:  rgb(0, 0, 0, 0.7);
    /* background-color: green; */
    float: right;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation {
    width: min(940px, 100%);
    height: 48px;
    display: flex;
    justify-content: space-between;
    /* border-radius: 20px 20px 0px 0px; */
    /* background-color: pink; */
}
.main .Y_All .Y_Doc .Y_Doc_Navigation h4 {
    height: 48px;
    font-size: 20px;
    line-height: 48px;
    padding: 0 20px;
    font-weight: 400;
    text-align: center;
    color: #ff8500;
    border-bottom: 3px solid rgb(225, 225, 225, 0.5);
    float: left;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation .empty {
    /* width: min(820px, 100%); */
    height: 48px;
    /* background-color: pink; */
    /* border-bottom: 1px solid rgb(225, 225, 225, 0.5); */
    float: left;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation .empty h3 {
    width: 215px;
    height: 48px;
    line-height: 48px;
    font-size: 13px;
    font-weight: 400;
    text-align: center;
    color: rgb(225, 225, 225, 0.5);
    float: right;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation .empty h3 a {
    color: rgb(225, 225, 225, 0.5);
    text-decoration: none;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation .empty h3 a:hover {
    color: #ff8500;
}
.main .Y_All .Y_Doc .Y_Doc_Line {
    width: 100%;
    height: 1px;
    background-color: rgb(225, 225, 225, 0.5);
}
.main .Y_All .Y_Doc .Y_Doc_Text p {
    color: #fcfcfc;
    font-size: 20px;
    line-height: 1.5em;
    text-align: justify;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Title {
    margin-top: 10px;
    text-align: center;
    line-height: 29px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Title_English {
    text-align: center;
    margin-top: 10px;
    line-height: 29px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Map {
    margin-top: 10px;
    margin-left: 120px;
    width: min(700px, 100%);
    height: 250px;
    /* background-color: #fff; */
    background-image: url(@img/MJU_Map.png);
    background-size: 700px 250px;
    background-repeat: no-repeat;
    background-position: center;
}
.main .Y_All .Y_Doc .Y_Doc_Text .DOC {
    margin-top: 30px;
    margin-left: 20px;
    width: min(900px, 100%);
    /* height: 200px; */
    /* background-color: #fff; */
}
.main .Y_All .Y_Doc .Y_Doc_Text .Member {
    font-size: 18px;
    text-indent: 42px;
    margin-top: 10px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Member_Text {
    font-size: 16px;
    text-indent: 42px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Intention {
    font-size: 18px;
    text-indent: 42px;
    margin-top: 10px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Intention_Text {
    font-size: 16px;
    text-indent: 42px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Idea {
    font-size: 18px;
    text-indent: 42px;
    margin-top: 10px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Idea_Text {
    font-size: 16px;
    /* text-indent: 42px; */
    margin-left: 55px;
    color: #fcfcfc;
    line-height: 1.5em  ;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Idea_Text li {
    list-style: disc;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Target {
    font-size: 18px;
    text-indent: 42px;
    margin-top: 10px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Target_Text {
    font-size: 16px;
    /* text-indent: 42px; */
    margin-left: 55px;
    color: #fcfcfc;
    line-height: 1.5em  ;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Target_Text li {
    list-style: disc;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Join {
    font-size: 18px;
    text-indent: 42px;
    margin-top: 10px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Join_Text {
    font-size: 16px;
    text-indent: 42px;
}
</style>