// src/composables/useFormValidation.ts
import { ref, computed, watch } from 'vue'

interface ValidationRule {
  (value: any): boolean | string
}

interface ValidationResult {
  valid: boolean
  message?: string
}

export function useFormValidation(options: {
  initialValues?: Record<string, any>
  validationRules?: Record<string, ValidationRule[]>
  validateOnMount?: boolean
  validateOnChange?: boolean
} = {}) {
  const {
    initialValues = {},
    validationRules = {},
    validateOnMount = false,
    validateOnChange = true,
  } = options

  // Form data
  const formData = ref({ ...initialValues })

  // Validation state
  const fieldErrors = ref<Record<string, string>>({})
  const touched = ref<Record<string, boolean>>({})
  const isSubmitting = ref(false)

  // Computed properties
  const isValid = computed(() => {
    return Object.keys(fieldErrors.value).length === 0
  })

  const isDirty = computed(() => {
    return Object.keys(touched.value).length > 0
  })

  // Validate a specific field
  const validateField = (field: string, value: any): ValidationResult => {
    if (!validationRules[field] || validationRules[field].length === 0) {
      return { valid: true }
    }

    // Check all rules for the field
    for (const rule of validationRules[field]) {
      const result = rule(value)

      if (result !== true) {
        fieldErrors.value[field] = typeof result === 'string' ? result : 'Invalid value'
        return { valid: false, message: fieldErrors.value[field] }
      }
    }

    // If all rules pass, remove any existing error
    if (fieldErrors.value[field]) {
      delete fieldErrors.value[field]
    }

    return { valid: true }
  }

  // Validate all fields
  const validateForm = (): boolean => {
    let isFormValid = true

    // Check all fields with validation rules
    Object.keys(validationRules).forEach(field => {
      const result = validateField(field, formData.value[field])
      if (!result.valid) {
        isFormValid = false
      }
    })

    return isFormValid
  }

  // Update a field value
  const updateField = (field: string, value: any) => {
    formData.value[field] = value
    touched.value[field] = true

    if (validateOnChange) {
      validateField(field, value)
    }
  }

  // Reset the form
  const resetForm = (newValues = initialValues) => {
    formData.value = { ...newValues }
    fieldErrors.value = {}
    touched.value = {}
    isSubmitting.value = false
  }

  // Handle form submission
  const handleSubmit = async (submitFn: (data: Record<string, any>) => Promise<any> | void) => {
    // Validate all fields before submitting
    const isFormValid = validateForm()

    if (!isFormValid) {
      return { success: false, errors: fieldErrors.value }
    }

    isSubmitting.value = true

    try {
      const result = await submitFn(formData.value)
      return { success: true, result }
    } catch (error) {
      return { success: false, error }
    } finally {
      isSubmitting.value = false
    }
  }

  // Watch for external changes to initialValues
  watch(() => options.initialValues, (newValues) => {
    if (newValues && Object.keys(newValues).length > 0) {
      resetForm(newValues)
    }
  }, { deep: true })

  // Validate on mount if requested
  if (validateOnMount) {
    validateForm()
  }

  return {
    formData,
    fieldErrors,
    touched,
    isSubmitting,
    isValid,
    isDirty,
    validateField,
    validateForm,
    updateField,
    resetForm,
    handleSubmit,
  }
}
