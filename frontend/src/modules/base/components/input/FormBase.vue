<template>
  <form v-bind="$attrs">
    <slot />
    <ButtonGroup>
      <slot name="actions" />
    </ButtonGroup>
  </form>
</template>

<script lang="ts" setup>
  import ButtonGroup from '../ButtonGroup.vue'
</script>

<style scoped>
  form {
    display: flex;
    flex-flow: column;
    row-gap: 0.75rem;
    width: 100%;
  }
</style>
