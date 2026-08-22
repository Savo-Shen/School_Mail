<script setup>

import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { baseColor } from '@/assets/js/color';
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const emit = defineEmits(['cd_page'])
const isOpen = ref(0)

// 登录状态从全局 store 读，不再每个组件各自请求一次接口
const isLogin = computed(() => auth.isAuthenticated)
const username = computed(() => auth.username)

function login() {
    router.push('/login')
}

function register() {
    router.push('/register')
}

function openStudy() {
    router.push('/study')
}

async function logout() {
    await auth.logout()
    // store 是响应式的，界面会自动更新，不需要 router.go(0) 强刷页面
    router.push('/')
}

function openLabel(labelId) {
    isOpen.value = labelId
    emit('cd_page', labelId)
}

</script>

<template>
    <div>
        <div id="main_Logo">
            <div id="main_Logo_img" @click="openLabel(0)"></div>
            <div id="main_Logo_doc">
                <div class="chinese"> 计 算 机 科 学 与 技 术</div>
                <div class="english">Computer Science and Technology of MinJiang University</div>
            </div>
            <div id="main_login">
                <div v-if="isLogin" id="profile">您好，{{username}}</div>
                <div v-if="isLogin" id="logout" @click="logout">退出登录</div>
                <div v-if="!isLogin" id="login" @click="login">登录</div>
                <!-- <div v-if="!isLogin" id="register" @click="register">注册</div> -->
            </div>
        </div>
        <div class="main_Navigation" :style="baseColor">
            <div class="main_Navigation1">
                <div class="Navigation_Logo">
                    <div class="Navigation">
                        <a @click="openLabel(0)" :class="{labelHover: isOpen==0}">首页</a>
                        <a @click="openLabel(1)" :class="{labelHover: isOpen==1}">专业概况</a>
                        <a @click="openLabel(3)" :class="{labelHover: isOpen==3}">班级风光</a>
                        <a @click="openLabel(5)" :class="{labelHover: isOpen==5}">学生风采</a>
                        <!-- <a @click="openLabel(6)" :class="{labelHover: isOpen==6}">社区互动</a> -->
                        <!-- <a @click="openLabel(7)" :class="{labelHover: isOpen==7}">共创营地</a> -->
                        <a @click="openStudy">学习资源</a>
                        <a @click="openLabel(2)" :class="{labelHover: isOpen==2}">关于我们</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/*  Header配色方案1 20230214
background: linear-gradient(to bottom, rgba(255,255,255,0.15) 0%, rgba(0,0,0,0.15) 100%), radial-gradient(at top center, rgba(255,255,255,0.40) 0%, rgba(0,0,0,0.40) 120%) #989898;
 background-blend-mode: multiply,multiply; */

 * {
    margin: 0;
    padding: 0;
}
#main_Logo {
    width: 100%;
    height: 150px;
    background-color: rgba(20, 42, 49);
    position: relative;
    /* 父盒子：让子盒子垂直居中显示 */
    display: flex;
    align-items: center;
    justify-content: space-between;
    
}
#main_Logo_img {
    width: min(600px, 100%);
    height: 120px;
    /* background-color: green; */
    /* margin-top: 15px; */
    /* margin-bottom: auto; */
    /* position: absolute; */
    /* top: 50%; */
    /* margin-top: -60px;
    margin-left: 100px; */
    /* 让盒子垂直居中显示 */
    /* margin-right: 0; */
    background-image: url(@img/IDEC_CE_Logo_With_Name.png);
    background-repeat: no-repeat;
    background-position: center;
    background-size: 240px 120px;
    right: 50px;
    /* float: left; */
    cursor: pointer;
}
#main_Logo_doc {
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /* background-color: green; */
    /* position: absolute; */
    /* top: 50%;
    margin-top: -60px;
    margin-left: 350px; */
    /* float: left; */
}

#main_login {
    /* 原来写死 400px + margin-left:200px，在 flex 布局里会被挤压，
       导致「您好，xxx」折成两行。改成按内容撑开 + gap 控制间距。 */
    height: 40px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-right: 60px;
    flex-shrink: 0;
}

#main_login #profile {
    font-size: 20px;
    color: rgb(200, 200, 200);
    line-height: 40px;
    /* 用户名不折行；过长时省略而不是撑破布局 */
    white-space: nowrap;
    max-width: 220px;
    overflow: hidden;
    text-overflow: ellipsis;
}

#main_login #logout {
    flex-shrink: 0;
    width: 120px;
    height: 40px;
    border: 1px solid rgb(120, 120, 120);
    text-align: center;
    line-height: 40px;
    border-radius: 50px;
    font-size: 20px;
    color: rgb(160, 160, 160);
    cursor: pointer;
}

#main_login #logout:hover {
    background-color: rgb(200, 200, 200);
    color: #000;
}

