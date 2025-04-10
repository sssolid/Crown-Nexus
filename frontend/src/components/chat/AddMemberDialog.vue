<!-- frontend/src/components/chat/AddMemberDialog.vue -->
<template>
  <v-dialog v-model="dialogVisible" max-width="500">
    <v-card>
      <v-card-title>Add Member to Chat</v-card-title>

      <v-card-text>
        <v-form ref="form" @submit.prevent="submitForm">
          <v-autocomplete
            v-model="selectedUser"
            :items="availableUsers"
            item-title="full_name"
            item-value="id"
            label="Select User"
            required
            :rules="[v => !!v || 'User is required']"
            :loading="loadingUsers"
          ></v-autocomplete>

          <v-select
            v-model="selectedRole"
            label="Role"
            :items="roleOptions"
            item-title="text"
            item-value="value"
            required
          ></v-select>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
        <v-btn
          color="primary"
          @click="submitForm"
          :loading="isSubmitting"
        >
          Add
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { ChatMemberRole } from '@/types/chat';
import api from '@/services/api';
import { chatService } from '@/services/chat';
import { notificationService } from '@/utils/notifications';

const props = defineProps<{
  modelValue: boolean;
  roomId: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'add', userId: string, role: string): void;
}>();

// State
const selectedUser = ref<string | null>(null);
const selectedRole = ref(ChatMemberRole.MEMBER);
const availableUsers = ref<any[]>([]);
const loadingUsers = ref(false);
const isSubmitting = ref(false);
const form = ref<any>(null);

// Computed
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const roleOptions = computed(() => [
  { text: 'Member', value: ChatMemberRole.MEMBER },
  { text: 'Admin', value: ChatMemberRole.ADMIN },
]);

// Watch for dialog visibility
watch(() => props.modelValue, (isVisible) => {
  if (isVisible) {
    resetForm();
    loadUsers();
  }
});

// Methods
function closeDialog() {
  dialogVisible.value = false;
}

function resetForm() {
  selectedUser.value = null;
  selectedRole.value = ChatMemberRole.MEMBER;

  // Reset form validation
  if (form.value) {
    form.value.resetValidation();
  }
}

async function loadUsers() {
  loadingUsers.value = true;

  try {
    // Get users from API
    const response = await api.get('/users');

    if (response.items) {
      // Get current members to filter them out
      const roomMembers = chatService.activeRoomMembers.value || [];
      const memberIds = roomMembers.map(m => m.user_id);

      // Filter out users who are already members
      availableUsers.value = response.items.filter(
        (user: any) => !memberIds.includes(user.id)
      );
    }
  } catch (error) {
    console.error('Error loading users:', error);
    notificationService.error('Failed to load users');
  } finally {
    loadingUsers.value = false;
  }
}

async function submitForm() {
  if (!form.value) return;

  const { valid } = await form.value.validate();

  if (!valid || !selectedUser.value) return;

  isSubmitting.value = true;

  try {
    // Emit add event
    emit('add', selectedUser.value, selectedRole.value);

    // Close dialog
    closeDialog();
  } catch (error) {
    console.error('Error adding member:', error);
    notificationService.error('Failed to add member');
  } finally {
    isSubmitting.value = false;
  }
}

// Initialize
onMounted(() => {
  if (props.modelValue) {
    loadUsers();
  }
});
</script>
