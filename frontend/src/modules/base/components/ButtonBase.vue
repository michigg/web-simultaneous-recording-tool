<template>
  <button v-bind="$attrs">
    <slot />
  </button>
</template>

<style scoped>
  button {
    background-color: hsl(var(--hue), 100%, 50%);
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    flex-grow: 1;
    cursor: pointer;
    transition: box-shadow 150ms ease-out;
    color: var(--color-text-button);
    font-weight: bold;
  }

  button:hover {
    box-shadow: inset 0.25rem 0.25rem 0.5rem hsl(var(--hue), 100%, 20%);
  }
</style>
