<!-- frontend/src/components/common/ConfirmDialog.vue -->
<template>
  <v-dialog v-model="dialogVisible" max-width="400">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>

      <v-card-text>
        {{ message }}
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn
          variant="text"
          @click="cancel"
          :disabled="isLoading"
        >
          {{ cancelText }}
        </v-btn>

        <v-btn
          :color="confirmColor"
          @click="confirm"
          :loading="isLoading"
        >
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?'
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  confirmColor: {
    type: String,
    default: 'primary'
  },
  dangerConfirm: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm'): void;
  (e: 'cancel'): void;
}>();

// State
const isLoading = ref(false);

// Computed
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// Methods
function confirm() {
  isLoading.value = true;

  try {
    emit('confirm');
  } finally {
    // Reset loading state after a short delay to allow time for UI update
    setTimeout(() => {
      isLoading.value = false;
      dialogVisible.value = false;
    }, 300);
  }
}

function cancel() {
  emit('cancel');
  dialogVisible.value = false;
}

// Watchers
watch(() => props.dangerConfirm, (isDanger) => {
  // Change confirm color if danger mode is activated
  if (isDanger && props.confirmColor === 'primary') {
    props.confirmColor = 'error';
  }
});
</script>
