<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { ApiError } from '@/api/http.js'
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const formTitle = ref('注册信息')
const message = ref('')

const username = ref('')
const password = ref('')
const checkPassword = ref('')
const email    = ref('')

async function register () {

    if (username.value === '' || password.value === '' || checkPassword.value === '' || email.value === '') {
        message.value = '请填写完整信息'
        return
    }
    if (password.value !== checkPassword.value) {
        message.value = '两次密码不一致'
        return
    }

    message.value = ''

    try {
        await auth.register({
            username: username.value,
            password: password.value,
            email: email.value,
        })
        // 注册成功后直接登录并回首页
        await auth.login({ username: username.value, password: password.value })
        router.push('/')
    } catch (error) {
        message.value = error instanceof ApiError ? error.message : '注册失败，请稍后重试'
        if (!(error instanceof ApiError)) console.error(error)
    }
}

function login(){
    router.push('/login')
}

</script>

<template>

    <div></div>
    <div class="main">
        <div class="main_Navigation">
            <div class="Navigation_Logo"></div>
            <div class="Navigation_Title">计科账号</div>
            <h3>
                <a href="#">用户协议</a> |
                <a href="#">隐私政策</a> |
                <a href="#">帮助中心</a>
            </h3>
        </div>
        <div class="Register_Body">
            <div class="Body_Title">
                <div class="a1">
                    <a href="#" @click.prevent="login">登录</a>
                </div>
                <div class="a2">
                    <a href="#" @click.prevent>注册</a>
                </div>
            </div>
            <div class="Register_Form">
                <form>
                    <div class="Form_Username">
                        <div class="Logo"></div>
                        <input v-model="username" @keyup.enter="register" type="text" placeholder="注册用户名" name="注册用户名" class="Doc">
                    </div>
                    <div class="Form_Password">
                        <div class="Logo1"></div>
                        <input v-model="password" @keyup.enter="register" type="password" placeholder="注册密码" name="注册密码" class="Password">
                    </div>
                    <div class="Form_Confirm">
                        <div class="Logo2"></div>
                        <input v-model="checkPassword" @keyup.enter="register" type="password" placeholder="确认您的注册密码" name="确认注册密码" class="Confirm">
                    </div>
                    <div class="Form_Email">
                        <div class="Logo3"></div>
                        <input v-model="email" @keyup.enter="register" type="email" placeholder="输入您的邮箱" name="用户邮箱" class="Email">
                    </div>
                    <div class="Form_Bottom">
                        <div class="Bottom_Login">
                            <input @click="login" type="button" value="登录" class=Buttom1 style="width: 108px;
                            height: 40px;"/>
                        </div>
                        <div class="Bottom_Register">
                            <input @click="register" type="button" value="注册" class="Buttom2" style="width: 108px;
                            height: 40px;"/>
                        </div>
                        <div class="Bottom_List">
                        </div>
                    </div>
                    <div v-if="message" class="Form_Message">{{ message }}</div>
                    <div class="Form_End">
                        <div class="Havebeen">
                            <a href="#" @click.prevent="login">已有账号？去登录</a>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="End">闽江学院国际数字经济学院计算机科学与技术专业版权所有</div>
    </div>

</template>

<style scoped>

.Form_Message {
    clear: both;
    padding: 10px 0 0 24px;
    font-size: 14px;
    color: #ff8500;
    line-height: 1.5;
}


