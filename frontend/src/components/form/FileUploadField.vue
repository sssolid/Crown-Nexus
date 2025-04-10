<!-- src/components/form/FileUploadField.vue -->
<template>
  <div class="file-upload-field">
    <!-- Use your existing FormTextField for validation and field structure -->
    <form-text-field
      :model-value="displayValue"
      :label="label"
      :hint="hint"
      :placeholder="placeholder"
      :error-messages="errorMessage"
      :required="required"
      readonly
      @click="triggerFileInput"
      class="file-input-field"
    >
      <template #append-inner>
        <v-icon
          icon="mdi-paperclip"
          class="file-browse-icon"
          @click.stop="triggerFileInput"
        ></v-icon>
      </template>
    </form-text-field>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      class="file-upload__input"
      :accept="accept"
      :multiple="multiple"
      :disabled="disabled"
      @change="onFileChange"
    >

    <!-- File list -->
    <div v-if="selectedFiles.length > 0" class="selected-files mt-2">
      <v-list density="compact" class="file-list border rounded">
        <v-list-item
          v-for="(file, index) in selectedFiles"
          :key="index"
          :subtitle="formatFileSize(file.size)"
          density="compact"
          class="file-item"
        >
          <template v-slot:prepend>
            <v-icon :icon="getFileIcon(file)" size="small" class="me-2"></v-icon>
          </template>

          <v-list-item-title class="text-body-2">{{ file.name }}</v-list-item-title>

          <template v-slot:append>
            <v-btn
              icon="mdi-close"
              variant="text"
              size="small"
              color="error"
              density="compact"
              @click="removeFile(index)"
              aria-label="Remove file"
            ></v-btn>
          </template>
        </v-list-item>
      </v-list>

      <div v-if="multiple && selectedFiles.length > 1" class="d-flex justify-end mt-2">
        <v-btn
          size="small"
          variant="text"
          color="error"
          density="compact"
          @click="clearFiles"
          prepend-icon="mdi-delete-sweep"
        >
          Clear all files
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import FormTextField from '@/components/form/FormTextField.vue'

const props = defineProps({
  modelValue: {
    type: Array as PropType<File[]>,
    default: () => [],
  },
  label: {
    type: String,
    default: 'Upload File',
  },
  hint: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Click to select file',
  },
  accept: {
    type: String,
    default: '',
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  maxSize: {
    type: Number,
    default: 0, // In bytes, 0 means no limit
  },
})

const emit = defineEmits(['update:modelValue', 'change', 'error'])

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFiles = ref<File[]>([...props.modelValue])
const errorMessage = ref('')

// Display value for text field
const displayValue = computed(() => {
  if (selectedFiles.value.length === 0) {
    return ''
  } else if (selectedFiles.value.length === 1) {
    return selectedFiles.value[0].name
  } else {
    return `${selectedFiles.value.length} files selected`
  }
})

// Trigger file input click
const triggerFileInput = () => {
  if (!props.disabled && fileInput.value) {
    fileInput.value.click()
  }
}

// Format file size for display
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Get icon based on file type
const getFileIcon = (file: File): string => {
  const extension = file.name.split('.').pop()?.toLowerCase() || ''

  // Document types
  if (['pdf'].includes(extension)) return 'mdi-file-pdf-box'
  if (['doc', 'docx'].includes(extension)) return 'mdi-file-word-box'
  if (['xls', 'xlsx'].includes(extension)) return 'mdi-file-excel-box'
  if (['ppt', 'pptx'].includes(extension)) return 'mdi-file-powerpoint-box'
  if (['txt', 'rtf', 'md'].includes(extension)) return 'mdi-file-document'

  // Image types
  if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(extension)) {
    return 'mdi-file-image'
  }

  // Default
  return 'mdi-file'
}

// Handle file selection
const onFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement

  if (input.files && input.files.length > 0) {
    const files = Array.from(input.files)

    // Validate file size if needed
    if (props.maxSize > 0) {
      for (const file of files) {
        if (file.size > props.maxSize) {
          errorMessage.value = `File too large: ${file.name} (max size: ${formatFileSize(props.maxSize)})`
          emit('error', errorMessage.value)
          return
        }
      }
    }

    errorMessage.value = ''

    // Update files
    const newFiles = props.multiple ? [...selectedFiles.value, ...files] : [...files]
    selectedFiles.value = newFiles
    emit('update:modelValue', newFiles)
    emit('change', newFiles)
  }

  // Reset input so the same file can be selected again
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Remove a file
const removeFile = (index: number) => {
  selectedFiles.value.splice(index, 1)
  emit('update:modelValue', selectedFiles.value)
  emit('change', selectedFiles.value)
}

// Clear all files
const clearFiles = () => {
  selectedFiles.value = []
  emit('update:modelValue', [])
  emit('change', [])
}
</script>

<style scoped>
.file-upload__input {
  display: none;
}

.file-browse-icon {
  cursor: pointer;
}

.file-input-field {
  cursor: pointer;
}

.file-list {
  max-height: 300px;
  overflow-y: auto;
}

.file-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.file-item:last-child {
  border-bottom: none;
}
</style>
