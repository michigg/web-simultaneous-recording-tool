<template>
  <section class="base-section">
    <slot />
  </section>
</template>

<style scoped>
  .base-section {
    display: flex;
    flex-flow: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 100%;
    max-width: 500px;
    gap: 0.75rem;
    padding: 1rem 2rem;
    background-color: hsl(var(--hue), 70%, 90%);
    text-align: left;
  }
</style>
