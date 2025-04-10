<!-- src/components/form/FileUpload.vue -->
<template>
  <div class="file-upload" :class="[`file-upload--${variant}`, customClass]">
    <div
      v-if="variant === 'dropzone'"
      class="file-upload__dropzone"
      :class="{
        'file-upload__dropzone--active': isDragActive,
        'file-upload__dropzone--disabled': disabled,
        'file-upload__dropzone--error': !!errorMessage,
        [`file-upload__dropzone--${size}`]: true
      }"
      @dragenter.prevent="onDragEnter"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
    >
      <div class="file-upload__content">
        <div v-if="$slots.dropzone">
          <slot name="dropzone" :is-drag-active="isDragActive"></slot>
        </div>
        <div v-else class="file-upload__default-content">
          <v-icon :icon="icon" :size="iconSize" :color="iconColor" class="mb-3"></v-icon>
          <div class="file-upload__title">{{ title }}</div>
          <div class="file-upload__subtitle">{{ subtitle }}</div>
          <v-btn
            v-if="showBrowseButton"
            size="small"
            class="mt-3"
            :variant="browseButtonVariant"
            :color="browseButtonColor"
            :disabled="disabled"
            @click.stop="triggerFileInput"
          >
            {{ browseButtonText }}
          </v-btn>
        </div>
      </div>
    </div>

    <div v-else class="file-upload__button-container">
      <slot name="button">
        <v-btn
          :color="color"
          :variant="buttonVariant"
          :disabled="disabled"
          :loading="loading"
          :prepend-icon="icon"
          @click="triggerFileInput"
          :class="buttonClass"
        >
          {{ buttonText }}
        </v-btn>
      </slot>
    </div>

    <input
      ref="fileInput"
      type="file"
      class="file-upload__input"
      :accept="accept"
      :multiple="multiple"
      :disabled="disabled"
      @change="onFileChange"
    >

    <v-alert
      v-if="errorMessage"
      type="error"
      variant="tonal"
      class="mt-2"
      density="compact"
    >
      {{ errorMessage }}
    </v-alert>

    <div v-if="showSelectedFiles && selectedFiles.length > 0" class="file-upload__selected-files mt-3">
      <div v-if="$slots['files-header']" class="mb-2">
        <slot name="files-header" :files="selectedFiles"></slot>
      </div>

      <v-list v-if="!$slots.files" density="compact" class="file-upload__files-list">
        <v-list-item
          v-for="(file, index) in selectedFiles"
          :key="index"
          :subtitle="formatFileSize(file.size)"
          class="file-item"
        >
          <template v-slot:prepend>
            <v-icon :icon="getFileIcon(file)" class="me-2"></v-icon>
          </template>

          <v-list-item-title>{{ file.name }}</v-list-item-title>

          <template v-slot:append>
            <v-btn
              icon="mdi-close"
              variant="text"
              size="small"
              color="error"
              @click="removeFile(index)"
              aria-label="Remove file"
            ></v-btn>
          </template>
        </v-list-item>
      </v-list>

      <slot v-else name="files" :files="selectedFiles" :remove-file="removeFile"></slot>

      <div v-if="$slots['files-footer']" class="mt-2">
        <slot name="files-footer" :files="selectedFiles" :clear-files="clearFiles"></slot>
      </div>

      <div v-else-if="showClearButton && selectedFiles.length > 1" class="d-flex justify-end mt-2">
        <v-btn
          size="small"
          variant="text"
          color="error"
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
import { ref, computed, watch } from 'vue'

interface FileInfo extends File {
  preview?: string;
  progress?: number;
  error?: string;
  status?: 'pending' | 'uploading' | 'success' | 'error';
}