*{
    padding: 0;
    margin: 0;
}
.main {
    width: 100%;
    background-color: rgb(0, 0, 0, 0.9);
}
.main .main_Navigation {
    width: 100%;
    height: 80px;
    /* background-color: rgb(0, 0, 0, 0.7); */
    /* border-bottom: 3px solid #ff8500; */
    /* position: relative; */
}
.main .main_Navigation .Navigation_Logo {
    width: 80px;
    height: 80px;
    /* position: absolute; */
    /* background-color: pink; */
    /* top: 50%; */
    /* margin-top: -20px; */
    margin-left: 100px;
    background-image: url(@img/IDEC_CE_Logo.png);
    background-size: 100px 100px;
    background-position: center;
    background-repeat: no-repeat;
    float: left;
}
.main .main_Navigation .Navigation_Title {
    width: 114px;
    height: 80px;
    font-size: 26px;
    line-height: 80px;
    color: #fcfcfc;
    /* background-color: #fff; */
    float: left;
}
.main .main_Navigation h3 {
    width: 250px;
    height: 80px;
    font-size: 14px;
    line-height: 80px;
    font-weight: 400;
    color: #838383;
    float: right;
}
.main .main_Navigation h3 a {
    color: #838383;
    text-decoration: none;
}
.main .main_Navigation h3 a:hover {
    color: #ff8500;
}
.main .Register_Body {
    width: min(405px, 100%);
    height: 528.375px;
    background-color: rgb(225, 225, 225, 0.1);
    margin: 90px auto;
    border-radius: 10px 10px 10px 10px;
}
.main .Register_Body .Body_Title {
    width: 360px;
    height: 41px;
    /* background-color: #fff; */
    margin-top: 30px;
    margin-bottom: 0;
    margin-left: 22.5px;
    margin-right: 22.5px;
    float: left;
}
.main .Register_Body .Body_Title .a1 {
    width: 44px;
    height: 41px;
    line-height: 41px;
    /* background-color: #fff; */
    /* border-bottom: 3px solid #ff8500; */
    text-align: center;
    float: left;
} 
.main .Register_Body .Body_Title .a1 a {
    color: #bbbbbb;
    text-decoration: none;
    font-size: 20px;
}
.main .Register_Body .Body_Title .a1 a:hover {
    color: #ff8500;
}
.main .Register_Body .Body_Title .a2 {
    width: 44px;
    height: 41px;
    line-height: 41px;
    margin-left: 20px;
    border-bottom: 3px solid #ff8500;
    float: left;
    text-align: center;
}
.main .Register_Body .Body_Title .a2 a {
    color: #bbbbbb;
    text-decoration: none;
    font-size: 20px;
    font-weight: 700;
}
.main .Register_Body .Body_Title .a2 a:hover {
    color: #ff8500;
}
.main .Register_Body .Register_Form {
    width: 360px;
    height: 335.38px;
    margin-left: 24px;
    margin-top: 40px;
    margin-bottom: 0;
    float: left;
    /* background-color: #fff; */
}
.main .Register_Body .Register_Form .Form_Username {
    width: 354px;
    height: 40px;
    /* background-color: pink; */
}
.main .Register_Body .Register_Form .Form_Username .Logo {
    width: 40px;
    height: 40px;
    background-color: rgb(0, 0, 0, 0.3);
    background-image: url(@img/登录.png);
    background-size: 20px 20px;
    border-radius: 7px;
    background-repeat: no-repeat;
    background-position: center;
    float: left;
}
.main .Register_Body .Register_Form .Form_Username .Doc {
    width: 294px;
    height: 40px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Register_Body .Register_Form .Form_Username .Doc:hover {
    caret-color: #ff8500;
}
.main .Register_Body .Register_Form .Form_Password {
    width: 354px;
    height: 40px;
    margin-top: 35px;
    /* background-color: #fff; */
}
.main .Register_Body .Register_Form .Form_Password .Logo1 {
    width: 40px;
    height: 40px;
    background-color: rgb(0, 0, 0, 0.3);
    background-image: url(@img/密码.png);
    background-size: 20px 20px;
    border-radius: 7px;
    background-repeat: no-repeat;
    background-position: center;
    float: left;
}
.main .Register_Body .Register_Form .Form_Password .Password {
    width: 294px;
    height: 40px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Register_Body .Register_Form .Form_Password .Password:hover {
    caret-color: #ff8500;
}
.main .Register_Body .Register_Form .Form_Confirm {
    width: 354px;
    height: 40px;
    margin-top: 35px;
}
.main .Register_Body .Register_Form .Form_Confirm .Logo2 {
    width: 40px;
    height: 40px;
    background-color: rgb(0, 0, 0, 0.3);
    background-image: url(@img/确认密码.png);
    background-size: 18px 18px;
    border-radius: 7px;
    background-repeat: no-repeat;
    background-position: center;
    float: left;
}
.main .Register_Body .Register_Form .Form_Confirm .Confirm {
    width: 294px;
    height: 40px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Register_Body .Register_Form .Form_Confirm .Confirm:hover {
    caret-color: #ff8500;
}
.main .Register_Body .Register_Form .Form_Email {
    width: 354px;
    height: 40px;
    margin-top: 35px;
}
.main .Register_Body .Register_Form .Form_Email .Logo3 {
    width: 40px;
    height: 40px;
    background-color: rgb(0, 0, 0, 0.3);
    background-image: url(@img/邮箱.png);
    background-size: 18px 18px;
    border-radius: 7px;
    background-repeat: no-repeat;
    background-position: center;
    float: left;
}
.main .Register_Body .Register_Form .Form_Email .Email {
    width: 294px;
    height: 40px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Register_Body .Register_Form .Form_Email .Email:hover {
    caret-color: #ff8500;
}
.main .Register_Body .Register_Form .Form_Bottom {
    width: 354px;
    height: 40px;
    /* background-color: #fff; */
    margin-top: 30px;
}
.main .Register_Body .Register_Form .Form_Bottom .Bottom_Login {
    width: 108px;
    height: 40px;
    /* background-color: pink; */
    float: left;
}
.Buttom1 {
    background-color: #ff8500;
    font-size: 18px;
    color: #fcfcfc;
    border-radius: 7px;
    border: none;
    cursor: pointer;
}
.Buttom1:hover {
    background-color: rgb(255, 153, 18);
}
.main .Register_Body .Register_Form .Form_Bottom .Bottom_Register {
    width: 108px;
    height: 40px;
    /* background-color: pink; */
    margin-left: 15px;
    float: left;
}
.Buttom2 {
    background-color: #ff8500;
    font-size: 18px;
    color: #fcfcfc;
    border-radius: 7px;
    border: none;
    cursor: pointer;
}
.Buttom2:hover {
    background-color: rgb(255, 153, 18);
}
.main .Register_Body .Register_Form .Form_Bottom .Bottom_List {
    width: 108px;
    height: 40px;
    /* background-color: pink; */
    /* margin-left: 20px ; */
    float: right;
}
.Buttom3 {
    background-color: #ff8500;
    font-size: 18px;
    color: #fcfcfc;
    border-radius: 7px;
    border: none;
    cursor: pointer;
}
.Buttom3:hover {
    background-color: rgb(255, 153, 18);
}
.main .Register_Body .Register_Form .Form_End {
    width: 356px;
    height: 36.71px;
    /* background-color: #fff; */
    margin-top: 10px;
}
.main .Register_Body .Register_Form .Form_End .Havebeen {
    width: 90px;
    height: 36.71px;
    float: left;
    line-height: 36.71px;
    text-align: center;
}
.main .Register_Body .Register_Form .Form_End .Havebeen a {
    font-size: 17px;
    font-weight: 200;
    color: #ff8500;
    text-decoration: none;
}
.main .Register_Body .Register_Form .Form_End .Havebeen a:hover {
    color: #bbbbbb;
}
.main .Register_Body .Register_Form .Form_End .Out {
    width: 121.71px;
    height: 36.71px;
    float: right;
}
.main .Register_Body .Register_Form .Form_End .Out .Out_Logo {
    width: 36.71px;
    height: 36.71px;
    background-image: url(@img/退出登录.png);
    background-size: 25px 25px;
    background-position: center;
    background-repeat: no-repeat;
    float: left;
}
.main .Register_Body .Register_Form .Form_End .Out .Out_Doc {
    width: 85px;
    height: 36.71px;
    line-height: 36.71px;
    text-align: center;
    float: left;
}
.main .Register_Body .Register_Form .Form_End .Out .Out_Doc a {
    font-size: 17px;
    font-weight: 200;
    color: #ff8500;
    text-decoration: none;
}
.main .Register_Body .Register_Form .Form_End .Out .Out_Doc a:hover {
    color: #bbbbbb;
}
.main .End {
    width: 100%;
    height: 30px;
    line-height: 30px;
    font-size: 15px;
    font-weight: 200;
    margin-top: 280px;
    background-color: rgb(0, 0, 0, 0);
    color: #bbbbbb;
    text-align: center;
    /* background-color: #fff; */
    /* position: fixed; */
    bottom: 0;
}

</style>