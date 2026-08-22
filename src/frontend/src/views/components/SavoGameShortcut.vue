<script setup>
function goKeepRunning() {
    window.open(import.meta.env.BASE_URL + 'KeepRunning/index.html');
}
</script>

<template>
<div></div>

<div id='main'>
    <div class="body">
        <div class="image">
            <div id="image"></div>
        </div>
        <div class="right">
            <div class="text">
                <div class="title">Keep Running</div>
                <div class="subtitle">Savo的游戏2.0</div>
                <div class="content">作为一名社畜，你已经厌倦了城市中日复一日的工作和一眼望到头的未来，面对这样的生活你现在只想要做的是</div>
                <div class="button" @click="goKeepRunning()">Keep Running</div>
            </div>        
        </div>
    </div>
</div>

</template>

<style scoped>
#main {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    min-width: 1200px;
    height: 600px;
    background-color: rgb(124, 207, 117);
}
.body {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 100%;
    max-width: 1600px;
}

.image {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 50%;
}
#image {
    height: 400px;
    width: 600px;
    border-radius: 60px;
    background-color: blue;
    background-image: url(@img/game/KeepRunning2.png);
    background-position: center;
    background-size: cover;

}
.right {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 50%;
    padding: 50px;
}
.text {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    margin-right: 100px;
}
.title {
    font-size: 50px;
    font-weight: bold;
    margin-bottom: 5px;
    color:rgb(20, 42, 49)
}
.subtitle {
    font-size: 25px;
    margin-bottom: 5px;
    color:#794004;
}
.content {
    font-size: 20px;
    margin-bottom: 5px;
    color:rgb(20, 42, 49)
}
.button {
    font-size: 40px;
    margin-bottom: 5px;
    color:rgb(20, 42, 49);
    border: 1px solid rgb(20, 42, 49);
    border-radius: 30px;
    margin: 50px;
    padding: 30px;
    cursor: pointer;
}
.button:hover {
    background-color: rgb(20, 42, 49);
    color: white;
}
</style>