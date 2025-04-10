<!-- src/components/accordion/BaseAccordion.vue -->
<template>
  <div class="base-accordion" :class="customClass">
    <v-expansion-panels
      v-model="localPanel"
      :multiple="multiple"
      :mandatory="mandatory"
      :variant="variant"
      :density="density"
      :color="color"
      :readonly="readonly"
      :disabled="disabled"
      :theme="theme"
      :flat="flat"
      :bg-color="bgColor"
      @update:model-value="onPanelChange"
    >
      <v-expansion-panel
        v-for="(panel, index) in panels"
        :key="index"
        :value="panel.value"
        :class="panel.class"
        :disabled="panel.disabled"
        :readonly="panel.readonly"
        :title="panel.title"
        :text="panel.text"
        :bg-color="panel.bgColor"
        :color="panel.color"
        hide-actions
      >
        <template #title v-if="$slots[`title-${panel.value}`] || panel.customTitle">
          <slot :name="`title-${panel.value}`">
            <div v-if="panel.customTitle" v-html="panel.title"></div>
            <template v-else>{{ panel.title }}</template>
          </slot>
        </template>

        <v-expansion-panel-text>
          <slot :name="`panel-${panel.value}`">
            <slot :name="panel.value">
              <div v-if="panel.content" v-html="panel.content"></div>
              <template v-else>{{ panel.text }}</template>
            </slot>
          </slot>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Panel {
  title: string
  text?: string
  content?: string
  value: string | number
  class?: string
  disabled?: boolean
  readonly?: boolean
  bgColor?: string
  color?: string
  customTitle?: boolean
}

const props = defineProps({
  modelValue: {
    type: [Array, Number, String],
    default: null,
  },
  panels: {
    type: Array as PropType<Panel[]>,
    required: true,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  mandatory: {
    type: Boolean,
    default: false,
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'accordion', 'inset', 'popout'].includes(value),
  },
  density: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'comfortable', 'compact'].includes(value),
  },
  color: {
    type: String,
    default: undefined,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  theme: {
    type: String,
    default: undefined,
  },
  flat: {
    type: Boolean,
    default: false,
  },
  bgColor: {
    type: String,
    default: undefined,
  },
  customClass: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

// Initialize local panel state, handling both single and multiple modes
const localPanel = ref(props.modelValue !== null ? props.modelValue : props.multiple ? [] : null)

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  localPanel.value = newValue
})

// Watch for local changes and emit events
watch(localPanel, (newValue) => {
  emit('update:modelValue', newValue)
})

// Handle panel change
const onPanelChange = (value: any) => {
  emit('change', value)
}

// Expose methods to parent component
defineExpose({
  openPanel: (value: string | number) => {
    if (props.multiple) {
      if (Array.isArray(localPanel.value)) {
        if (!localPanel.value.includes(value)) {
          localPanel.value = [...localPanel.value, value]
        }
      } else {
        localPanel.value = [value]
      }
    } else {
      localPanel.value = value
    }
  },
  closePanel: (value: string | number) => {
    if (props.multiple && Array.isArray(localPanel.value)) {
      localPanel.value = localPanel.value.filter(v => v !== value)
    } else if (localPanel.value === value) {
      localPanel.value = null
    }
  },
  togglePanel: (value: string | number) => {
    if (props.multiple && Array.isArray(localPanel.value)) {
      if (localPanel.value.includes(value)) {
        localPanel.value = localPanel.value.filter(v => v !== value)
      } else {
        localPanel.value = [...localPanel.value, value]
      }
    } else {
      localPanel.value = localPanel.value === value ? null : value
    }
  },
  isOpen: (value: string | number) => {
    if (props.multiple && Array.isArray(localPanel.value)) {
      return localPanel.value.includes(value)
    } else {
      return localPanel.value === value
    }
  },
})
</script>
