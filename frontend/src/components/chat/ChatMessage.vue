<!-- frontend/src/components/chat/ChatMessage.vue -->
<template>
  <div 
    class="message-wrapper"
    :class="{
      'own-message': isOwnMessage,
      'system-message': message.message_type === 'system',
      'deleted-message': message.is_deleted
    }"
  >
    <div 
      v-if="showSender && message.sender_name && message.message_type !== 'system'" 
      class="message-sender"
    >
      {{ message.sender_name }}
    </div>
    
    <div class="message-content-wrapper">
      <div class="avatar" v-if="!isOwnMessage && message.message_type !== 'system'">
        <v-avatar 
          color="primary" 
          size="36"
          :class="{ 'no-sender': !showSender }"
        >
          {{ avatarInitials }}
        </v-avatar>
      </div>
      
      <div class="message-bubble">
        <template v-if="isEditing">
          <v-textarea
            v-model="editContent"
            auto-grow
            rows="1"
            variant="outlined"
            density="compact"
            hide-details
            @keydown.esc="cancelEdit"
            @keydown.enter.exact.prevent="saveEdit"
          ></v-textarea>
          
          <div class="edit-actions">
            <v-btn size="small" variant="text" @click="cancelEdit">Cancel</v-btn>
            <v-btn size="small" color="primary" @click="saveEdit">Save</v-btn>
          </div>
        </template>
        
        <template v-else>
          <div v-if="message.message_type === 'image'" class="message-image">
            <img :src="message.content" alt="Image message" />
          </div>
          
          <div v-else-if="message.message_type === 'file'" class="message-file">
            <v-icon>mdi-file-outline</v-icon>
            <a :href="message.content" target="_blank" download>
              {{ message.metadata.filename || 'Download file' }}
            </a>
          </div>
          
          <div v-else class="message-text">
            {{ message.content }}
          </div>
          
          <div class="message-meta">
            <span v-if="message.is_edited" class="edited-indicator">edited</span>
            <span class="message-time">{{ formatTime(message.created_at) }}</span>
          </div>
        </template>
      </div>
    </div>
    
    <div class="message-actions" v-if="!isEditing && !message.is_deleted">
      <v-menu
        v-model="showReactionMenu"
        location="top"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            icon
            size="small"
            variant="text"
            class="action-button"
          >
            <v-icon>mdi-emoticon-outline</v-icon>
          </v-btn>
        </template>
        <div class="reaction-menu">
          <button 
            v-for="reaction in availableReactions" 
            :key="reaction"
            class="reaction-button"
            @click="addReaction(reaction)"
          >
            {{ reaction }}
          </button>
        </div>
      </v-menu>
      
      <v-btn
        v-if="canEdit"
        icon
        size="small"
        variant="text"
        class="action-button"
        @click="startEdit"
      >
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      
      <v-btn
        v-if="canDelete"
        icon
        size="small"
        variant="text"
        class="action-button"
        @click="confirmDelete"
      >
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </div>
    
    <div v-if="hasReactions" class="message-reactions">
      <div
        v-for="(users, reaction) in message.reactions"
        :key="reaction"
        class="reaction-badge"
        :class="{ 'own-reaction': users.includes(currentUserId) }"
        @click="toggleReaction(reaction, users)"
      >
        <span class="reaction-emoji">{{ reaction }}</span>
        <span class="reaction-count">{{ users.length }}</span>
      </div>
    </div>
    
    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Delete Message</v-card-title>
        <v-card-text>
          Are you sure you want to delete this message? This cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteMessage">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { format } from 'date-fns';
import { ChatMessage } from '@/types/chat';
import { useAuthStore } from '@/stores/auth';

const props = defineProps<{
  message: ChatMessage;
  isOwnMessage: boolean;
  showSender: boolean;
}>();

const emit = defineEmits<{
  (e: 'react', messageId: string, reaction: string, isAdding: boolean): void;
  (e: 'edit', messageId: string, content: string): void;
  (e: 'delete', messageId: string): void;
}>();

const authStore = useAuthStore();
const currentUserId = computed(() => authStore.user?.id || '');

// State
const isEditing = ref(false);
const editContent = ref('');
const showReactionMenu = ref(false);
const showDeleteDialog = ref(false);

