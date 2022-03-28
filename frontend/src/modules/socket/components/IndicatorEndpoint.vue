<script lang="ts" setup>
  const socketUrl = import.meta.env.VITE_SOCKET_URL
</script>

<template>
  <p>Data will be send to {{ socketUrl }}.</p>
</template>
