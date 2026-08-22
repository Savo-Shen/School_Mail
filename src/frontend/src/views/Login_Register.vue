<script setup>

import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { ApiError } from '@/api/http.js'
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const isActive = ref(false)

const loginUsername = ref('')
const loginPassword = ref('')
const loginMessage = ref("")

const registerUsername = ref('')
const registerPassword = ref('')
const registerEmail = ref('')
const registerMessage = ref("")

const isLoginUsernameError = ref(false)
const isLoginPasswordError = ref(false)
const isRegisterUsernameError = ref(false)
const isRegisterPasswordError = ref(false)
const isRegisterEmailError = ref(false)

const styleVar = ref({
	/* COLORS */
	/* 强制规定颜色代码 */
	"--white": "#e9e9e9",
	"--gray": "#333",
	// "--blue": "#0367a6",
	"--lightblue": "#008997",
	"--orange": "#ff8500",

	/* RADII */
	"--button-radius": "0.7rem",

	/* SIZES */
	"--max-width": "758px",
	"--max-height": "420px",
})

function goHome() {
	router.push('/')
}

function resetLoginErrors() {
	isLoginUsernameError.value = false
	isLoginPasswordError.value = false
}

function resetRegisterErrors() {
	isRegisterUsernameError.value = false
	isRegisterPasswordError.value = false
	isRegisterEmailError.value = false
}

async function login() {

	resetLoginErrors()

	if (loginUsername.value === '') {
		loginMessage.value = "请填写用户名"
		isLoginUsernameError.value = true
		return
	}
	if (loginPassword.value === '') {
		loginMessage.value = '请填写密码'
		isLoginPasswordError.value = true
		return
	}

	loginMessage.value = ''

	try {
		await auth.login({
			username: loginUsername.value,
			password: loginPassword.value,
		})
		// 支持被守卫拦下来时记录的返回地址
		const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
		router.push(redirect)
	} catch (error) {
		if (error instanceof ApiError) {
			loginMessage.value = error.message
			// 账号密码错误时两个输入框一起标红
			if (error.status === 401) {
				isLoginUsernameError.value = true
				isLoginPasswordError.value = true
			}
			isLoginUsernameError.value = isLoginUsernameError.value || Boolean(error.fieldError('username'))
			isLoginPasswordError.value = isLoginPasswordError.value || Boolean(error.fieldError('password'))
		} else {
			loginMessage.value = '登录失败，请稍后重试'
			console.error(error)
		}
	}
}

async function register () {

	resetRegisterErrors()

	if (registerUsername.value === '') {
		registerMessage.value = '请填写用户名'
		isRegisterUsernameError.value = true
		return
	}
	if (registerPassword.value === '') {
		registerMessage.value = '请填写密码'
		isRegisterPasswordError.value = true
		return
	}
	if (registerEmail.value === '') {
		registerMessage.value = '请填写邮箱'
		isRegisterEmailError.value = true
		return
	}

	registerMessage.value = ''

	try {
		await auth.register({
			username: registerUsername.value,
			password: registerPassword.value,
			email: registerEmail.value,
		})
		// 注册成功后直接登录，省掉再输一次账号密码
		await auth.login({
			username: registerUsername.value,
			password: registerPassword.value,
		})
		router.push('/')
	} catch (error) {
		if (error instanceof ApiError) {
			registerMessage.value = error.message
			isRegisterUsernameError.value = Boolean(error.fieldError('username'))
			isRegisterPasswordError.value = Boolean(error.fieldError('password'))
			isRegisterEmailError.value = Boolean(error.fieldError('email'))
		} else {
			registerMessage.value = '注册失败，请稍后重试'
			console.error(error)
		}
	}
}

function forget() {
	loginMessage.value = '找回密码功能还没做，请联系管理员重置'
}

</script>   


<template>
<div id="main" :style=styleVar>

	<div class="logo">
		<img @click="goHome" src="@img/IDEC_CE_Logo_With_Name.png" alt="logo">
	</div>

	<div class="container" :class="{ rightPanelActive: isActive}">

		<div class="container__form container--signup">
			<div class="form" id="form1">
				<h2 class="form__title">注册</h2>
				<input v-model="registerUsername" type="text" placeholder="用户名" class="input" :class="{'input_error': isRegisterUsernameError}" name="注册用户名"/>				
				<input v-model="registerPassword" type="password" placeholder="密码" class="input" :class="{'input_error': isRegisterPasswordError}" name="注册密码"/>
				<input v-model="registerEmail" @keyup.enter="register" type="email" placeholder="邮箱" class="input" :class="{'input_error': isRegisterEmailError}" name="注册邮箱"/>
				<div class="message">
					{{registerMessage}}
				</div>
				<button @click="register" :disabled="auth.loading" class="btn">{{ auth.loading ? '注册中…' : '注册' }}</button>
			</div>
		</div>
		
		<div class="container__form container--signin">
			<div class="form" id="form2">
				<h2 class="form__title">登录</h2>
				<input v-model="loginUsername" @keyup.enter="login" type="text" placeholder="用户名" class="input" :class="{'input_error': isLoginUsernameError}" name="登录用户名"/>
				<input v-model="loginPassword" @keyup.enter="login" type="password" placeholder="密码" class="input" :class="{'input_error': isLoginPasswordError}" name="登录密码"/>
				<div class="message">
					{{loginMessage}}
				</div>
				<a @click.prevent="forget" href="#" class="link">忘记密码?</a>
				<button @click="login" :disabled="auth.loading" class="btn">{{ auth.loading ? '登录中…' : '登录' }}</button>
			</div>
		</div>
		
		<div class="container__overlay">
			<div class="overlay">
				<div class="overlay__panel overlay--left">
					<button @click="isActive=false" class="btn" id="signIn">登录</button>
				</div>
				<div class="overlay__panel overlay--right">
					<button @click="isActive=true" class="btn" id="signUp">注册</button>
				</div>
			</div>
		</div>
	</div>
