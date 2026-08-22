<script setup>

import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const isLogin = computed(() => auth.isAuthenticated)

function login() {
    router.push('/login')
}

async function logout(){
    await auth.logout()
    router.push('/')
}
</script>

<template>
 <div class="_all">
    <div class="_title">
      <div class="_title1">
          <div class="_logo"></div>
          <div class="_navigation">
              <a href="#">专业概况</a>
              <a href="#">关于我们</a>
              <a href="#">班级荣誉</a>
              <a href="#">团日活动</a>
              <a href="#">学生风采</a>
              <a href="#">社区互动</a>
              <a href="#">共创营地</a>
          </div>
          <div class="_logo_landing"></div>
          <div v-if="!isLogin" class="_landing">
              <a @click="login">欢迎登录</a>
          </div>
          <input v-if="isLogin" type="button" @click="logout" value="退出登录" />
      </div>
  </div>
 </div>
</template>

<style scoped>

._all ._title {
    width: 100%;
    height: 67.35px;
    /* border-top:5px solid black; */
    /* border-bottom: 3px solid #edeef0; */
    background-color: rgb(0, 0, 0, 0.3);
}
._all ._title ._title1 {
    width: 1300px;
    height: 67.35px;
    /* background-color: aqua; */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
    /* float: left; */
} 
._all ._title ._title1 ._logo {
    width: 60px;
    height: 67.35px;
    margin-right: 80px;
    line-height: 67.35px;
    color: #fcfcfc;
    /* background-color: blue; */
    background-image: url(@img/IDEC_CE_Logo.png);
    background-size: 67px 67px;
    background-position: center;
    background-repeat: no-repeat;
    float: left;
    cursor: pointer;
}
._all ._title ._title1 ._navigation {
    width: 900px;
    height: 67.35px;
    line-height: 67.35px;
    margin-right: 70px;
    /* background-color: pink; */
    float: left;
}
._all ._title ._title1 ._navigation a {
    font-size: 18px;
    height: 67.35px;
    padding: 0 20px;
    color: #fcfcfc;
    text-decoration: none;
    display: inline-block;
}
._all ._title ._title1 ._navigation a:hover {
    background-color: #eee;
    color: black;
}
._all ._title ._title1 ._logo_landing {
    width: 68.28px;
    height: 67.35px;
    background-image: url(@icons/Login1.png);
    background-size: 36px 36px;
    background-position: center;
    background-repeat: no-repeat;
    float: left;
}
._all ._title ._title1 ._landing {
    width: 120px;
    height: 67.35px;
    line-height: 67.35px;
    float: right;
    cursor: pointer;
}
._all ._title ._title1 ._landing a {
    font-size: 18px;
    height: 67.35px;
    padding: 0 20px;
    color: #fcfcfc;
    /* background-color: blue; */
    text-decoration: none;
    user-select: none;
    display: inline-block;
}
._all ._title ._title1 ._landing a:hover {
    background-color: #eee;
    color: black;
}


</style>