<!-- frontend/src/components/chat/ChatRoomItem.vue -->
<template>
  <div 
    class="room-item"
    :class="{ 'active': active }"
    @click="$emit('click')"
  >
    <div class="room-avatar">
      <v-badge
        :content="room.unread_count"
        :value="room.unread_count && room.unread_count > 0"
        color="error"
      >
        <v-avatar color="primary" size="40">
          <span class="room-avatar-text">{{ avatarText }}</span>
        </v-avatar>
      </v-badge>
    </div>
    
    <div class="room-details">
      <div class="room-header">
        <div class="room-name">{{ displayName }}</div>
        <div class="room-time">{{ formattedTime }}</div>
      </div>
      
      <div class="room-preview">
        <div class="message-preview">{{ messagePreview }}</div>
        <div class="member-count" v-if="!isDirect">
          <v-icon size="small">mdi-account-multiple</v-icon>
          {{ room.member_count }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { format, isToday, isYesterday } from 'date-fns';
import { ChatRoom, ChatRoomType } from '@/types/chat';

const props = defineProps<{
  room: ChatRoom;
  active: boolean;
}>();

// Emits
defineEmits<{
  (e: 'click'): void;
}>();

// Computed properties
const avatarText = computed(() => {
  if (props.room.type === ChatRoomType.DIRECT) {
    // For direct chats, use the other user's initials
    const otherUser = getOtherUserName();
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
    return getOtherUserName() || 'Direct Message';
  }
  
  return props.room.name || `${props.room.type} Chat`;
});

const messagePreview = computed(() => {
  if (!props.room.last_message) {
    return 'No messages yet';
  }
  
  if (props.room.last_message.is_deleted) {
    return 'This message was deleted';
  }
  
  if (props.room.last_message.message_type === 'image') {
    return '📷 Image';
  }
  
  if (props.room.last_message.message_type === 'file') {
    return '📎 File';
  }
  
  if (props.room.last_message.message_type === 'system') {
    return props.room.last_message.content;
  }
  
  // For text messages, limit the preview length
  let preview = props.room.last_message.content;
  if (preview.length > 30) {
    preview = preview.substring(0, 30) + '...';
  }
  
  return preview;
});

const formattedTime = computed(() => {
  if (!props.room.last_message) {
    return '';
  }
  
  const date = new Date(props.room.last_message.created_at);
  
  if (isToday(date)) {
    return format(date, 'h:mm a');
  } else if (isYesterday(date)) {
    return 'Yesterday';
  } else {
    return format(date, 'MM/dd/yy');
  }
});

// Methods
function getOtherUserName(): string | null {
  if (!props.room.last_message) return null;
  
  // In direct chats, the sender name is likely the other user
  return props.room.last_message.sender_name;
}
</script>

<style scoped>
.room-item {
  display: flex;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.room-item:hover {
  background-color: var(--v-neutral-100);
}

.room-item.active {
  background-color: var(--v-primary-lighten-5);
}

.room-avatar {
  margin-right: 12px;
}

.room-avatar-text {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.room-details {
  flex-grow: 1;
  overflow: hidden;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.room-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.room-time {
  font-size: 0.8rem;
  color: var(--v-on-surface-variant);
  white-space: nowrap;
  margin-left: 8px;
}

.room-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-preview {
  font-size: 0.85rem;
  color: var(--v-on-surface-variant);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.member-count {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--v-on-surface-variant);
  margin-left: 8px;
}
</style>
