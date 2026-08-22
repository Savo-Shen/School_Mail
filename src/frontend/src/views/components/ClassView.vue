<script setup>

</script>

<template>
    <div class="main">
        <div id="main_Logo">
            <div id="main_Logo_img"></div>
            <div id="main_Logo_doc">
                <div class="chinese"> 计 算 机 科 学 与 技 术 专 业</div>
                <div class="english">Computer Science and Technology of MinJiang University</div>
            </div>
            <div id="main_Logo_login_img"></div>
            <div id="main_Logo_login_doc"><a href="#">欢迎登录</a></div>
        </div>
        <div class="main_Navigation">
            <div class="main_Navigation1">
                <div class="Navigation_Logo">
                    <div class="Navigation">
                        <a href="#">专业概况</a>
                        <a href="#">班级荣誉</a>
                        <a href="#">学生风采</a>
                        <a href="#">社区互动</a>
                        <a href="#">共创营地</a>
                        <a href="#">关于我们</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="Y_All">
            <div class="Y_Navigation">
                <h3 class="Y_Navigation_Title">专业概况</h3>
                <ul>
                    <li><a href="#">【计科】专业简介</a></li>
                    <li><a href="#">【计科】现任领导</a></li>
                    <li><a href="#">【计科】专业风光</a></li>
                </ul>
            </div>
            <div class="Y_Doc">
                <div class="Y_Doc_Navigation">
                    <!-- <div class="Y_Doc_Navigation_Title">专业简介</div> -->
                    <h4>专业风光</h4>
                    <div class="empty">
                        <h3>当前位置 | <a href="#">专业概况</a> | <a href="#">专业风光</a></h3>
                    </div>
                </div>
                <div class="Y_Doc_Text">
                    <div class="picture1"></div>
                    <div class="picture2"></div>
                    <div class="Doc">计算机科学与技术专业晨跑活动</div>
                    <div class="picture3"></div>
                    <div class="Doc">国际学院计科专业2021-2022团日活动</div>
                    <div class="picture4"></div>
                    <div class="Doc">计算机科学与技术专业军训</div>
                    <div class="picture5"></div>
                    <div class="picture6"></div>
                    <div class="picture7"></div>
                    <div class="Doc">计算机科学与技术专业心理团建</div>
                    <div class="picture8"></div>
                    <div class="picture9"></div>
                    <div class="Doc">计算机科学与技术专业实践</div>
                </div>
            </div>
        </div>
        <div class="_US">
            <div class="_US_Logo"></div>
            <div class="_US_Doc">
                <div class="_link">
                    <a href="#">闽江学院</a> |
                    <a href="#">闽江学院国际数字经济学院</a> |
                    <a href="#">校函</a> |
                    <a href="#">国际学院计算机科学与技术</a> |
                    <a href="#">国际学院计科官网隐私政策</a> |
                    <a href="#">国际学院计科官网用户协议</a> |
                    <a href="#">问题反馈</a> |
                </div>
                <div class="_my">
                    违法和不良信息举报电话:137-7450-2836 |
                    <a href="#">知识产权侵权投诉</a> |
                    本网站所有数据、资料,除特殊说明,均出自于我院专业实验室                     
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
    height: 4064px;
    background-color: rgb(225, 225, 225, 0.9);
    /* background-color: pink; */
}
#main_Logo {
    width: 100%;
    height: 150px;
    background-color: rgb(0, 0, 0, 0.7);
    position: relative;
    /* 父盒子：让子盒子垂直居中显示 */
}
#main_Logo_img {
    width: 240px;
    height: 120px;
    /* background-color: green; */
    /* margin-top: 15px; */
    /* margin-bottom: auto; */
    position: absolute;
    top: 50%;
    margin-top: -60px;
    margin-left: 100px;
    /* 让盒子垂直居中显示 */
    margin-right: 0;
    background-image: url(@img/IDEC_CE_Logo_With_Name.png);
    background-repeat: no-repeat;
    background-position: center;
    background-size: 240px 120px;
    /* float: left; */
}
#main_Logo_doc {
    width: min(600px, 100%);
    height: 120px;
    /* background-color: green; */
    position: absolute;
    top: 50%;
    margin-top: -60px;
    margin-left: 350px;
    /* float: left; */
}
#main_Logo_login_img {
    width: 60px;
    height: 60px;
    position: absolute;
    top: 50%;
    margin-top: -30px;
    margin-left: 1150px;
    /* background-color: pink; */
    background-image: url(@img/登录.png);
    background-size: 40px 40px;
    background-position: center;
    background-repeat: no-repeat;
}
#main_Logo_login_doc {
    width: 100px;
    height: 60px;
    position: absolute;
    top: 50%;
    margin-top: -30px;
    margin-left: 1210px;
    text-align: center;
    line-height: 60px;
}
#main_Logo_login_doc a {
    color: #fcfcfc;
    text-decoration: none;
    font-size: 18px;
    
}
#main_Logo_login_doc a:hover {
    color: #ff8500;
}
.chinese {
    width: min(600px, 100%);
    height: 80px;
    /* background-color: pink; */
    font-size: 38px;
    font-weight: 200;
    line-height: 80px;
    color: #fcfcfc;
}
.english {
    width: min(600px, 100%);
    height: 40px;
    /* background-color: #fff; */
    font-size: 20px;
    color: #fcfcfc;
    line-height: 10px;
}
.main_Navigation {
    width: 100%;
    height: 67.35px;
    border-top: 3px solid #ff8500;
    border-bottom: 2px solid #edeef0;
    background-color: rgb(0, 0, 0, 0.7);
}
.main_Navigation .main_Navigation1 {
    width: min(1300px, 100%);
    height: 67.35px;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
}
.main_Navigation .main_Navigation1 .Navigation {
    width: min(1300px, 100%);
    height: 67.35px;
    line-height: 67.35px;
    margin: 0 auto;
    /* background-color: green; */
    text-align: center;
    /* float: left; */
}
.main_Navigation .main_Navigation1 .Navigation a {
    font-size: 18px;
    height: 67.35px;
    padding: 0 40px;
    color: #fcfcfc;
    text-decoration: none;
    display: inline-block;
}
.main_Navigation .main_Navigation1 .Navigation a:hover {
    background-color: #eee;
    color: black;
}
.main .Y_All {
    width: min(1200px, 100%);
    height: 3650px;
    /* background-color:  rgb(0, 0, 0, 0.7); */
    /* background-color: #fff; */
    margin: 20px auto;
}
.main .Y_All .Y_Navigation {
    width: 240px;
    height: 222px;
    border-radius: 20px 20px 20px 20px;
    box-shadow: 5px 5px 5px 5px rgb(0, 0, 0, 0.3);
    background-color:  rgb(0, 0, 0, 0.7);
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
    border-bottom: 2px solid #ff8500;
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
    height: 3650px;
    /* border-radius: 20px 20px 20px 20px; */
    box-shadow: 5px 5px 5px 5px rgb(0, 0, 0, 0.3);
    background-color:  rgb(0, 0, 0, 0.7);
    float: right;
}
.main .Y_All .Y_Doc .Y_Doc_Navigation {
    width: min(940px, 100%);
    height: 48px;
    /* border-radius: 20px 20px 0px 0px; */
    /* background-color: pink; */
}
.main .Y_All .Y_Doc .Y_Doc_Navigation h4 {
    width: 120px;
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
    width: min(820px, 100%);
    height: 48px;
    /* background-color: pink; */
    border-bottom: 1px solid rgb(225, 225, 225, 0.5);
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
.main .Y_All .Y_Doc .Y_Doc_Text {
    width: min(940px, 100%);
    height: 3650px;
    /* background-color: #fff; */
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture1 {
    width: min(940px, 100%);
    height: 375px;
    /* background-color: #fff; */
    margin-top: 10px;
    background-image: url(@img/专业风光/专业风光1.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture2 {
    width: min(940px, 100%);
    height: 375px;
    margin-bottom: 10px;
    background-image: url(@img/专业风光/专业风光2.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Doc {
    width: min(940px, 100%);
    height: 20px;
    font-size: 18px;
    color: #fcfcfc;
    text-align: center;
    line-height: 20px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture3 {
    width: min(940px, 100%);
    height: 375px;
    margin-bottom: 10px;
    margin-top: 10px;
    background-image: url(@img/专业风光/专业风光3.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture4 {
    width: min(940px, 100%);
    height: 375px;
    margin-bottom: 10px;
    margin-top: 10px;
    background-image: url(@img/专业风光/专业风光4.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture5 {
    width: min(940px, 100%);
    height: 375px;
    /* margin-bottom: 10px; */
    margin-top: 10px;
    background-image: url(@img/专业风光/专业风光5.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture6 {
    width: min(940px, 100%);
    height: 375px;
    /* margin-bottom: 10px;
    margin-top: 10px; */
    background-image: url(@img/专业风光/专业风光6.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture7 {
    width: min(940px, 100%);
    height: 375px;
    margin-bottom: 10px;
    /* margin-top: 10px; */
    background-image: url(@img/专业风光/专业风光7.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture8 {
    width: min(940px, 100%);
    height: 375px;
    /* margin-bottom: 10px; */
    margin-top: 10px;
    background-image: url(@img/专业风光/专业风光8.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
.main .Y_All .Y_Doc .Y_Doc_Text .picture9 {
    width: min(940px, 100%);
    height: 375px;
    margin-bottom: 10px;
    /* margin-top: 10px; */
    background-image: url(@img/专业风光/专业风光9.jpg);
    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px 357px;
}
._US {
    width: 100%;
    height: 150px;
    margin-top: 20px;
    /* height: 100vh; */
    background-color: rgb(0, 0, 0, 0.3);
    /* background-color: pink; */
    /* position: absolute; */
    /* bottom: 0; */
}
.main ._US ._US_Logo {
    width: 150px;
    height: 75px;
    margin-left: 250px;
    /* background-color: #fff; */
    background-image: url(@img/IDEC_CE_Logo_With_Name.png);
    background-size: 150px 75px;
    background-repeat: no-repeat;
    float: left;
}
.main ._US ._US_Doc {
    width: min(700px, 100%);
    height: 150px;
    /* background-color: #fff; */
    float: left;
}
.main ._US ._US_Doc ._link {
    width: min(700px, 100%);
    height: 75px;
    color: #fcfcfc;
    /* line-height: 50px; */
    /* background-color: green; */
}
.main ._US ._US_Doc ._link a {
    font-size: 13px;
    color: #fcfcfc;
    text-decoration: none;
}
.main ._US ._US_Doc ._link a:hover {
    color: #ff8500;
}
.main ._US ._US_Doc ._my {
    width: min(700px, 100%);
    height: 75px;
    /* background-color: pink; */
    font-size: 13px;
    color: #fcfcfc;
}
.main ._US ._US_Doc ._my a {
    font-size: 13px;
    color: #fcfcfc;
    text-decoration: none;
}
.main ._US ._US_Doc ._my a:hover {
    color: #ff8500;
}
</style>