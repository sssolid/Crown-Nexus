<!-- src/components/popovers/BasePopover.vue -->
<template>
  <v-menu
    v-model="isOpen"
    :location="location"
    :close-on-content-click="closeOnContentClick"
    :offset="offset"
    :open-delay="openDelay"
    :close-delay="closeDelay"
    :open-on-click="openOnClick"
    :open-on-hover="openOnHover"
    :open-on-focus="openOnFocus"
    :return-value="returnValue"
    :transition="transition"
    :content-class="contentClass"
    :theme="theme"
    :z-index="zIndex"
    :disabled="disabled"
    v-bind="$attrs"
    @update:model-value="onOpenChange"
  >
    <template v-slot:activator="slotProps">
      <slot name="activator" v-bind="slotProps"></slot>
    </template>

    <v-card
      :elevation="cardElevation"
      :max-width="maxWidth"
      :min-width="minWidth"
      :max-height="maxHeight"
      :width="width"
      :rounded="rounded"
      class="popover-card"
    >
      <v-card-title v-if="$slots.title || title" class="popover-title">
        <slot name="title">{{ title }}</slot>
      </v-card-title>

      <v-divider v-if="($slots.title || title) && showDivider"></v-divider>

      <v-card-text :class="contentTextClass">
        <slot></slot>
      </v-card-text>

      <v-divider v-if="$slots.actions && showDivider"></v-divider>

      <v-card-actions v-if="$slots.actions" class="popover-actions">
        <slot name="actions"></slot>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
  location: {
    type: String,
    default: 'bottom',
  },
  closeOnContentClick: {
    type: Boolean,
    default: true,
  },
  offset: {
    type: [Number, String, Array],
    default: 5,
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
    default: true,
  },
  openOnHover: {
    type: Boolean,
    default: false,
  },
  openOnFocus: {
    type: Boolean,
    default: false,
  },
  returnValue: {
    type: null,
    default: undefined,
  },
  maxWidth: {
    type: [Number, String],
    default: 'auto',
  },
  minWidth: {
    type: [Number, String],
    default: undefined,
  },
  maxHeight: {
    type: [Number, String],
    default: 'auto',
  },
  width: {
    type: [Number, String],
    default: undefined,
  },
  transition: {
    type: String,
    default: 'scale-transition',
  },
  contentClass: {
    type: String,
    default: '',
  },
  contentTextClass: {
    type: String,
    default: '',
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
  cardElevation: {
    type: [Number, String],
    default: 4,
  },
  rounded: {
    type: [Boolean, String, Number],
    default: 'sm',
  },
  showDivider: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'open', 'close'])

const isOpen = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  isOpen.value = newVal
})

watch(isOpen, (newVal) => {
  emit('update:modelValue', newVal)
})

const onOpenChange = (val: boolean) => {
  if (val) {
    emit('open')
  } else {
    emit('close')
  }
}

// Expose methods to parent component
defineExpose({
  open: () => {
    isOpen.value = true
  },
  close: () => {
    isOpen.value = false
  },
  toggle: () => {
    isOpen.value = !isOpen.value
  },
})
</script>

<style scoped>
.popover-card {
  overflow: hidden;
}

.popover-title {
  padding: 12px 16px;
  font-size: 1rem;
}

.popover-actions {
  padding: 8px 16px;
}
</style>