// Available reactions
const availableReactions = ['👍', '❤️', '😂', '😮', '😢', '👏', '🎉', '🤔'];

// Computed properties
const avatarInitials = computed(() => {
  if (!props.message.sender_name) return '';
  
  return props.message.sender_name
    .split(' ')
    .map(n => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
});

const hasReactions = computed(() => {
  return Object.keys(props.message.reactions).length > 0;
});

const canEdit = computed(() => {
  return (
    props.isOwnMessage && 
    !props.message.is_deleted && 
    props.message.message_type === 'text'
  );
});

const canDelete = computed(() => {
  return (
    props.isOwnMessage && 
    !props.message.is_deleted
  );
});

// Methods
function formatTime(dateStr: string): string {
  return format(new Date(dateStr), 'h:mm a');
}

function startEdit() {
  if (!canEdit.value) return;
  
  editContent.value = props.message.content;
  isEditing.value = true;
}

function cancelEdit() {
  isEditing.value = false;
  editContent.value = '';
}

function saveEdit() {
  if (editContent.value.trim() === '') {
    return;
  }
  
  if (editContent.value !== props.message.content) {
    emit('edit', props.message.id, editContent.value);
  }
  
  isEditing.value = false;
}

function confirmDelete() {
  showDeleteDialog.value = true;
}

function deleteMessage() {
  emit('delete', props.message.id);
  showDeleteDialog.value = false;
}

function addReaction(reaction: string) {
  showReactionMenu.value = false;
  
  // Check if user already reacted with this emoji
  const hasReacted = props.message.reactions[reaction]?.includes(currentUserId.value);
  
  emit('react', props.message.id, reaction, !hasReacted);
}

function toggleReaction(reaction: string, users: string[]) {
  const hasReacted = users.includes(currentUserId.value);
  emit('react', props.message.id, reaction, !hasReacted);
}
</script>

<style scoped>
.message-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
  position: relative;
  max-width: 70%;
}

.own-message {
  align-self: flex-end;
}

.system-message {
  align-self: center;
  max-width: 90%;
}

.message-sender {
  font-size: 0.8rem;
  margin-left: 52px;
  margin-bottom: 2px;
  font-weight: 500;
  color: var(--v-on-surface-variant);
}

.message-content-wrapper {
  display: flex;
}

.avatar {
  margin-right: 8px;
  align-self: flex-end;
}

.avatar.no-sender {
  opacity: 0;
  visibility: hidden;
}

.message-bubble {
  padding: 8px 12px;
  border-radius: 12px;
  background-color: var(--v-neutral-100);
  position: relative;
  min-width: 40px;
}

.own-message .message-bubble {
  background-color: var(--v-primary);
  color: var(--v-on-primary);
}

.system-message .message-bubble {
  background-color: var(--v-info);
  color: var(--v-on-info);
  padding: 6px 12px;
  font-size: 0.85rem;
  border-radius: 16px;
}

.deleted-message .message-bubble {
  opacity: 0.7;
  font-style: italic;
}

.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-image img {
  max-width: 100%;
  border-radius: 8px;
}

.message-file {
  display: flex;
  align-items: center;
  gap: 8px;
}

.message-meta {
  display: flex;
  justify-content: flex-end;
  font-size: 0.7rem;
  margin-top: 4px;
  opacity: 0.7;
}

.edited-indicator {
  margin-right: 6px;
}

.message-actions {
  position: absolute;
  right: 0;
  top: -16px;
  display: flex;
  background-color: var(--v-surface-base);
  border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: opacity 0.2s;
  z-index: 1;
}

.message-wrapper:hover .message-actions {
  opacity: 1;
}

.action-button {
  margin: 0 2px;
}

.message-reactions {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 4px;
}

.reaction-badge {
  display: inline-flex;
  align-items: center;
  background-color: var(--v-neutral-100);
  border-radius: 12px;
  padding: 2px 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.own-reaction {
  background-color: var(--v-primary-lighten-4);
}

.reaction-emoji {
  margin-right: 4px;
}

.reaction-count {
  font-size: 0.7rem;
}

.reaction-menu {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.reaction-button {
  border: none;
  background: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: transform 0.1s;
}

.reaction-button:hover {
  background-color: var(--v-neutral-100);
  transform: scale(1.2);
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
