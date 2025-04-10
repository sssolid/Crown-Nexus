<!-- src/components/dialogs/ConfirmationDialog.vue -->
<template>
  <base-dialog
    v-model="dialogVisible"
    :title="title"
    :max-width="maxWidth"
    :persistent="persistent"
    :show-close-button="showCloseButton"
    :prepend-icon="prependIcon || icon"
    :prepend-icon-color="prependIconColor || iconColor"
    @close="onClose"
  >
    <div v-if="message" class="confirmation-message" v-html="message"></div>
    <slot></slot>

    <template #actions>
      <v-spacer></v-spacer>

      <template v-if="type === 'binary'">
        <v-btn
          variant="text"
          :color="cancelColor"
          @click="onCancel"
          :disabled="loading"
          class="me-2"
        >
          {{ cancelText }}
        </v-btn>

        <v-btn
          :color="confirmColor"
          :loading="loading"
          @click="onConfirm"
          :disabled="loading"
        >
          {{ confirmText }}
        </v-btn>
      </template>

      <template v-else-if="type === 'multiple'">
        <template v-for="(action, index) in actions" :key="index">
          <v-btn
            :variant="action.variant || 'text'"
            :color="action.color || 'primary'"
            @click="onActionClick(action)"
            :disabled="loading || action.disabled"
            :loading="loading && currentAction === action.value"
            class="mx-1"
          >
            <v-icon v-if="action.icon" :icon="action.icon" start></v-icon>
            {{ action.text }}
          </v-btn>
        </template>
      </template>

      <template v-else-if="type === 'acknowledge'">
        <v-btn
          :color="confirmColor"
          @click="onAcknowledge"
          :disabled="loading"
          :loading="loading"
        >
          {{ acknowledgeText }}
        </v-btn>
      </template>
    </template>
  </base-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, PropType } from 'vue'
import BaseDialog from './BaseDialog.vue'

interface DialogAction {
  text: string
  value: string
  color?: string
  variant?: string
  icon?: string
  disabled?: boolean
}

type DialogType = 'binary' | 'multiple' | 'acknowledge'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: 'Confirmation',
  },
  message: {
    type: String,
    default: '',
  },
  type: {
    type: String as PropType<DialogType>,
    default: 'binary',
    validator: (value: string) => ['binary', 'multiple', 'acknowledge'].includes(value),
  },
  icon: {
    type: String,
    default: '',
  },
  iconColor: {
    type: String,
    default: '',
  },
  confirmText: {
    type: String,
    default: 'Confirm',
  },
  cancelText: {
    type: String,
    default: 'Cancel',
  },
  acknowledgeText: {
    type: String,
    default: 'OK',
  },
  confirmColor: {
    type: String,
    default: 'primary',
  },
  cancelColor: {
    type: String,
    default: 'secondary',
  },
  actions: {
    type: Array as PropType<DialogAction[]>,
    default: () => [],
  },
  maxWidth: {
    type: [String, Number],
    default: 400,
  },
  persistent: {
    type: Boolean,
    default: false,
  },
  showCloseButton: {
    type: Boolean,
    default: false,
  },
  prependIcon: {
    type: String,
    default: '',
  },
  prependIconColor: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'update:modelValue',
  'confirm',
  'cancel',
  'acknowledge',
  'action',
  'close'
])

const dialogVisible = ref(props.modelValue)
const currentAction = ref<string | null>(null)

// Watch for external changes to modelValue
watch(() => props.modelValue, (newVal) => {
  dialogVisible.value = newVal
})

// Watch for internal changes and emit updates
watch(dialogVisible, (newVal) => {
  emit('update:modelValue', newVal)
})

const onConfirm = () => {
  emit('confirm')
}

const onCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}

const onAcknowledge = () => {
  emit('acknowledge')
  dialogVisible.value = false
}

const onActionClick = (action: DialogAction) => {
  currentAction.value = action.value
  emit('action', action)
}

const onClose = () => {
  emit('close')
  emit('update:modelValue', false)
}

defineExpose({
  close: () => {
    dialogVisible.value = false
  },
})
</script>

<style scoped>
.confirmation-message {
  white-space: pre-line;
}
</style>
