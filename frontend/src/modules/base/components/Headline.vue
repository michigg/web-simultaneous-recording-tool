<template>
  <h1 class="text-3xl" data-test="headline">
    {{ title }}
  </h1>
</template>

<script lang="ts" setup>
  defineProps<{ title: string }>()
</script>
