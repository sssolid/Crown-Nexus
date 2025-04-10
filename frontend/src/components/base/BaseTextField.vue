<!-- src/components/base/BaseTextField.vue -->
<template>
  <v-text-field
    v-model="localModelValue"
    :label="label"
    :placeholder="placeholder"
    :hint="hint"
    :error-messages="errorMessages"
    :rules="rules"
    :density="density"
    :variant="variant"
    :color="color"
    :bg-color="bgColor"
    :disabled="disabled"
    :readonly="readonly"
    :clearable="clearable"
    :type="type"
    :hide-details="hideDetails"
    :counter="counter"
    :autofocus="autofocus"
    :autocomplete="autocomplete"
    :required="required"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
  >
    <template v-for="(_, slot) in $slots" #[slot]="scope">
      <slot :name="slot" v-bind="scope || {}" />
    </template>
  </v-text-field>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  hint: {
    type: String,
    default: '',
  },
  errorMessages: {
    type: [String, Array],
    default: () => [],
  },
  rules: {
    type: Array,
    default: () => [],
  },
  density: {
    type: String,
    default: 'comfortable',
    validator: (value: string) =>
      ['default', 'comfortable', 'compact'].includes(value),
  },
  variant: {
    type: String,
    default: 'outlined',
    validator: (value: string) =>
      ['plain', 'filled', 'outlined', 'solo', 'underlined'].includes(value),
  },
  color: {
    type: String,
    default: 'primary',
  },
  bgColor: {
    type: String,
    default: undefined,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String,
    default: 'text',
  },
  hideDetails: {
    type: [Boolean, String],
    default: false,
  },
  counter: {
    type: [Boolean, Number, String],
    default: false,
  },
  autofocus: {
    type: Boolean,
    default: false,
  },
  autocomplete: {
    type: String,
    default: undefined,
  },
  required: {
    type: Boolean,
    default: false,
  },
  prependIcon: {
    type: String,
    default: '',
  },
  appendIcon: {
    type: String,
    default: '',
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'change'])

const localModelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>
