<template>
      <div class="welcome text-h1 text-weight-bolder">{{ text }}</div>
</template>
  
<script setup name="AppHome">
  import { ref } from 'vue'
  
  let text = ref('Welcome! ^_^')
</script>

<style>
  .welcome {
    width: 100%;
    height: 300px;
    background-color: #b30000;
    float: left;
    left: 0;
    margin-top: 200px;
    color: bisque;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>