<script setup lang="ts">
  defineProps<{
    inputDevice: MediaDeviceInfo | undefined
    isRecording: boolean
    isReady: boolean
    userCount: number
  }>()
</script>

<template>
  <ul class="list">
    <li class="list-element">
      <span>Nutzer</span>
      <span>{{ userCount }}</span>
    </li>
    <li class="list-element state">
      <span>Status</span>
      <span v-if="isReady" class="success">Ready</span>
      <span v-else-if="isRecording" class="warning">Recording...</span>
      <span v-else class="danger">Not Ready</span>
    </li>
  </ul>
</template>

<style scoped>
  .warning {
    background-color: hsl(40, 100%, 50%);
  }

  .success {
    background-color: hsl(120, 100%, 35%);
  }

  .list {
    width: 100%;
    list-style: none;
    padding: 0;
  }

  .list-element {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .list-element.state {
    font-size: 2.2rem;
  }
</style>
