<script setup>

import { ref } from 'vue'

import router from '@/router'

import { useIntersectionObserver } from '@vueuse/core'

const Main = ref(null)
const Value = ref(null)

// const { stop }= useIntersectionObserver(
  
//     Main,
//     ([{ isIntersecting }], observerElement) => {
//         if (isIntersecting) {
//             Main.value.classList.add('animate__animated', 'animate__fadeIn')
//             Value.value.classList.add('animate__animated', 'animate__fadeInUp')
//         }
//     },
//     {
//         threshold: 0,
//     },
// )

</script>

<template>
<div></div>
<div id="main" ref="Main">
    <div class="_all" ref="Value"> 
        <div class="_Computer"></div>
        <div class="_GetIn">
            <a>Computer Engineering</a>
        </div>
        <div class="_GetIn1">
            <a>Around The World</a>
        </div>
        <div class="_Auto">
            <div class="_Know">
                <a>了解更多</a>
            </div>
            <div class="_Community">
                <a @click="">进入社区</a>
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
#main {
    min-height: 600px;
    width: 100%;
    background-image: url(@img/IT2.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
}
._all {
    width: 100%;
    min-height: 1000px;
    /* background-color: pink; */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

._all ._Computer {
    width: 100px;
    height: 100px;
    margin-top: 100px;
    margin-bottom: 0;
    margin-left: auto;
    margin-right: auto;
    background-image: url(@img/computer.png);
    background-size: 70px 70px;
    background-repeat: no-repeat;
    background-position: center;
    /* background-color: green; */
}
._all ._Computer img {
    max-width: 70px;
    max-height: 70px;
}
._all ._GetIn {
    width: min(600px, 100%);
    height: 80px;
    font-size: 45px;
    line-height: 80px;
    margin: 0 auto;
    text-align: center;
    /* background-color: green; */
}
._all ._GetIn a {
    color: black;
    text-decoration: none;
    /* user-select: none; */
}
._all ._GetIn a:hover {
    background-color: rgb(0, 0, 0, 0);
}
._all ._GetIn1 {
    width: min(600px, 100%);
    height: 80px;
    font-size: 45px;
    line-height: 80px;
    margin: 0 auto;
    text-align: center;
    /* background-color: green; */
}
._all ._GetIn1 a {
    color: black;
    text-decoration: none;
    /* user-select: none; */
}
._all ._GetIn1 a:hover {
    background-color: rgb(0, 0, 0, 0);
}
._all ._Auto {
    /* width: min(450px, 100%); */
    height: 40px;
    margin-top: 50px;
    margin-bottom: 0;
    margin-left: auto;
    margin-right: auto;
    /* background-color: green; */
}
._all ._Auto ._Know {
    width: 50%;
    height: 40px;
    line-height: 40px;
    border-radius: 36px 0 0 36px;
    /* background-color: rgb(0, 0, 0, 0.7); */
    text-align: center;
    float: left;
}
/* ._all ._Auto ._Know:hover {
    background-color: rgb(255, 255, 255, 0.7);
} */
._all ._Auto ._Know a {
    
    padding: 8px 72px 8px 72px;
    height: 40px;
    font-size: 20px;
    border-radius: 36px 0 0 36px;
    background-color: rgb(0, 0, 0, 0.7);
    text-decoration: none;
    color: #fcfcfc;
    user-select: none;
    cursor: pointer;
}
._all ._Auto ._Know a:hover {
    color: black;
    background-color: rgb(255, 255, 255, 0.7);
}
._all ._Auto ._Community {
    width: 50%;
    height: 40px;
    line-height: 40px;
    border-radius: 0 36px 36px 0;
    /* background-color: rgb(128, 128, 128, 0.7); */
    text-align: center;
    float: right;
    cursor: pointer;
}
/* ._all ._Auto ._Community:hover {
    background-color: rgb(0, 0, 0, 0.7);
} */
._all ._Auto ._Community a {
    padding: 8px 72px 8px 72px;
    height: 40px;
    font-size: 20px;
    border-radius: 0 36px 36px 0;
    background-color: rgb(255, 255, 255, 0.7);
    text-decoration: none;
    color: black;
    user-select: none;
}
._all ._Auto ._Community a:hover{
    background-color: rgb(0, 0, 0, 0.7);
    color: #fcfcfc;
}

</style>