</div>

</template>

<style scoped>
#main {
	display: flex;
	justify-content: center;
	flex-direction: column;
	align-items: center;
	background-color: var(--white);
	background: url("@img/bg/background_Login.jpg");
	background-attachment: fixed;
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	height: 100vh;
	font-size: 16px;
	height: 100%;
	width: 100%;
	min-width: 1200px;
	/* max-width: 1905px; */
	min-height: 800px;
	place-items: center;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
		Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.logo {
	height: 120px;
	margin-top: -140px;
	margin-bottom: 20px;
	
}

.logo img {
	height: 100%;
	object-fit: contain;
	cursor: pointer;
}

.form__title {
	font-weight: 300;
	margin: 0;
	margin-bottom: 1.25rem;
	color: var(--gray);
}

.link {
	color: var(--gray);
	font-size: 0.9rem;
	margin: 1.5rem 0;
	text-decoration: none;
}

.container {
	background-color: var(--white);
	border-radius: var(--button-radius);
	box-shadow: 0 0.9rem 1.7rem rgba(0, 0, 0, 0.25),
		0 0.7rem 0.7rem rgba(0, 0, 0, 0.22);
	height: var(--max-height);
	max-width: var(--max-width);
	overflow: hidden;
	position: relative;
	width: 100%;
}

.container__form {
	height: 100%;
	position: absolute;
	top: 0;
	transition: all 0.6s ease-in-out;
}

.container--signin {
	left: 0;
	width: 50%;
	z-index: 2;
}

.container--signin .link:hover {
    color: var(--orange);
}

.container.rightPanelActive .container--signin {
	transform: translateX(100%);
}

.container--signup {
	left: 0;
	opacity: 0;
	width: 50%;
	z-index: 1;
}

.container.rightPanelActive .container--signup {
	-webkit-animation: show 0.6s;
	        animation: show 0.6s;
	opacity: 1;
	transform: translateX(100%);
	z-index: 5;
}

.container__overlay {
	height: 100%;
	left: 50%;
	overflow: hidden;
	position: absolute;
	top: 0;
	transition: transform 0.6s ease-in-out;
	width: 50%;
	z-index: 100;
}

.container.rightPanelActive .container__overlay {
	transform: translateX(-100%);
}

.overlay {
	/* background-color: var(--lightblue); */
	background: url("@img/bg/background_Login.jpg");
	opacity: 0.95;
	background-attachment: fixed;
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	height: 100%;
	left: -100%;
	position: relative;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
	width: 200%;
}

.container.rightPanelActive .overlay {
	transform: translateX(50%);
}

.overlay__panel {
	align-items: center;
	display: flex;
	flex-direction: column;
	height: 100%;
	justify-content: center;
	position: absolute;
	text-align: center;
	top: 0;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
	width: 50%;
}

.overlay--left {
	transform: translateX(-20%);
}

.container.rightPanelActive .overlay--left {
	transform: translateX(0);
}

.overlay--right {
	right: 0;
	transform: translateX(0);
}

.container.rightPanelActive .overlay--right {
	transform: translateX(20%);
}

.btn {
	/* background-color: var(--blue); */
    background-color: var(--orange);
	background-image: linear-gradient(90deg, var(--orange) 0%, var(--orange) 74%);
	border-radius: 20px;
	border: 1px solid var(--blue);
	color: var(--white);
	cursor: pointer;
	font-size: 0.8rem;
	font-weight: bold;
	letter-spacing: 0.1rem;
	padding: 0.9rem 4rem;
	text-transform: uppercase;
	transition: transform 80ms ease-in;
}

.form > .btn {
	margin-top: 1.5rem;
}

.btn:active {
	transform: scale(0.95);
}

.btn:focus {
	outline: none;
}

.form {
	background-color: var(--white);
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 3rem;
	height: 100%;
	text-align: center;
}

.message {
	color: var(--gray);
	height: 20px;
}

.input {
	background-color: #fff;
	border: none;
	padding: 0.9rem 0.9rem;
	margin: 0.5rem 0;
	width: 100%;
	border-radius: 20px;
	font-size: 14px;
	outline: none;
}

.input_error {
	border: 1px solid red;
}

@-webkit-keyframes show {
	0%,
	49.99% {
		opacity: 0;
		z-index: 1;
	}

	50%,
	100% {
		opacity: 1;
		z-index: 5;
	}
}

@keyframes show {
	0%,
	49.99% {
		opacity: 0;
		z-index: 1;
	}

	50%,
	100% {
		opacity: 1;
		z-index: 5;
	}
}
</style>