#main_login #login{
    flex-shrink: 0;
    width: 100px;
    height: 40px;
    border: 1px solid rgb(200, 200, 200);
    text-align: center;
    line-height: 40px;
    border-radius: 50px;
    font-size: 20px;
    color: #fff;
    cursor: pointer;
}

#main_login #login:hover {
    background-color: rgb(200, 200, 200);
    color: #000;
}

#main_login #register {
    width: 80px;
    height: 40px;
    border: 1px solid rgb(200, 200, 200);
    background-color: rgb(200, 200, 200);
    text-align: center;
    line-height: 40px;
    border-radius: 50px;
    font-size: 20px;
    color: #000;
    left:20px;
    margin-left: 20px;
    cursor: pointer;
}

#main_login #register:hover {
    background-color: rgba(20, 42, 49);
    color: #fcfcfc;
}

.chinese {
    width: min(600px, 100%);
    height: 80px;
    /* background-color: pink; */
    font-size: 38px;
    font-weight: 200;
    line-height: 80px;
    text-align: center;
    color: rgb(248, 248, 248);
}
.english {
    width: min(600px, 100%);
    height: 40px;
    /* background-color: #fff; */
    font-size: 20px;
    color: rgb(227, 225, 210);
    text-align: center;
    line-height: 10px;
}
.main_Navigation {
    width: 100%;
    height: 67.35px;
    border-top: 3px solid #cbebf4;
    border-bottom: 2px solid #fdeac9;
    /* background-color:rgb(138, 202, 218); */
    background-color: var(--blue);
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
    /* color: #fcfcfc; */
    text-decoration: none;
    display: inline-block;
    cursor: pointer;
}
.main_Navigation .main_Navigation1 .Navigation a:hover {
    background-color: #eee;
    color: black;
}
.labelHover {
    background-color: #eee;
    color: black;
}

/* ------------------------------------------------------------------ *
 * 响应式
 * 原设计固定 1300px：logo 区独占 600px、导航项 padding 0 40px，
 * 六项加起来约 890px。窄屏下导航会折行，而导航栏高度写死 67.35px，
 * 第二行直接被裁掉。下面按断点收缩，并把写死的高度改成自适应。
 * ------------------------------------------------------------------ */

@media (max-width: 1100px) {
    #main_Logo {
        height: auto;
        padding: 12px 16px;
        gap: 12px;
    }
    #main_Logo_doc {
        /* flex 子项默认 min-width:auto，会被内容（写死 600px 的标题）撑住不肯收缩 */
        min-width: 0;
    }
    #main_Logo_doc .chinese,
    #main_Logo_doc .english {
        /* 原来写死 600px，会把右侧登录区顶出视口 */
        width: 100%;
        max-width: 600px;
        /* 原来是写死的 height + line-height（.english 的 line-height 只有 10px），
           单行勉强能看，一折行就上下重叠 */
        height: auto;
    }
    #main_Logo_doc .chinese {
        line-height: 1.3;
    }
    #main_Logo_doc .english {
        line-height: 1.5;
    }
    #main_Logo_img {
        /* 原来占 600px 只为放一张 240px 的图；flex 下还会被压缩到 0 导致 logo 消失 */
        width: 200px;
        flex: 0 0 200px;
        background-size: contain;
    }
    #main_Logo_doc {
        flex: 1 1 auto;
    }
    #main_login {
        margin-right: 0;
    }
    .main_Navigation .main_Navigation1 .Navigation a {
        padding: 0 20px;
        font-size: 16px;
    }
}

@media (max-width: 820px) {
    /* 导航允许换行，高度改为自适应，否则第二行被裁 */
    .main_Navigation,
    .main_Navigation .main_Navigation1,
    .main_Navigation .main_Navigation1 .Navigation {
        height: auto;
    }
    .main_Navigation .main_Navigation1 .Navigation {
        line-height: normal;
        padding: 4px 0;
    }
    .main_Navigation .main_Navigation1 .Navigation a {
        height: 44px;
        line-height: 44px;
        padding: 0 14px;
        font-size: 15px;
    }
    #main_Logo_img {
        width: 150px;
        flex: 0 0 150px;
    }
    #main_Logo_doc .chinese {
        font-size: 26px;
        letter-spacing: 3px;
    }
    #main_Logo_doc .english {
        font-size: 14px;
    }
}

@media (max-width: 560px) {
    #main_Logo {
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
    }
    #main_Logo_doc .chinese {
        font-size: 18px;
        letter-spacing: 2px;
    }
    #main_Logo_doc .english {
        font-size: 11px;
    }
    #main_login {
        gap: 12px;
    }
    #main_login #login,
    #main_login #logout {
        width: auto;
        padding: 0 14px;
        font-size: 15px;
    }
    #main_login #profile {
        font-size: 15px;
        max-width: 130px;
    }
    .main_Navigation .main_Navigation1 .Navigation a {
        padding: 0 10px;
        font-size: 14px;
    }
}
</style>