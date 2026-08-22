<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { ApiError } from '@/api/http.js'
import { useAuthStore } from '@/stores/auth.js'

const auth = useAuthStore()
const router = useRouter()

const formTitle = ref('注销账户')
const message = ref('')
const password = ref('')
const checkPassword = ref('')
const confirmed = ref(false)
const submitting = ref(false)

const isLogin = computed(() => auth.isAuthenticated)
const username = computed(() => auth.username)

async function deleteAccount () {

    if (!isLogin.value) {
        message.value = '请先登录'
        return
    }
    if (password.value === '' || checkPassword.value === '') {
        message.value = '请填写完整信息'
        return
    }
    if (password.value !== checkPassword.value) {
        message.value = '两次密码不一致'
        return
    }
    if (!confirmed.value) {
        message.value = '请勾选确认，注销后账号无法恢复'
        return
    }

    message.value = ''
    submitting.value = true
    try {
        // 只能注销自己的账号，后端会校验密码；旧版本的「超级密码」是硬编码在
        // 源码里的，任何人拿到都能删别人的号，已经移除。
        await auth.deleteAccount({ password: password.value })
        router.push('/')
    } catch (error) {
        message.value = error instanceof ApiError ? error.message : '注销失败，请稍后重试'
        if (!(error instanceof ApiError)) console.error(error)
    } finally {
        submitting.value = false
    }
}

</script>

<template>
    <div id="main">
        <div id="title">
            {{formTitle}}
        </div>
        <form>
            <div id="username">
                <label for="username">当前账号</label>
                <input :value="username" type="text" disabled />
            </div>
            <div id="password">
                <label for="password">密码</label>
                <input v-model="password" type="password" placeholder="密码" />
            </div>
            <div id="checkPassword">
                <label for="checkPassword">确认密码</label>
                <input v-model="checkPassword" type="password" placeholder="确认密码" />
            </div>
            <div id="confirm">
                <label for="confirm">
                    <input v-model="confirmed" id="confirm" type="checkbox" />
                    我确认注销，账号和数据将无法恢复
                </label>
            </div>
            <input v-on:click="deleteAccount" :disabled="submitting" type="button" :value="submitting ? '注销中…' : '注销账户'" />
            {{message}}
        </form>
    </div>
</template>

<style scoped>

#main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 400px;
    width: 300px;
    background-color: rgb(140, 140, 140);
}

#title {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 50px;
    height: 50px;
    width: 100%;
    background-color: rgb(113, 113, 113);
}

form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 200px;
    width: 100%;
    background-color: rgb(113, 113, 113);
}
</style>