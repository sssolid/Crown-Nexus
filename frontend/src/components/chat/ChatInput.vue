<!-- frontend/src/components/chat/ChatInput.vue -->
<template>
  <div class="chat-input-container">
    <div class="typing-indicator" v-if="typingUsers.length > 0">
      <span>{{ typingText }}</span>
    </div>
    
    <div class="input-wrapper">
      <v-icon
        v-if="showAttachmentButton"
        class="attachment-button"
        @click="$refs.fileInput.click()"
      >
        mdi-paperclip
      </v-icon>
      
      <input
        ref="fileInput"
        type="file"
        style="display: none"
        @change="handleFileSelected"
      >
      
      <v-textarea
        v-model="messageText"
        class="message-textarea"
        placeholder="Type a message..."
        auto-grow
        rows="1"
        max-rows="6"
        variant="outlined"
        hide-details
        density="comfortable"
        @keydown="handleKeydown"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
      ></v-textarea>
      
      <v-btn
        icon
        color="primary"
        class="send-button"
        :disabled="!canSend"
        @click="sendMessage"
      >
        <v-icon>mdi-send</v-icon>
      </v-btn>
    </div>

    <!-- Attachment preview -->
    <div class="attachment-preview" v-if="attachment">
      <div class="preview-content">
        <v-icon class="file-icon">{{ fileIcon }}</v-icon>
        <span class="file-name">{{ attachment.name }}</span>
        <span class="file-size">({{ formatFileSize(attachment.size) }})</span>
      </div>
      
      <v-btn icon size="small" @click="clearAttachment">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { chatService } from '@/services/chat';
import { MessageType } from '@/types/chat';

const props = defineProps<{
  roomId: string;
}>();

const emit = defineEmits<{
  (e: 'send', content: string, messageType?: string, file?: File): void;
  (e: 'typing', isTyping: boolean): void;
}>();

// Refs
const messageText = ref('');
const isTyping = ref(false);
const typingTimeout = ref<number | null>(null);
const attachment = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

// Computed
const canSend = computed(() => {
  return (messageText.value.trim() !== '' || attachment.value !== null);
});

const typingUsers = computed(() => {
  return chatService.getTypingUsers(props.roomId);
});

const typingText = computed(() => {
  if (typingUsers.value.length === 0) return '';
  if (typingUsers.value.length === 1) return `${typingUsers.value[0]} is typing...`;
  if (typingUsers.value.length === 2) return `${typingUsers.value[0]} and ${typingUsers.value[1]} are typing...`;
  return 'Several people are typing...';
});

const showAttachmentButton = computed(() => {
  return !attachment.value;
});

const fileIcon = computed(() => {
  if (!attachment.value) return 'mdi-file-outline';
  
  const type = attachment.value.type;
  if (type.startsWith('image/')) return 'mdi-file-image-outline';
  if (type.startsWith('video/')) return 'mdi-file-video-outline';
  if (type.includes('pdf')) return 'mdi-file-pdf-outline';
  if (type.includes('spreadsheet') || type.includes('excel')) return 'mdi-file-excel-outline';
  if (type.includes('document') || type.includes('word')) return 'mdi-file-word-outline';
  
  return 'mdi-file-outline';
});

// Methods
function sendMessage() {
  if (!canSend.value) return;
  
  if (attachment.value) {
    // Handle file upload
    const messageType = getMessageType(attachment.value);
    emit('send', messageText.value, messageType, attachment.value);
    clearAttachment();
  } else {
    // Send regular text message
    emit('send', messageText.value);
  }
  
  // Clear input
  messageText.value = '';
  stopTyping();
}

function getMessageType(file: File): MessageType {
  const type = file.type;
  if (type.startsWith('image/')) return MessageType.IMAGE;
  return MessageType.FILE;
}

function handleKeydown(event: KeyboardEvent) {
  // Send on Enter without Shift
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

function handleInput() {
  if (messageText.value.trim() !== '') {
    if (!isTyping.value) {
      startTyping();
    }
    
    // Reset typing timeout
    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value);
    }
    
    typingTimeout.value = window.setTimeout(() => {
      stopTyping();
    }, 2000);
  } else if (isTyping.value) {
    stopTyping();
  }
}

function startTyping() {
  isTyping.value = true;
  emit('typing', true);
}

function stopTyping() {
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
    typingTimeout.value = null;
  }
  
  if (isTyping.value) {
    isTyping.value = false;
    emit('typing', false);
  }
}

function handleFocus() {
  // Additional focus handling if needed
}

function handleBlur() {
  // Stop typing indicator when input loses focus
  stopTyping();
}

function handleFileSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  
  if (input.files && input.files.length > 0) {
    attachment.value = input.files[0];
  }
  
  // Reset file input
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

function clearAttachment() {
  attachment.value = null;
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Clean up typing timeout on component unmount
onBeforeUnmount(() => {
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
  }
  
  if (isTyping.value) {
    emit('typing', false);
  }
});

// Reset state when room changes
watch(() => props.roomId, () => {
  messageText.value = '';
  isTyping.value = false;
  attachment.value = null;
  
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
    typingTimeout.value = null;
  }
});
</script>

<style scoped>
.chat-input-container {
  padding: 8px 16px 16px;
  border-top: 1px solid var(--v-neutral-200);
  background-color: var(--v-surface-base);
}

.typing-indicator {
  font-size: 0.8rem;
  color: var(--v-on-surface-variant);
  padding: 4px 0;
  min-height: 24px;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  background-color: var(--v-surface-variant);
  border-radius: 8px;
  overflow: hidden;
}

.attachment-button {
  margin: 8px;
  cursor: pointer;
  color: var(--v-on-surface-variant);
}

.message-textarea {
  flex-grow: 1;
}

.send-button {
  margin: 8px;
}

.attachment-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--v-neutral-100);
  border-radius: 8px;
  padding: 8px 12px;
  margin-top: 8px;
}

.preview-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-icon {
  color: var(--v-primary);
}

.file-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.file-size {
  font-size: 0.8rem;
  color: var(--v-on-surface-variant);
}
</style>
