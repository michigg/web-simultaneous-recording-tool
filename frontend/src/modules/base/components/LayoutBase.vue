<template>
  <div class="flex flex-col items-center" data-test="page">
    <Headline v-if="title" :title="title" />
    <CustomSection>
      <IndicatorMode />
    </CustomSection>
    <slot />
  </div>
</template>

<script lang="ts" setup>
  import Headline from './Headline.vue'
  import CustomSection from './CustomSection.vue'
  import IndicatorMode from './IndicatorMode.vue'

  withDefaults(
    defineProps<{
      title?: string
    }>(),
    {
      title: '',
    }
  )
</script>
<style scoped>
  div {
    margin-top: 1rem;
  }
</style>
