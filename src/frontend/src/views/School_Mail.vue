<script setup>

import { ref } from 'vue'
import { homePageComponentsList } from '@/views/components/index.js'

import router from '@/router/index.js'

import Header_skip from './components/header/Header_skip.vue';
import Footer from '@/views/components/Footer.vue'

const isOpen = ref(0)

</script>

<template>

  <div id="app">
    
    <Header_skip @cd_page="(value) => isOpen = value"></Header_skip>
    
    <div v-for="components in homePageComponentsList">
      <div v-if="isOpen === components.id" v-for="component in components.components">
        <component :is="component"></component>
      </div>
    </div>
    
    <Footer></Footer>

  </div>

</template>

<!-- style 加上scoped标签，只会影响当前组件的css -->
<style scoped>

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  /* max-width: 1905px; */
  /* min-height: 800px; */
  background-color: black;
}

</style>