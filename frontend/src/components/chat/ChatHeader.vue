<!-- frontend/src/components/chat/ChatHeader.vue -->
<template>
  <div class="chat-header">
    <div class="room-info">
      <v-avatar color="primary" size="40" class="mr-3">
        <span class="room-avatar-text">{{ avatarText }}</span>
      </v-avatar>

      <div class="room-details">
        <h3 class="room-name">{{ displayName }}</h3>
        <div class="room-meta">
          <v-icon size="small" color="success" v-if="onlineCount > 0">mdi-circle</v-icon>
          <span class="online-status">{{ statusText }}</span>
        </div>
      </div>
    </div>

    <div class="header-actions">
      <v-btn
        icon
        variant="text"
        @click="$emit('toggle-member-list')"
        v-tooltip="'View members'"
      >
        <v-icon>mdi-account-multiple</v-icon>
        <v-badge
          :content="onlineCount.toString()"
          :value="onlineCount > 0"
          color="success"
          offset-x="12"
          offset-y="12"
        ></v-badge>
      </v-btn>

      <v-menu location="bottom end">
        <template v-slot:activator="{ props }">
          <v-btn icon variant="text" v-bind="props">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list density="compact">
          <v-list-item
            prepend-icon="mdi-information-outline"
            title="Room Info"
            @click="showRoomInfo = true"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-bell-outline"
            title="Notification Settings"
            @click="showNotificationSettings = true"
          ></v-list-item>

          <v-divider></v-divider>

          <v-list-item
            v-if="canLeaveRoom"
            prepend-icon="mdi-exit-to-app"
            title="Leave Room"
            @click="confirmLeaveRoom"
            class="text-error"
          ></v-list-item>
        </v-list>
      </v-menu>
    </div>

    <!-- Room Info Dialog -->
    <v-dialog v-model="showRoomInfo" max-width="500">
      <v-card>
        <v-card-title>Room Information</v-card-title>
        <v-card-text>
          <div class="room-info-item">
            <div class="info-label">Name:</div>
            <div class="info-value">{{ room.name || 'Unnamed Room' }}</div>
          </div>

          <div class="room-info-item">
            <div class="info-label">Type:</div>
            <div class="info-value">{{ roomTypeDisplay }}</div>
          </div>

          <div class="room-info-item">
            <div class="info-label">Created:</div>
            <div class="info-value">{{ formatDate(room.created_at) }}</div>
          </div>

          <div class="room-info-item">
            <div class="info-label">Member Count:</div>
            <div class="info-value">{{ room.member_count || 0 }}</div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showRoomInfo = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Notification Settings Dialog -->
    <v-dialog v-model="showNotificationSettings" max-width="500">
      <v-card>
        <v-card-title>Notification Settings</v-card-title>
        <v-card-text>
          <v-radio-group v-model="notificationLevel">
            <v-radio value="all" label="All messages"></v-radio>
            <v-radio value="mentions" label="Only mentions and direct messages"></v-radio>
            <v-radio value="none" label="None"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showNotificationSettings = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveNotificationSettings">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Leave Room Confirmation Dialog -->
    <v-dialog v-model="showLeaveDialog" max-width="400">
      <v-card>
        <v-card-title>Leave Room</v-card-title>
        <v-card-text>
          Are you sure you want to leave this room? You'll need to be invited back to rejoin.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showLeaveDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="leaveRoom">Leave</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { format } from 'date-fns';
import { ChatRoom, ChatRoomType } from '@/types/chat';
import { chatService } from '@/services/chat';
import { notificationService } from '@/utils/notification';
import { useAuthStore } from '@/stores/auth';

const props = defineProps<{
  room: ChatRoom;
  onlineCount: number;
}>();

const emit = defineEmits<{
  (e: 'toggle-member-list'): void;
}>();

// State
const showRoomInfo = ref(false);
const showNotificationSettings = ref(false);
const showLeaveDialog = ref(false);
const notificationLevel = ref('all'); // Default notification level

// Store
const authStore = useAuthStore();

// Computed properties
const avatarText = computed(() => {
  if (props.room.type === ChatRoomType.DIRECT) {
    // For direct chats, use the other user's initials
    const otherUser = props.room.last_message?.sender_name;
    if (otherUser) {
      return otherUser
        .split(' ')
        .map(n => n[0])
        .join('')
        .slice(0, 2)
        .toUpperCase();
    }
  }

  if (props.room.name) {
    return props.room.name
      .split(' ')
      .map(n => n[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();
  }

  return props.room.type.slice(0, 1).toUpperCase();
});

const isDirect = computed(() => {
  return props.room.type === ChatRoomType.DIRECT;
});

const displayName = computed(() => {
  if (isDirect.value) {
    return props.room.last_message?.sender_name || 'Direct Message';
  }

  return props.room.name || `${props.room.type} Chat`;
});

const statusText = computed(() => {
  if (isDirect.value) {
    return props.onlineCount > 0 ? 'Online' : 'Offline';
  }

  return `${props.onlineCount} online`;
});

const roomTypeDisplay = computed(() => {
  switch (props.room.type) {
    case ChatRoomType.DIRECT:
      return 'Direct Message';
    case ChatRoomType.GROUP:
      return 'Group Chat';
    case ChatRoomType.COMPANY:
      return 'Company-wide Chat';
    default:
      return props.room.type;
  }
});

const canLeaveRoom = computed(() => {
  // Can't leave direct messages
  if (props.room.type === ChatRoomType.DIRECT) {
    return false;
  }

  // Can leave group chats
  return true;
});

// Methods
function formatDate(dateStr: string): string {
  return format(new Date(dateStr), 'MMMM d, yyyy • h:mm a');
}

function confirmLeaveRoom() {
  showLeaveDialog.value = true;
}

async function leaveRoom() {
  try {
    await chatService.leaveRoom(props.room.id);
    notificationService.success('You have left the room');
    showLeaveDialog.value = false;
  } catch (error) {
    console.error('Error leaving room:', error);
    notificationService.error('Failed to leave room');
  }
}

async function saveNotificationSettings() {
  try {
    // Implementation would depend on your API
    // await chatService.updateRoomNotificationSettings(props.room.id, notificationLevel.value);
    notificationService.success('Notification settings updated');
    showNotificationSettings.value = false;
  } catch (error) {
    console.error('Error updating notification settings:', error);
    notificationService.error('Failed to update notification settings');
  }
}
</script>

<style scoped>
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--v-neutral-200);
  background-color: var(--v-surface-base);
}

.room-info {
  display: flex;
  align-items: center;
}

.room-avatar-text {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.room-details {
  display: flex;
  flex-direction: column;
}

.room-name {
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

.room-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  color: var(--v-on-surface-variant);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.room-info-item {
  display: flex;
  margin-bottom: 12px;
}

.info-label {
  font-weight: 500;
  width: 120px;
  color: var(--v-on-surface-variant);
}

.info-value {
  flex-grow: 1;
}
</style>
