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
                    <h4>现任领导</h4>
                    <div class="empty">
                        <h3>当前位置 | <a href="#">专业概况</a> | <a href="#">现任领导</a></h3>
                    </div>
                </div>
                <div class="Y_Doc_Text">
                    <div class="Text_Table">
                        <table border="1" cellpadding="0" cellspacing="0">
                            <tbody>
                                <tr>
                                    <td id="_width">
                                        <p>
                                            计算机科学与专业主任
                                        </p>
                                        <p>汪涛</p>
                                    </td>
                                    <td id="DOC">汪涛,男,1987年3月出生,福建福州人,博士/副教授。历任闽江学院计算机与控制工程学院讲师、院长助理。现任闽江学院国际数字经济学院院长助理、计算机科学与技术系主任。</td>
                                </tr>
                                <tr>
                                    <td>
                                        <p>
                                            2022级计科专业班主任
                                        </p>
                                        <p>
                                            余根平
                                        </p>
                                    </td>
                                    <td id="DOC">
                                        余根平,男,1989年11月出生,福建南平人,在读博士\助教,历任闽江学院互联网创新研究中心创新创业部主任,2021年6月任闽江学院国际数字经济学院计算机专业教师
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <p>
                                            2021级计科专业班主任
                                        </p>
                                        <p>
                                            陈震宇
                                        </p>
                                    </td>
                                    <td id="DOC">陈震宇,男,1997年10月出生,福建福州人,2022年2月历任闽江学院国际数字经济学院计算机科学与技术助教。</td>
                                </tr>
                                <tr>
                                    <td>
                                        <p>
                                            2021级计科专业辅导员
                                        </p>
                                        <p>
                                            陈伟伟
                                        </p>
                                    </td>
                                    <td id="DOC">陈伟伟,中共党员,文学硕士,毕业于南京师范大学,现任国际数字经济学院2021级、2022级辅导员。曾获得校社会实践先进个人、优秀共青团干部、三好学生等荣誉。</td>
                                </tr>
                                <tr>
                                    <td>
                                        <p>
                                            2022级计科专业辅导员 
                                        </p>
                                        <p>
                                            石思沅
                                        </p>
                                    </td>
                                    <td id="DOC">石思沅,福建福鼎人,毕业于厦门大学。现任国际数字经济学院2022级辅导员,喜好游泳,热爱自然。</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
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
    height: 1110px;
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
    height: 700px;
    /* background-color: pink; */
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
    height: 700px;
    /* border-radius: 20px 20px 20px 20px; */
    box-shadow: 5px 5px 5px 5px rgb(0, 0, 0, 0.3);
    background-color:  rgb(0, 0, 0, 0.7);
    /* background-color: green; */
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
    margin: 0;
    padding: 0;
    width: min(940px, 100%);
    height: 640px;
    /* background-color: #fff; */
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Table {
    margin-top: 140px;
    margin-left: 20px;
    width: min(900px, 100%);
    height: 400px;
    /* background-color: #fff; */
    text-align: center;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Table table {
    border: 1px solid rgb(225, 225, 225, 0.7);
    font-size: 18px;
    color: #fcfcfc;
}
#_width {
    width: 250px;
}
#DOC {
    line-height: 1.5em;
    font-size: 16px;
    text-align: justify;
}
.main .Y_All .Y_Doc .Y_Doc_Text .Text_Table table p {
    margin-top: 4px;
    margin-bottom: 4px;
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