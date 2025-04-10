<!-- frontend/src/components/chat/ChatRoomDialog.vue -->
<template>
  <v-dialog v-model="dialogVisible" max-width="500">
    <v-card>
      <v-card-title>Create New Chat Room</v-card-title>
      
      <v-card-text>
        <v-form ref="form" @submit.prevent="submitForm">
          <v-text-field
            v-model="roomName"
            label="Room Name"
            required
            :rules="[v => !!v || 'Room name is required']"
          ></v-text-field>
          
          <v-select
            v-model="roomType"
            label="Room Type"
            :items="roomTypeOptions"
            item-title="text"
            item-value="value"
            required
          ></v-select>
          
          <v-autocomplete
            v-if="showMembersField"
            v-model="selectedMembers"
            :items="availableUsers"
            item-title="full_name"
            item-value="id"
            label="Add Members"
            multiple
            chips
            closable-chips
            :loading="loadingUsers"
          ></v-autocomplete>
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
          Create
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { ChatRoomType } from '@/types/chat';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import { notificationService } from '@/utils/notification';

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'create', name: string, type: ChatRoomType, members: any[]): void;
}>();

// State
const roomName = ref('');
const roomType = ref(ChatRoomType.GROUP);
const selectedMembers = ref<string[]>([]);
const availableUsers = ref<any[]>([]);
const loadingUsers = ref(false);
const isSubmitting = ref(false);
const form = ref<any>(null);

// Store
const authStore = useAuthStore();

// Computed
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const roomTypeOptions = computed(() => [
  { text: 'Group Chat', value: ChatRoomType.GROUP },
  { text: 'Company Chat', value: ChatRoomType.COMPANY },
]);

const showMembersField = computed(() => {
  return roomType.value === ChatRoomType.GROUP;
});

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
  roomName.value = '';
  roomType.value = ChatRoomType.GROUP;
  selectedMembers.value = [];
  
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
      // Filter out current user
      availableUsers.value = response.items.filter(
        (user: any) => user.id !== authStore.user?.id
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
  
  if (!valid) return;
  
  isSubmitting.value = true;
  
  try {
    // Prepare members array with roles
    const members = selectedMembers.value.map(userId => ({
      user_id: userId,
      role: 'member'
    }));
    
    // Add current user as owner
    if (authStore.user) {
      members.push({
        user_id: authStore.user.id,
        role: 'owner'
      });
    }
    
    // Emit create event
    emit('create', roomName.value, roomType.value, members);
    
    // Close dialog
    closeDialog();
  } catch (error) {
    console.error('Error creating room:', error);
    notificationService.error('Failed to create room');
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
