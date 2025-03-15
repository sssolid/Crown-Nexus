<!-- frontend/src/views/ChatPage.vue -->
<template>
  <div class="chat-page">
    <ChatContainer />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue';
import ChatContainer from '@/components/chat/ChatContainer.vue';
import { chatService } from '@/services/chat';

// Initialize chat service when the page loads
onMounted(() => {
  chatService.initialize();
});

// Clean up when leaving the page
onBeforeUnmount(() => {
  chatService.disconnectWebSocket();
});
</script>

<style scoped>
.chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
