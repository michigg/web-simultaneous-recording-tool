<template>
  <RouterView />
</template>

<style>
  body,
  #app {
    width: 100vw;
    height: 100vh;
    margin: 0;
    position: relative;
    background-color: hsl(var(--hue), 15%, 95%);
    box-sizing: content-box !important;
    display: flex;
    flex-flow: column;
    font-size: 16px;
    text-align: center;
    color: #2c3e50;
  }
</style>
