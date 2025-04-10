<!-- src/components/form/FormBuilder.vue -->
<template>
  <v-form ref="form" @submit.prevent="handleSubmit">
    <v-row v-if="title || description">
      <v-col cols="12">
        <h2 v-if="title" class="text-h5 mb-2">{{ title }}</h2>
        <p v-if="description" class="text-body-2">{{ description }}</p>
        <v-divider class="my-4"></v-divider>
      </v-col>
    </v-row>

    <v-row>
      <template v-for="(field, index) in fields" :key="index">
        <v-col :cols="field.cols || 12" :md="field.md" :sm="field.sm">
          <!-- Text Field -->
          <form-text-field
            v-if="field.type === 'text' || field.type === 'email' || field.type === 'password' || field.type === 'number'"
            v-model="formData[field.name]"
            :label="field.label"
            :type="field.type"
            :placeholder="field.placeholder"
            :hint="field.hint"
            :required="field.required"
            :validation-rules="field.rules"
            :disabled="loading || field.disabled"
            :readonly="field.readonly"
            :clearable="field.clearable"
            @validation="handleFieldValidation(field.name, $event)"
            ref="fieldRefs"
          />

          <!-- Select Field -->
          <form-select
            v-else-if="field.type === 'select'"
            v-model="formData[field.name]"
            :label="field.label"
            :items="field.items || []"
            :item-title="field.itemTitle || 'text'"
            :item-value="field.itemValue || 'value'"
            :multiple="field.multiple"
            :chips="field.chips"
            :hint="field.hint"
            :required="field.required"
            :validation-rules="field.rules"
            :disabled="loading || field.disabled"
            :readonly="field.readonly"
            :clearable="field.clearable"
            :return-object="field.returnObject"
            @validation="handleFieldValidation(field.name, $event)"
            ref="fieldRefs"
          />

          <!-- Checkbox Field -->
          <v-checkbox
            v-else-if="field.type === 'checkbox'"
            v-model="formData[field.name]"
            :label="field.label"
            :hint="field.hint"
            :disabled="loading || field.disabled"
            :color="field.color || 'primary'"
            @update:model-value="handleFieldChange(field.name, $event)"
          />

          <!-- Radio Group -->
          <v-radio-group
            v-else-if="field.type === 'radio'"
            v-model="formData[field.name]"
            :label="field.label"
            :disabled="loading || field.disabled"
            @update:model-value="handleFieldChange(field.name, $event)"
          >
            <v-radio
              v-for="(option, optionIndex) in field.options"
              :key="optionIndex"
              :label="option.label"
              :value="option.value"
              :disabled="option.disabled"
            ></v-radio>
          </v-radio-group>

          <!-- Textarea Field -->
          <v-textarea
            v-else-if="field.type === 'textarea'"
            v-model="formData[field.name]"
            :label="field.label"
            :placeholder="field.placeholder"
            :hint="field.hint"
            :rows="field.rows || 3"
            :auto-grow="field.autoGrow"
            :disabled="loading || field.disabled"
            :readonly="field.readonly"
            :clearable="field.clearable"
            @update:model-value="handleFieldChange(field.name, $event)"
          />

          <!-- Date Picker -->
          <v-menu
            v-else-if="field.type === 'date'"
            v-model="dateMenus[field.name]"
            :close-on-content-click="false"
            transition="scale-transition"
            min-width="auto"
          >
            <template v-slot:activator="{ props }">
              <v-text-field
                v-model="formData[field.name]"
                :label="field.label"
                prepend-icon="mdi-calendar"
                :hint="field.hint"
                :disabled="loading || field.disabled"
                readonly
                v-bind="props"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="formData[field.name]"
              @update:model-value="dateMenus[field.name] = false"
              :disabled="loading || field.disabled"
            ></v-date-picker>
          </v-menu>

          <!-- Switch -->
          <v-switch
            v-else-if="field.type === 'switch'"
            v-model="formData[field.name]"
            :label="field.label"
            :hint="field.hint"
            :disabled="loading || field.disabled"
            :color="field.color || 'primary'"
            @update:model-value="handleFieldChange(field.name, $event)"
          ></v-switch>

          <!-- Slider -->
          <div v-else-if="field.type === 'slider'">
            <label class="text-body-2 font-weight-medium">{{ field.label }}</label>
            <v-slider
              v-model="formData[field.name]"
              :min="field.min || 0"
              :max="field.max || 100"
              :step="field.step || 1"
              :disabled="loading || field.disabled"
              :color="field.color || 'primary'"
              thumb-label
              @update:model-value="handleFieldChange(field.name, $event)"
            ></v-slider>
          </div>

          <!-- Custom Field Slot -->
          <slot
            v-else-if="field.type === 'custom'"
            :name="`field-${field.name}`"
            :field="field"
            :model-value="formData[field.name]"
            :update-value="(value) => updateCustomField(field.name, value)"
            :loading="loading"
          ></slot>

          <!-- Default for unsupported types -->
          <v-alert
            v-else
            type="warning"
            variant="tonal"
            density="compact"
            class="mb-3"
          >
            Unsupported field type: {{ field.type }}
          </v-alert>
        </v-col>
      </template>
    </v-row>

    <div class="d-flex justify-end mt-4">
      <slot name="form-actions">
        <v-btn
          v-if="showCancelButton"
          variant="outlined"
          color="secondary"
          class="mr-3"
          @click="handleCancel"
          :disabled="loading"
        >
          {{ cancelButtonText }}
        </v-btn>

        <v-btn
          type="submit"
          color="primary"
          :loading="loading"
          :disabled="loading || (validateOnInput && !isFormValid)"
        >
          {{ submitButtonText }}
        </v-btn>
      </slot>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import FormTextField from '@/components/form/FormTextField.vue'
