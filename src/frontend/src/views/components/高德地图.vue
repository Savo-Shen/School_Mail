<script setup>

import { ref } from 'vue';

import AMapLoader from '@amap/amap-jsapi-loader';

AMapLoader.load({
    "key": "5b0397673260ef3a7599c7f8eafb0687",          // 申请好的Web端开发者Key，首次调用 load 时必填
    "version": "1.4.15",                                // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
    "plugins": [],                                      // 需要使用的的插件列表，如比例尺'AMap.Scale'等
    "AMapUI": {                                         // 是否加载 AMapUI，缺省不加载
        "version": '1.1',                               // AMapUI 缺省 1.1
        "plugins":[
            // 'AMap.ToolBar',
        ]                            // 需要加载的 AMapUI ui插件
    },
    "Loca":{                                            // 是否加载 Loca， 缺省不加载
        "version": '1.3.2'                              // Loca 版本，缺省 1.3.2
    },
}).then((AMap)=>{
    var map = new AMap.Map('container', {
        zoom:15.4,                                        //级别
        center: [119.16907656193156, 26.065216708718417],                 //中心点坐标        
    });
    map.addControl(new AMap.ToolBar());
    map.addControl(new AMap.Driving())
}).catch(e => {
    console.log(e);
})

</script>

<template>

<div></div>
<div id="main">

    <div id="title">
        <h1>我们在这</h1>
    </div>
    <div id="container"></div>

</div>  

</template>

<style scoped>

#main {
    height: 800px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
}

#title {
    margin-top: -50px;
    margin-bottom: 60px;
}

#title h1 {
    color: #333;
    font-size: 40px;
    font-family: PingFangSC-Regular;
}

#container {
    height: 500px;
    width: min(600px, 100%);
    border-radius: 10px;
}

</style>