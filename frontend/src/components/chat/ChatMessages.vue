<!-- frontend/src/components/chat/ChatMessages.vue -->
<template>
  <div 
    class="messages-container"
    ref="messagesContainer"
    @scroll="handleScroll"
  >
    <div class="load-more" v-if="canLoadMore">
      <v-btn
        variant="text"
        size="small"
        :loading="isLoadingMore"
        @click="loadMore"
      >
        Load older messages
      </v-btn>
    </div>
    
    <div class="messages-list">
      <template v-for="(message, index) in messages" :key="message.id">
        <!-- Date separator -->
        <div 
          v-if="shouldShowDateSeparator(message, index)"
          class="date-separator"
        >
          <div class="date-line"></div>
          <div class="date-text">{{ formatDateSeparator(message.created_at) }}</div>
          <div class="date-line"></div>
        </div>
        
        <!-- Message -->
        <ChatMessage 
          :message="message"
          :is-own-message="message.sender_id === currentUserId"
          :show-sender="shouldShowSender(message, index)"
          @react="handleReaction"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </template>
    </div>
    
    <div class="typing-indicator" v-if="typingUsers.length > 0">
      <v-icon size="small" class="typing-icon">mdi-message-processing</v-icon>
      <span>{{ typingText }}</span>
    </div>
    
    <div ref="bottomAnchor"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUpdated, watch } from 'vue';
import { format, isToday, isYesterday, isSameDay } from 'date-fns';
import { ChatMessage } from '@/types/chat';
import { chatService } from '@/services/chat';
import ChatMessage from './ChatMessage.vue';

const props = defineProps<{
  messages: ChatMessage[];
  roomId: string;
  currentUserId: string;
}>();

const emit = defineEmits<{
  (e: 'load-more', beforeId: string): void;
  (e: 'react', messageId: string, reaction: string, isAdding: boolean): void;
  (e: 'edit', messageId: string, content: string): void;
  (e: 'delete', messageId: string): void;
}>();

// Refs
const messagesContainer = ref<HTMLElement | null>(null);
const bottomAnchor = ref<HTMLElement | null>(null);
const isLoadingMore = ref(false);
const hasReachedTop = ref(false);
const shouldScrollToBottom = ref(true);
const lastHeight = ref(0);
const lastScrollTop = ref(0);

// Computed
const typingUsers = computed(() => {
  return chatService.getTypingUsers(props.roomId);
});

const typingText = computed(() => {
  if (typingUsers.value.length === 0) return '';
  if (typingUsers.value.length === 1) return `${typingUsers.value[0]} is typing...`;
  if (typingUsers.value.length === 2) return `${typingUsers.value[0]} and ${typingUsers.value[1]} are typing...`;
  return 'Several people are typing...';
});

const canLoadMore = computed(() => !hasReachedTop.value && props.messages.length > 0);

// Methods
function handleScroll() {
  if (!messagesContainer.value) return;
  
  // Save current scroll position
  lastScrollTop.value = messagesContainer.value.scrollTop;
  
  // Determine if we should auto-scroll to bottom on new messages
  shouldScrollToBottom.value = 
    messagesContainer.value.scrollHeight - messagesContainer.value.scrollTop - messagesContainer.value.clientHeight < 10;
  
  // Check if reached top for loading more
  if (messagesContainer.value.scrollTop < 50 && props.messages.length > 0 && !isLoadingMore.value) {
    loadMore();
  }
}

function loadMore() {
  if (isLoadingMore.value || props.messages.length === 0) return;
  
  isLoadingMore.value = true;
  const oldestMessage = props.messages[0];
  
  // Save current scroll height
  if (messagesContainer.value) {
    lastHeight.value = messagesContainer.value.scrollHeight;
  }
  
  emit('load-more', oldestMessage.id);
  
  // Reset loading after a timeout in case of error
  setTimeout(() => {
    isLoadingMore.value = false;
  }, 5000);
}

function restoreScrollPosition() {
  if (!messagesContainer.value) return;
  
  // If we loaded more (at top), maintain relative scroll position
  if (isLoadingMore.value && lastHeight.value > 0) {
    const newHeight = messagesContainer.value.scrollHeight;
    const heightDiff = newHeight - lastHeight.value;
    messagesContainer.value.scrollTop = lastScrollTop.value + heightDiff;
    isLoadingMore.value = false;
  }
  // Otherwise scroll to bottom if necessary
  else if (shouldScrollToBottom.value) {
    scrollToBottom();
  }
}

function scrollToBottom() {
  if (bottomAnchor.value) {
    bottomAnchor.value.scrollIntoView({ behavior: 'smooth' });
  }
}

function shouldShowDateSeparator(message: ChatMessage, index: number): boolean {
  if (index === 0) return true;
  
  const currentDate = new Date(message.created_at);
  const prevDate = new Date(props.messages[index - 1].created_at);
  
  return !isSameDay(currentDate, prevDate);
}

function formatDateSeparator(dateStr: string): string {
  const date = new Date(dateStr);
  
  if (isToday(date)) {
    return 'Today';
  } else if (isYesterday(date)) {
    return 'Yesterday';
  } else {
    return format(date, 'MMMM d, yyyy');
  }
}

function shouldShowSender(message: ChatMessage, index: number): boolean {
  // Always show sender for system messages
  if (message.message_type === 'system') return false;
  
  // First message or after date separator
  if (index === 0) return true;
  
  const prevMessage = props.messages[index - 1];
  
  // Different sender or more than 5 minutes gap
  if (prevMessage.sender_id !== message.sender_id) return true;
  
  const timeDiff = new Date(message.created_at).getTime() - new Date(prevMessage.created_at).getTime();
  return timeDiff > 5 * 60 * 1000; // 5 minutes
}

function handleReaction(messageId: string, reaction: string, isAdding: boolean) {
  emit('react', messageId, reaction, isAdding);
}

function handleEdit(messageId: string, content: string) {
  emit('edit', messageId, content);
}

function handleDelete(messageId: string) {
  emit('delete', messageId);
}

// Lifecycle hooks
onMounted(() => {
  scrollToBottom();
});

onUpdated(() => {
  restoreScrollPosition();
});

// Watch for room changes to reset scroll state
watch(() => props.roomId, () => {
  hasReachedTop.value = false;
  shouldScrollToBottom.value = true;
  lastHeight.value = 0;
  lastScrollTop.value = 0;
  
  // Scroll to bottom on room change
  nextTick(() => {
    scrollToBottom();
  });
});

// Watch for new messages to scroll to bottom if needed
watch(() => props.messages.length, () => {
  if (shouldScrollToBottom.value) {
    nextTick(() => {
      scrollToBottom();
    });
  }
});
</script>

<style scoped>
.messages-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.messages-list {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.date-separator {
  display: flex;
  align-items: center;
  margin: 16px 0;
  color: var(--v-on-surface-variant);
  font-size: 0.85rem;
}

.date-line {
  flex-grow: 1;
  height: 1px;
  background-color: var(--v-neutral-200);
}

.date-text {
  padding: 0 16px;
}

.load-more {
  text-align: center;
  padding: 8px 0;
}

.typing-indicator {
  padding: 8px 0;
  font-size: 0.85rem;
  color: var(--v-on-surface-variant);
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.typing-icon {
  margin-right: 8px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}
</style>