import FormSelect from '@/components/form/FormSelect.vue'

interface FormField {
  name: string
  type: string
  label: string
  placeholder?: string
  hint?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  clearable?: boolean
  rules?: Array<(value: any) => true | string>
  cols?: number
  md?: number
  sm?: number
  items?: Array<any>
  itemTitle?: string
  itemValue?: string
  multiple?: boolean
  chips?: boolean
  returnObject?: boolean
  options?: Array<{ label: string; value: any; disabled?: boolean }>
  rows?: number
  autoGrow?: boolean
  min?: number
  max?: number
  step?: number
  color?: string
  [key: string]: any
}

interface Props {
  fields: FormField[]
  initialValues?: Record<string, any>
  title?: string
  description?: string
  loading?: boolean
  validateOnInput?: boolean
  showCancelButton?: boolean
  submitButtonText?: string
  cancelButtonText?: string
}

const props = withDefaults(defineProps<Props>(), {
  initialValues: () => ({}),
  title: '',
  description: '',
  loading: false,
  validateOnInput: true,
  showCancelButton: true,
  submitButtonText: 'Submit',
  cancelButtonText: 'Cancel'
})

const emit = defineEmits([
  'submit',
  'cancel',
  'validation',
  'field-change'
])

// Track form state
const form = ref<any>(null)
const fieldRefs = ref<any[]>([])
const formData = reactive<Record<string, any>>({})
const fieldValidation = reactive<Record<string, { valid: boolean; message?: string }>>({})
const dateMenus = reactive<Record<string, boolean>>({})

// Initialize form data with initial values
onMounted(() => {
  // Initialize form data with initial values or defaults based on field type
  props.fields.forEach(field => {
    if (props.initialValues && props.initialValues[field.name] !== undefined) {
      formData[field.name] = props.initialValues[field.name]
    } else {
      // Set default values based on field type
      switch (field.type) {
        case 'checkbox':
        case 'switch':
          formData[field.name] = false
          break
        case 'select':
          formData[field.name] = field.multiple ? [] : null
          break
        default:
          formData[field.name] = null
          break
      }
    }

    // Initialize date menus if needed
    if (field.type === 'date') {
      dateMenus[field.name] = false
    }
  })
})

// Watch for changes in initialValues and update formData
watch(
  () => props.initialValues,
  (newValues) => {
    if (newValues) {
      Object.keys(newValues).forEach(key => {
        formData[key] = newValues[key]
      })
    }
  },
  { deep: true }
)

// Computed property to check if form is valid
const isFormValid = computed(() => {
  const fieldNames = props.fields.map(field => field.name)
  const validatedFields = Object.keys(fieldValidation)

  // All fields that should be validated are in the fieldValidation object
  const allFieldsValidated = fieldNames.every(name => {
    const field = props.fields.find(f => f.name === name)
    // Skip validation for fields without validation rules
    if (!field || !field.rules || field.rules.length === 0) {
      return true
    }
    return validatedFields.includes(name)
  })

  // All validated fields are valid
  const allFieldsValid = Object.values(fieldValidation).every(state => state.valid)

  return allFieldsValidated && allFieldsValid
})

// Handle field validation events
const handleFieldValidation = (fieldName: string, event: { valid: boolean; message?: string }) => {
  fieldValidation[fieldName] = event
  emit('validation', { field: fieldName, valid: event.valid, message: event.message, formValid: isFormValid.value })
}

// Handle field change events
const handleFieldChange = (fieldName: string, value: any) => {
  emit('field-change', { field: fieldName, value })
}

// Update a custom field value
const updateCustomField = (fieldName: string, value: any) => {
  formData[fieldName] = value
  handleFieldChange(fieldName, value)
}

// Validate all fields in the form
const validateForm = async () => {
  let formValid = true

  // Get all field components with validate method
  const fieldComponents = fieldRefs.value.filter(component => component && typeof component.validate === 'function')

  // Validate each field
  for (const component of fieldComponents) {
    const isValid = await component.validate()
    if (!isValid) {
      formValid = false
    }
  }

  return formValid
}

// Handle form submission
const handleSubmit = async () => {
  // Validate all fields first
  const isValid = await validateForm()

  if (isValid) {
    emit('submit', { ...formData })
  } else {
    emit('validation', { formValid: false })
  }
}

// Handle cancel button click
const handleCancel = () => {
  emit('cancel')
}

// Expose methods to parent component
defineExpose({
  validateForm,
  formData,
  isFormValid,
  resetForm: () => {
    // Reset the form data to initial values
    props.fields.forEach(field => {
      if (props.initialValues && props.initialValues[field.name] !== undefined) {
        formData[field.name] = props.initialValues[field.name]
      } else {
        formData[field.name] = null
      }
    })

    // Clear validation state
    Object.keys(fieldValidation).forEach(key => {
      delete fieldValidation[key]
    })
  }
})
</script>