const props = defineProps({
  modelValue: {
    type: Array as PropType<File[]>,
    default: () => [],
  },
  variant: {
    type: String,
    default: 'button',
    validator: (value: string) => ['button', 'dropzone'].includes(value),
  },
  accept: {
    type: String,
    default: '',
  },
  multiple: {
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
  maxSize: {
    type: Number,
    default: 0, // In bytes, 0 means no limit
  },
  maxFiles: {
    type: Number,
    default: 0, // 0 means no limit
  },
  icon: {
    type: String,
    default: 'mdi-cloud-upload',
  },
  iconSize: {
    type: [String, Number],
    default: 'large',
  },
  iconColor: {
    type: String,
    default: 'primary',
  },
  color: {
    type: String,
    default: 'primary',
  },
  buttonVariant: {
    type: String,
    default: 'elevated',
  },
  buttonText: {
    type: String,
    default: 'Upload Files',
  },
  buttonClass: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    default: 'Drop files here',
  },
  subtitle: {
    type: String,
    default: 'or click to browse',
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value: string) => ['small', 'medium', 'large'].includes(value),
  },
  showSelectedFiles: {
    type: Boolean,
    default: true,
  },
  showClearButton: {
    type: Boolean,
    default: true,
  },
  customClass: {
    type: String,
    default: '',
  },
  showBrowseButton: {
    type: Boolean,
    default: true,
  },
  browseButtonText: {
    type: String,
    default: 'Browse Files',
  },
  browseButtonVariant: {
    type: String,
    default: 'tonal',
  },
  browseButtonColor: {
    type: String,
    default: 'primary',
  },
  validateOnDrop: {
    type: Boolean,
    default: true,
  },
  validateFileType: {
    type: Boolean,
    default: true,
  },
  validateFileSize: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits([
  'update:modelValue',
  'change',
  'error',
  'drop',
  'select',
  'remove',
  'clear'
])

const fileInput = ref<HTMLInputElement | null>(null)
const isDragActive = ref(false)
const selectedFiles = ref<FileInfo[]>([...props.modelValue])
const errorMessage = ref('')

// Watch for external changes to modelValue
watch(() => props.modelValue, (newFiles) => {
  selectedFiles.value = [...newFiles]
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

  // Audio types
  if (['mp3', 'wav', 'ogg', 'flac', 'm4a'].includes(extension)) {
    return 'mdi-file-music'
  }

  // Video types
  if (['mp4', 'avi', 'mov', 'wmv', 'mkv', 'webm'].includes(extension)) {
    return 'mdi-file-video'
  }

  // Archive types
  if (['zip', 'rar', '7z', 'tar', 'gz'].includes(extension)) {
    return 'mdi-zip-box'
  }

  // Code types
  if (['js', 'ts', 'html', 'css', 'php', 'py', 'java', 'cs', 'rb', 'go'].includes(extension)) {
    return 'mdi-code-braces'
  }

  // Default
  return 'mdi-file'
}

// Validate files
const validateFiles = (files: File[]): { valid: boolean; message: string } => {
  // Check max files
  if (props.maxFiles > 0 && files.length > props.maxFiles) {
    return {
      valid: false,
      message: `You can upload a maximum of ${props.maxFiles} file${props.maxFiles !== 1 ? 's' : ''}`
    }
  }

  // Check file types if accept is specified
  if (props.validateFileType && props.accept) {
    const acceptedTypes = props.accept.split(',').map(type => type.trim())

    for (const file of files) {
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
      const fileType = file.type

      const isAccepted = acceptedTypes.some(type => {
        // Handle file extensions (e.g., .jpg)
        if (type.startsWith('.')) {
          return type.toLowerCase() === fileExtension.toLowerCase()
        }
        // Handle MIME types with wildcards (e.g., image/*)
        else if (type.includes('*')) {
          const typeParts = type.split('/')
          const fileTypeParts = fileType.split('/')
          return typeParts[0] === fileTypeParts[0] && (typeParts[1] === '*' || typeParts[1] === fileTypeParts[1])
        }
        // Handle exact MIME types (e.g., image/jpeg)
        else {
          return type === fileType
        }
      })

      if (!isAccepted) {
        return {
          valid: false,
          message: `File type not accepted: ${file.name}`
        }
      }
    }
  }

  // Check file sizes
  if (props.validateFileSize && props.maxSize > 0) {
    for (const file of files) {
      if (file.size > props.maxSize) {
        return {
          valid: false,
          message: `File too large: ${file.name} (max size: ${formatFileSize(props.maxSize)})`
        }
      }
    }
  }

  return { valid: true, message: '' }
}

// Handle file selection
const onFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement

  if (input.files && input.files.length > 0) {
    const files = Array.from(input.files)
    handleFiles(files)
  }

  // Reset input so the same file can be selected again
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Handle files (both from input and drop)
const handleFiles = (files: File[]) => {
  // Validate files
  const validation = validateFiles(files)

  if (!validation.valid) {
    errorMessage.value = validation.message
    emit('error', validation.message, files)
    return
  }

  errorMessage.value = ''

  // If not multiple, replace existing files
  const newFiles = props.multiple
    ? [...selectedFiles.value, ...files]
    : [...files]

  selectedFiles.value = newFiles
  emit('update:modelValue', newFiles)
  emit('change', newFiles)
  emit('select', files)
}

// Remove a file
const removeFile = (index: number) => {
  const removedFile = selectedFiles.value[index]
  selectedFiles.value.splice(index, 1)
  emit('update:modelValue', selectedFiles.value)
  emit('change', selectedFiles.value)
  emit('remove', removedFile, index)
}

// Clear all files
const clearFiles = () => {
  const oldFiles = [...selectedFiles.value]
  selectedFiles.value = []
  emit('update:modelValue', [])
  emit('change', [])
  emit('clear', oldFiles)
}

// Drag event handlers
const onDragEnter = (event: DragEvent) => {
  if (props.disabled) return
  isDragActive.value = true
}

const onDragOver = (event: DragEvent) => {
  if (props.disabled) return
  isDragActive.value = true
}

const onDragLeave = (event: DragEvent) => {
  if (props.disabled) return
  isDragActive.value = false
}

const onDrop = (event: DragEvent) => {
  if (props.disabled) return
  isDragActive.value = false

  if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
    const files = Array.from(event.dataTransfer.files)
    handleFiles(files)
    emit('drop', files)
  }
}

// Expose methods to parent component
defineExpose({
  triggerFileInput,
  clearFiles,
  removeFile,
  validateFiles,
})
</script>

<style scoped>
.file-upload__input {
  display: none;
}

.file-upload__dropzone {
  border: 2px dashed var(--v-border-color);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  background-color: rgba(var(--v-theme-surface-variant), 0.5);
}

.file-upload__dropzone--active {
  border-color: var(--v-theme-primary);
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.file-upload__dropzone--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.file-upload__dropzone--error {
  border-color: var(--v-theme-error);
  background-color: rgba(var(--v-theme-error), 0.05);
}

.file-upload__dropzone--small {
  padding: 12px;
  min-height: 100px;
}

.file-upload__dropzone--medium {
  padding: 24px;
  min-height: 150px;
}

.file-upload__dropzone--large {
  padding: 32px;
  min-height: 200px;
}

.file-upload__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.file-upload__default-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.file-upload__title {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 4px;
}

.file-upload__subtitle {
  font-size: 0.9rem;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.file-upload__files-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid var(--v-border-color);
  border-radius: 4px;
}

.file-item {
  border-bottom: 1px solid var(--v-border-color);
}

.file-item:last-child {
  border-bottom: none;
}
</style>
