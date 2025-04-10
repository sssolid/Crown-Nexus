<!-- src/components/base/BaseIcon.vue -->
<template>
  <v-icon
    :icon="icon"
    :color="color"
    :size="size"
    :class="customClass"
    v-bind="$attrs"
  ></v-icon>
</template>

<script setup lang="ts">
defineProps({
  icon: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: undefined,
  },
  size: {
    type: [String, Number],
    default: undefined,
  },
  customClass: {
    type: String,
    default: '',
  },
})
</script>
