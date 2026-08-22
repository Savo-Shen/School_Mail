<script setup>

import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { ApiError } from '@/api/http.js'
import { getRandomBg } from '@js/random_bg.js'
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const title = ref('登录')
const message = ref('')
const username = ref('')
const password = ref('')

const main = ref(null)
const Login_background = getRandomBg()

const isLogin = computed(() => auth.isAuthenticated)

onMounted(() => {
    main.value.style.backgroundImage = "url(" + Login_background + ")"
    if (isLogin.value) {
        message.value = '您已经登录了'
    }
})

async function login() {

    if (username.value === '') {
        message.value = '请填写用户名'
        return
    }
    if (password.value === '') {
        message.value = '请填写密码'
        return
    }

    message.value = ''

    try {
        await auth.login({ username: username.value, password: password.value })
        router.push('/')
    } catch (error) {
        message.value = error instanceof ApiError ? error.message : '登录失败，请稍后重试'
        if (!(error instanceof ApiError)) console.error(error)
    }
}

function register() {
    router.push('/register')
}

</script>

<template>

<div class="main" ref="main">
        <div class="main_Navigation">
            <div class="Navigation_Logo"></div>
            <div class="Navigation_Title">计科账号</div>
            <h3>
                <a href="#">用户协议</a> |
                <a href="#">隐私政策</a> |
                <a href="#">帮助中心</a>
            </h3>
        </div>
        <div class="Body">
            <div class="Body_Title">
                <div class="a1">
                    <a href="#">登录</a>
                </div>
                <div class="a2">
                    <a href="#">注册</a>
                </div>
            </div>
            <div class="Form">
                <form>
                    <div class="From_Username">
                        <div class="Logo"></div>
                        <input v-model="username" @keyup.enter="login" type="text" placeholder="邮箱\手机号码\计科ID" name="用户名" class="Text">
                    </div>
                    <div class="Form_Password">
                        <div class="Logo1"></div>
                        <input v-model="password" @keyup.enter="login" type="password" placeholder="密码" name="Password" class="Password">
                    </div>
                    <div class="Form_Login">
                        <input @click="login" type="button" value="登录" name="登录" class="Login"/>
                    </div>
                    <div class="Form_Register"><input @click="register" type="button" value="注册" name="注册" class="Register"/></div>
                    <label v-if="message" id="message">{{ message }}</label>
                    <div class="Form_End">
                        <div class="Forget">
                            <a href="#">忘记密码?</a>
                        </div>
                        <div class="Out">
                            <div class="Out_Logo"></div>
                            <div class="Out_Doc">
                                <a href="#">退出登录</a>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <div class="Bottom">闽江学院国际数字经济学院计算机科学与技术专业版权所有</div>
    </div>

</template>

<style scoped>

