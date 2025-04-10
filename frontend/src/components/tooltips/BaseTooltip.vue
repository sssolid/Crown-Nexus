<!-- src/components/tooltips/BaseTooltip.vue -->
<template>
  <v-tooltip
    :text="text"
    :location="location"
    :open-delay="openDelay"
    :close-delay="closeDelay"
    :open-on-click="openOnClick"
    :open-on-hover="openOnHover"
    :open-on-focus="openOnFocus"
    :max-width="maxWidth"
    :min-width="minWidth"
    :content-class="contentClass"
    :transition="transition"
    :theme="theme"
    :z-index="zIndex"
    :disabled="disabled"
    :virtual-element="virtualElement"
    v-bind="$attrs"
  >
    <template v-slot:activator="slotProps">
      <slot name="activator" v-bind="slotProps"></slot>
    </template>

    <slot>
      {{ text }}
    </slot>
  </v-tooltip>
</template>

<script setup lang="ts">
const props = defineProps({
  text: {
    type: String,
    default: '',
  },
  location: {
    type: String,
    default: 'bottom',
  },
  openDelay: {
    type: [Number, String],
    default: 0,
  },
  closeDelay: {
    type: [Number, String],
    default: 0,
  },
  openOnClick: {
    type: Boolean,
    default: false,
  },
  openOnHover: {
    type: Boolean,
    default: true,
  },
  openOnFocus: {
    type: Boolean,
    default: true,
  },
  maxWidth: {
    type: [Number, String],
    default: 300,
  },
  minWidth: {
    type: [Number, String],
    default: undefined,
  },
  contentClass: {
    type: String,
    default: '',
  },
  transition: {
    type: String,
    default: 'scale-transition',
  },
  theme: {
    type: String,
    default: undefined,
  },
  zIndex: {
    type: [Number, String],
    default: undefined,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  virtualElement: {
    type: Object,
    default: undefined,
  },
})
</script>
