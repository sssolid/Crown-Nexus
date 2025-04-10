<!-- src/components/form/FormSelect.vue -->
<template>
  <div class="form-field" :class="{ 'form-field--error': hasError }">
    <v-select
      v-model="localModelValue"
      :label="label"
      :hint="hint"
      :items="items"
      :item-title="itemTitle"
      :item-value="itemValue"
      :multiple="multiple"
      :chips="chips"
      :error-messages="errorMessage"
      :rules="validationRules"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
      :clearable="clearable"
      :density="density"
      :variant="variant"
      :return-object="returnObject"
      v-bind="$attrs"
      @blur="validate"
      @update:model-value="onInput"
    >
      <template v-for="(_, slot) in $slots" #[slot]="scope">
        <slot :name="slot" v-bind="scope || {}" />
      </template>
    </v-select>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface Props {
  modelValue: any
  label?: string
  hint?: string
  items: Array<any>
  itemTitle?: string
  itemValue?: string
  multiple?: boolean
  chips?: boolean
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  clearable?: boolean
  returnObject?: boolean
  validateOnMount?: boolean
  validateOnInput?: boolean
  density?: 'default' | 'comfortable' | 'compact'
  variant?: string
  validationRules?: Array<(value: any) => true | string>
  validator?: (value: any) => { valid: boolean; message?: string }
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  hint: '',
  itemTitle: 'title',
  itemValue: 'value',
  multiple: false,
  chips: false,
  required: false,
  disabled: false,
  readonly: false,
  clearable: false,
  returnObject: false,
  validateOnMount: false,
  validateOnInput: true,
  density: 'comfortable',
  variant: 'outlined',
  validationRules: () => [],
  validator: undefined,
})

const emit = defineEmits([
  'update:modelValue',
  'validation',
  'blur',
  'focus',
  'change',
  'input'
])

const localModelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const errorMessage = ref<string>('')
const hasError = computed(() => errorMessage.value !== '')
const isValid = ref<boolean | null>(null)

// Combine built-in rules with required rule if needed
const validationRules = computed(() => {
  const rules = [...props.validationRules]

  // Add required rule if the field is marked as required
  if (props.required) {
    rules.unshift((v: any) => {
      // Check for empty array if multiple
      if (props.multiple && Array.isArray(v)) {
        return v.length > 0 || `${props.label || 'Field'} is required`
      }
      return !!v || `${props.label || 'Field'} is required`
    })
  }

  return rules
})

const validate = () => {
  // Check each validation rule
  for (const rule of validationRules.value) {
    const result = rule(localModelValue.value)
    if (result !== true) {
      errorMessage.value = result
      isValid.value = false
      emit('validation', { valid: false, message: result })
      return false
    }
  }

  // Check custom validator if provided
  if (props.validator) {
    const { valid, message } = props.validator(localModelValue.value)
    if (!valid) {
      errorMessage.value = message || 'Invalid input'
      isValid.value = false
      emit('validation', { valid: false, message: errorMessage.value })
      return false
    }
  }

  // If we got here, validation passed
  errorMessage.value = ''
  isValid.value = true
  emit('validation', { valid: true })
  return true
}

const onInput = (value: any) => {
  if (props.validateOnInput) {
    validate()
  }
  emit('input', value)
}

// Validate on mount if requested
onMounted(() => {
  if (props.validateOnMount) {
    validate()
  }
})

// Watch for external changes
watch(
  () => props.modelValue,
  () => {
    if (props.validateOnInput) {
      validate()
    }
  }
)

// Expose methods to parent component
defineExpose({
  validate,
  isValid,
  errorMessage,
})
</script>

<style scoped>
.form-field {
  margin-bottom: 16px;
}
</style>
