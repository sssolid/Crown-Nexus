<!-- src/components/base/BaseButton.vue -->
<template>
  <v-btn
    :color="color"
    :variant="variant"
    :size="size"
    :block="block"
    :disabled="disabled"
    :loading="loading"
    :icon="icon"
    :to="to"
    :href="href"
    :target="href ? '_blank' : undefined"
    :class="[roundedClass, elevationClass, customClass]"
    @click="$emit('click', $event)"
  >
    <slot name="prepend"></slot>
    <slot></slot>
    <slot name="append"></slot>
  </v-btn>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  color: {
    type: String,
    default: 'primary',
  },
  variant: {
    type: String,
    default: 'elevated',
    validator: (value: string) =>
      ['text', 'flat', 'elevated', 'tonal', 'outlined', 'plain'].includes(value),
  },
  size: {
    type: String,
    default: 'default',
    validator: (value: string) =>
      ['x-small', 'small', 'default', 'large', 'x-large'].includes(value),
  },
  rounded: {
    type: [String, Boolean],
    default: 'sm',
  },
  elevation: {
    type: [String, Number],
    default: undefined,
  },
  block: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: '',
  },
  to: {
    type: [String, Object],
    default: undefined,
  },
  href: {
    type: String,
    default: '',
  },
  customClass: {
    type: String,
    default: '',
  },
})

defineEmits(['click'])

const roundedClass = computed(() => {
  if (typeof props.rounded === 'boolean') {
    return props.rounded ? 'rounded' : ''
  }
  return `rounded-${props.rounded}`
})

const elevationClass = computed(() => {
  if (props.elevation !== undefined) {
    return `elevation-${props.elevation}`
  }
  return ''
})
</script>
