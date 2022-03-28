<template>
  <div class="input-group">
    <select :id="id" v-model="localValue" v-bind="$attrs">
      <option
        v-for="option in localOptions"
        :key="option.title || option"
        :value="option.value || option"
      >
        {{ option.title || option }}
      </option>
    </select>
    <label :for="id">{{ label }}</label>
  </div>
</template>
<script lang="ts" setup>
  import { computed } from 'vue'

  // eslint-disable-next-line no-undef
  const props = defineProps<{
    modelValue?: string | number | undefined
    id: string
    options: Array<string> | Array<{ title: string }>
    label: string
  }>()

  const localOptions = computed(() => {
    if (typeof props.options[0] === 'string') {
      return props.options
    } else {
      return (props.options as Array<{ title: string }>).map((option) => ({
        title: option.title,
        value: option,
      }))
    }
  })
  const emit = defineEmits<{
    (e: 'update:modelValue', value: string | number | undefined): void
  }>()
  const localValue = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value),
  })
</script>

<style scoped>
  .input-group {
    display: flex;
    flex-flow: column;
    row-gap: 0.1rem;
  }

  select {
    padding: 0.5rem 0.5rem;
    outline: none;
    width: 100%;
    height: 41px;
    border: none;
    border-radius: 0.5rem;
    border-bottom: solid 3px hsl(var(--hue) 30% 20%);
    background-color: #fff;
  }

  label {
    font-size: 0.75rem;
    padding-left: 0.5rem;
  }

  select:focus-visible,
  select:focus {
    border-bottom: solid 3px var(--color-focus);
  }

  select:invalid {
    border-bottom: solid 3px var(--color-danger);
  }
</style>