* {
    margin: 0;
    padding: 0;
}
/* #main {
    display: flex;
    justify-content: center;
    align-items: center;
    place-items: center;
    height: 100%;
    width: 100%;
    min-height: 800px;
    min-width: 1200px;
    background-size: cover;
} */
.main {
    width: 100%;
    min-height: 900px;
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
.main .Body {
    width: 405px;
    height: 528.375px;
    background-color: rgb(225, 225, 225, 0.1);
    margin: 90px auto;
    border-radius: 10px 10px 10px 10px;
}
.main .Body .Body_Title {
    width: 360px;
    height: 41px;
    /* background-color: #fff; */
    margin-top: 30px;
    margin-bottom: 0;
    margin-left: 22.5px;
    margin-right: 22.5px;
    float: left;
}
.main .Body .Body_Title .a1 {
    width: 44px;
    height: 41px;
    line-height: 41px;
    /* background-color: #fff; */
    border-bottom: 3px solid #ff8500;
    text-align: center;
    float: left;
} 
.main .Body .Body_Title .a1 a {
    color: #bbbbbb;
    text-decoration: none;
    /* text-align: center; */
    font-size: 20px;
    font-weight: 700;
}
.main .Body .Body_Title .a1 a:hover {
    color: #ff8500;
}
.main .Body .Body_Title .a2 {
    width: 44px;
    height: 41px;
    line-height: 41px;
    margin-left: 20px;
    /* background-color: #fff; */
    float: left;
    text-align: center;
}
.main .Body .Body_Title .a2 a {
    color: #bbbbbb;
    text-decoration: none;
    font-size: 20px;
}
.main .Body .Body_Title .a2 a:hover {
    color: #ff8500;
}
.main .Body .Form {
    width: 360px;
    height: 335.38px;
    /* background-color: #fff; */
    margin-left: 24px;
    /* margin-right: 34.81px; */
    margin-top: 40px;
    margin-bottom: 0;
    float: left;
}
.main .Body .Form .From_Username {
    width: 354px;
    height: 60px;
    /* background-color: #fff; */
}
.main .Body .Form .From_Username .Logo {
    width: 60px;
    height: 60px;
    background-color: rgb(0, 0, 0, 0.3);;
    background-image: url(@img/登录.png);
    background-size: 30px 30px;
    background-repeat: no-repeat;
    background-position: center;
    border-radius: 7px;
    float: left;
}
.main .Body .Form .From_Username .Text {
    width: 294px;
    height: 60px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Body .Form .From_Username .Text:hover {
    caret-color: #ff8500;
}
.main .Body .Form .Form_Password {
    width: 354px;
    height: 60px;
    margin-top: 40px;
    /* background-color: #fff; */
}
.main .Body .Form .Form_Password .Logo1 {
    width: 60px;
    height: 60px;
    background-color: rgb(0, 0, 0, 0.3);;
    background-image: url(@img/密码.png);
    background-size: 30px 30px;
    background-repeat: no-repeat;
    background-position: center;
    border-radius: 7px;
    float: left;
}
.main .Body .Form .Form_Password .Password {
    width: 294px;
    height: 60px;
    font-size: 17px;
    background-color: rgb(0, 0, 0, 0.3);
    color: #ff8500;
    border: none;
    border-radius: 7px;
    float: left;
}
.main .Body .Form .Form_Password .Password:hover {
    caret-color: #ff8500;
}
.main .Body .Form .Form_Login {
    width: 356px;
    height: 60px;
    margin-top: 40px;
    /* background-color: #fff; */
}
.main .Body .Form .Form_Login .Login {
    width: 356px;
    height: 60px;
    background-color: #ff8500;
    color: #fcfcfc;
    font-size: 18px;
    border: 0;
    border-radius: 7px;
}
.main .Body .Form .Form_Login .Login:hover {
    background-color: rgb(255, 153, 18);
}
.main .Body .Form .Form_Register {
    width: 356px;
    height: 60px;
    margin-top: 20px;
}
.main .Body .Form .Form_Register .Register {
    width: 356px;
    height: 60px;
    background-color: #ff8500;
    color: #fcfcfc;
    font-size: 18px;
    border: 0;
    border-radius: 7px;
}
.main .Body .Form .Form_Register .Register:hover {
    background-color: rgb(255, 153, 18);
}
.main .Body .Form .Form_End {
    width: 356px;
    height: 36.71px;
    /* background-color: #fff; */
    margin-top: 10px;
}
.main .Body .Form .Form_End .Forget {
    width: 85px;
    height: 36.71px;
    /* background-color: pink; */
    float: left;
    line-height: 36.71px;
    text-align: center;
}
.main .Body .Form .Form_End .Forget a {
    font-size: 17px;
    font-weight: 200;
    color: #ff8500;
    text-decoration: none;
}
.main .Body .Form .Form_End .Forget a:hover {
    color: #bbbbbb;
}
.main .Body .Form .Form_End .Out {
    width: 121.71px;
    height: 36.71px;
    /* background-color: pink; */
    float: right;
}
.main .Body .Form .Form_End .Out .Out_Logo {
    width: 36.71px;
    height: 36.71px;
    background-image: url(@img/退出登录.png);
    background-size: 25px 25px;
    background-position: center;
    background-repeat: no-repeat;
    float: left;
}
.main .Body .Form .Form_End .Out .Out_Doc {
    width: 85px;
    height: 36.71px;
    line-height: 36.71px;
    text-align: center;
    float: left;
}
.main .Body .Form .Form_End .Out .Out_Doc a {
    font-size: 17px;
    font-weight: 200;
    color: #ff8500;
    text-decoration: none;
}
.main .Body .Form .Form_End .Out .Out_Doc a:hover {
    color: #bbbbbb;
}
.main .Bottom {
    width: 100%;
    height: 30px;
    line-height: 30px;
    font-size: 15px;
    font-weight: 200;
    background-color: rgb(0, 0, 0, 0);
    color: #bbbbbb;
    text-align: center;
    /* background-color: #fff; */
    position: fixed;
    bottom: 0;
}

</style>