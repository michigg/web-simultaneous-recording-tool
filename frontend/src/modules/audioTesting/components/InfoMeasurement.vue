<script lang="ts" setup>
  import { Results } from '../models/Results'

  // eslint-disable-next-line no-undef
  defineProps<{ results: Results }>()
</script>

<template>
  <p v-if="results.fileNames.length === 0">Currently no records found!</p>
  <div v-else>
    <p>The last analysis was {{ results.analysisTitle }}</p>
    <p>Count: {{ results.fileNames.length }}</p>
    <ul>
      <li v-for="fileName in results.fileNames" :key="fileName">
        {{ fileName }}
      </li>
    </ul>
  </div>
</template>
<style scoped>
  ul {
    display: flex;
    flex-flow: column;
    justify-content: start;
    align-items: start;
    padding: 0;
  }

  li {
    list-style: none;
    word-break: break-word;
    white-space: break-spaces;
  }
</style>
