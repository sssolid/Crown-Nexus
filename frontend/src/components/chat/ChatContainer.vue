<!-- frontend/src/components/chat/ChatContainer.vue -->
<template>
  <div class="chat-container">
    <div class="chat-sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h2>Messages</h2>
        <v-btn icon @click="toggleSidebar">
          <v-icon>{{ sidebarCollapsed ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
        </v-btn>
      </div>
      
      <div class="search-bar">
        <v-text-field
          v-model="searchQuery"
          prepend-inner-icon="mdi-magnify"
          placeholder="Search chats"
          variant="outlined"
          density="compact"
          hide-details
          class="mb-2"
        ></v-text-field>
      </div>
      
      <div class="room-list">
        <ChatRoomItem
          v-for="room in filteredRooms"
          :key="room.id"
          :room="room"
          :active="activeRoomId === room.id"
          @click="joinRoom(room.id)"
        />
        
        <div v-if="Object.keys(chatRooms).length === 0" class="no-rooms">
          <p>No chat rooms available</p>
          <v-btn
            color="primary"
            @click="showCreateRoomDialog = true"
          >
            Create Room
          </v-btn>
        </div>
      </div>
      
      <div class="sidebar-actions">
        <v-btn
          block
          color="primary"
          prepend-icon="mdi-plus"
          @click="showCreateRoomDialog = true"
        >
          New Chat
        </v-btn>
      </div>
    </div>
    
    <div class="chat-content">
      <template v-if="activeRoomId && activeRoom">
        <ChatHeader
          :room="activeRoom"
          :online-count="onlineCount"
          @toggle-member-list="showMembersPanel = !showMembersPanel"
        />
        
        <ChatMessages
          :messages="activeRoomMessages"
          :room-id="activeRoomId"
          :current-user-id="currentUserId"
          @load-more="loadMoreMessages"
          @react="handleReaction"
          @edit="editMessage"
          @delete="deleteMessage"
        />
        
        <ChatInput
          :room-id="activeRoomId"
          @send="sendMessage"
          @typing="handleTyping"
        />
      </template>
      
      <div v-else class="no-room-selected">
        <div class="no-room-content">
          <v-icon size="64" color="primary">mdi-chat-outline</v-icon>
          <h3>Select a chat or start a new conversation</h3>
          <v-btn
            color="primary"
            @click="showCreateRoomDialog = true"
          >
            Start New Chat
          </v-btn>
        </div>
      </div>
    </div>
    
    <transition name="slide">
      <div v-if="showMembersPanel && activeRoom" class="members-panel">
        <ChatMembers
          :members="activeRoomMembers"
          :room="activeRoom"
          :current-user-id="currentUserId"
          @close="showMembersPanel = false"
          @add-member="showAddMemberDialog = true"
          @remove-member="confirmRemoveMember"
          @update-role="updateMemberRole"
        />
      </div>
    </transition>
    
    <!-- Dialogs -->
    <ChatRoomDialog
      v-model="showCreateRoomDialog"
      @create="createRoom"
    />
    
    <AddMemberDialog
      v-if="activeRoomId"
      v-model="showAddMemberDialog"
      :room-id="activeRoomId"
      @add="addMember"
    />
    
    <ConfirmDialog
      v-model="showRemoveMemberDialog"
      title="Remove Member"
      :message="`Are you sure you want to remove ${memberToRemove?.user_name || 'this member'} from the chat?`"
      @confirm="removeMemberConfirmed"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { chatService } from '@/services/chat';
import { ChatRoom, ChatMember, ChatRoomType } from '@/types/chat';
import { notificationService } from '@/utils/notification';

// Import components
import ChatRoomItem from './ChatRoomItem.vue';
import ChatHeader from './ChatHeader.vue';
import ChatMessages from './ChatMessages.vue';
import ChatInput from './ChatInput.vue';
import ChatMembers from './ChatMembers.vue';
import ChatRoomDialog from './ChatRoomDialog.vue';
import AddMemberDialog from './AddMemberDialog.vue';
import ConfirmDialog from '@/components/common/ConfirmDialog.vue';

// Reactive state
const searchQuery = ref('');
const sidebarCollapsed = ref(false);
const showMembersPanel = ref(false);
const showCreateRoomDialog = ref(false);
const showAddMemberDialog = ref(false);
const showRemoveMemberDialog = ref(false);
const memberToRemove = ref<ChatMember | null>(null);

// Store access
const authStore = useAuthStore();
const router = useRouter();

// Computed properties
const currentUserId = computed(() => authStore.user?.id || '');

const filteredRooms = computed(() => {
  const rooms = Object.values(chatService.chatRooms);
  
  if (!searchQuery.value) {
    return rooms;
  }
  
  const query = searchQuery.value.toLowerCase();
  return rooms.filter(room => {
    // Search by room name
    if (room.name && room.name.toLowerCase().includes(query)) {
      return true;
    }
    
    // For direct chats without names, search by other user's name
    if (room.type === ChatRoomType.DIRECT && room.last_message) {
      const otherUser = room.last_message.sender_name;
      return otherUser && otherUser.toLowerCase().includes(query);
    }
    
    return false;
  });
});

const activeRoomId = computed(() => chatService.activeRoomId.value);
const activeRoom = computed(() => chatService.activeRoom.value);
const activeRoomMessages = computed(() => chatService.activeRoomMessages.value);
const activeRoomMembers = computed(() => chatService.activeRoomMembers.value);
const chatRooms = computed(() => chatService.chatRooms);

const onlineCount = computed(() => {
  if (!activeRoomMembers.value) return 0;
  return activeRoomMembers.value.filter(m => m.is_online).length;
});

// Methods
function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value;
}

function joinRoom(roomId: string) {
  chatService.joinRoom(roomId);
}

function loadMoreMessages(beforeId: string) {
  if (activeRoomId.value) {
    chatService.fetchMessageHistory(activeRoomId.value, beforeId);
  }
}

function sendMessage(content: string) {
  if (activeRoomId.value) {
    chatService.sendMessage(activeRoomId.value, content);
  }
}

function handleTyping(isTyping: boolean) {
  if (!activeRoomId.value) return;
  
  if (isTyping) {
    chatService.sendTypingStart(activeRoomId.value);
  } else {
    chatService.sendTypingStop(activeRoomId.value);
  }
}

function handleReaction(messageId: string, reaction: string, isAdding: boolean) {
  if (!activeRoomId.value) return;
  
  if (isAdding) {
    chatService.addReaction(messageId, activeRoomId.value, reaction);
  } else {
    chatService.removeReaction(messageId, activeRoomId.value, reaction);
  }
}

function editMessage(messageId: string, content: string) {
  if (activeRoomId.value) {
    chatService.editMessage(messageId, activeRoomId.value, content);
  }
}

function deleteMessage(messageId: string) {
  if (activeRoomId.value) {
    chatService.deleteMessage(messageId, activeRoomId.value);
  }
}

async function createRoom(name: string, type: ChatRoomType, members: any[]) {
  const room = await chatService.createRoom(name, type, members);
  
  if (room) {
    showCreateRoomDialog.value = false;
    joinRoom(room.id);
  }
}

async function addMember(userId: string, role: string) {
  if (!activeRoomId.value) return;
  
  const success = await chatService.addMember(activeRoomId.value, userId, role);
  
  if (success) {
    showAddMemberDialog.value = false;
    notificationService.success('Member added successfully');
  }
}

function confirmRemoveMember(member: ChatMember) {
  memberToRemove.value = member;
  showRemoveMemberDialog.value = true;
}

async function removeMemberConfirmed() {
  if (!activeRoomId.value || !memberToRemove.value) return;
  
  const success = await chatService.removeMember(
    activeRoomId.value,
    memberToRemove.value.user_id
  );
  
  if (success) {
    notificationService.success('Member removed successfully');
  }
  
  memberToRemove.value = null;
}

async function updateMemberRole(userId: string, role: string) {
  if (!activeRoomId.value) return;
  
  const success = await chatService.updateMemberRole(activeRoomId.value, userId, role);
  
  if (success) {
    notificationService.success('Member role updated');
  }
}

// Lifecycle hooks
onMounted(() => {
  // Initialize chat service
  chatService.initialize();
  
  // Check if URL contains room ID to open
  const roomId = router.currentRoute.value.query.room as string;
  if (roomId) {
    joinRoom(roomId);
  }
});

// Watch for route changes to open rooms from URL
watch(
  () => router.currentRoute.value.query.room,
  (newRoomId) => {
    if (newRoomId && typeof newRoomId === 'string') {
      joinRoom(newRoomId);
    }
  }
);
</script>

<style scoped>
.chat-container {
  display: flex;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: var(--v-surface-base);
}

.chat-sidebar {
  width: 320px;
  border-right: 1px solid var(--v-neutral-200);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--v-neutral-200);
}

.search-bar {
  padding: 12px 16px;
}

.room-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 8px;
}

.sidebar-actions {
  padding: 16px;
  border-top: 1px solid var(--v-neutral-200);
}

.chat-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.no-room-selected {
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: center;
  background-color: var(--v-surface-variant);
}

.no-room-content {
  text-align: center;
  max-width: 300px;
}

.no-room-content h3 {
  margin: 16px 0;
  color: var(--v-on-surface-variant);
}

.no-rooms {
  text-align: center;
  padding: 32px 16px;
  color: var(--v-on-surface-variant);
}

.members-panel {
  width: 280px;
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  background-color: var(--v-surface-base);
  border-left: 1px solid var(--v-neutral-200);
  z-index: 2;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
