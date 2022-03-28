<template>
  <LayoutBase v-bind="$attrs" class="content">
    <slot />
  </LayoutBase>
</template>

<script lang="ts" setup>
  import LayoutBase from './LayoutBase.vue'
</script>

<style>
  .content {
    display: flex;
    flex-flow: column;
    align-items: center;
    gap: 1.75rem;
  }
</style>
