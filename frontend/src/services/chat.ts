// frontend/src/services/chat.ts
import { ref, reactive, computed, ComputedRef } from 'vue';
import api from '@/services/api';
import { 
  ChatRoom, 
  ChatMessage, 
  ChatMember,
  ChatRoomType,
  ChatMemberRole,
  MessageType,
  WebSocketCommand,
  WebSocketResponse,
  UserPresence
} from '@/types/chat';
import { useAuthStore } from '@/stores/auth';
import { notificationService } from '@/utils/notification';

// State variables
const chatRooms = reactive<Record<string, ChatRoom>>({});
const activeRoomId = ref<string | null>(null);
const messages = reactive<Record<string, ChatMessage[]>>({});
const members = reactive<Record<string, ChatMember[]>>({});
const isLoading = ref(false);
const wsConnection = ref<WebSocket | null>(null);
const connectionStatus = ref<'connected' | 'connecting' | 'disconnected'>('disconnected');
const userPresence = reactive<Record<string, UserPresence>>({});
const userTyping = reactive<Record<string, Record<string, number>>>({});

// Connection retry variables
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
const reconnectDelay = 2000; // 2 seconds initial delay
let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

// Computed properties
const activeRoom: ComputedRef<ChatRoom | null> = computed(() => {
  if (!activeRoomId.value) return null;
  return chatRooms[activeRoomId.value] || null;
});

const activeRoomMessages: ComputedRef<ChatMessage[]> = computed(() => {
  if (!activeRoomId.value) return [];
  return messages[activeRoomId.value] || [];
});

const activeRoomMembers: ComputedRef<ChatMember[]> = computed(() => {
  if (!activeRoomId.value) return [];
  return members[activeRoomId.value] || [];
});

const totalUnreadCount: ComputedRef<number> = computed(() => {
  return Object.values(chatRooms).reduce((total, room) => {
    return total + (room.unread_count || 0);
  }, 0);
});

// Chat service functions
export function useChatService() {
  const authStore = useAuthStore();
  
  /**
   * Connect to the WebSocket server
   */
  function connectWebSocket() {
    if (wsConnection.value && wsConnection.value.readyState < 2) {
      // Already connected or connecting
      return;
    }
    
    if (!authStore.token) {
      console.error('Cannot connect WebSocket: No auth token');
      connectionStatus.value = 'disconnected';
      return;
    }
    
    try {
      // Build WebSocket URL with authentication token
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      const wsUrl = `${protocol}//${host}/api/v1/ws/chat?token=${authStore.token}`;
      
      connectionStatus.value = 'connecting';
      wsConnection.value = new WebSocket(wsUrl);
      
      // Set up event handlers
      wsConnection.value.onopen = handleWebSocketOpen;
      wsConnection.value.onmessage = handleWebSocketMessage;
      wsConnection.value.onclose = handleWebSocketClose;
      wsConnection.value.onerror = handleWebSocketError;
    } catch (error) {
      console.error('WebSocket connection error:', error);
      connectionStatus.value = 'disconnected';
    }
  }
  
  /**
   * Disconnect from the WebSocket server
   */
  function disconnectWebSocket() {
    if (wsConnection.value && wsConnection.value.readyState < 2) {
      wsConnection.value.close();
    }
    
    // Clear reconnect timer if active
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    
    wsConnection.value = null;
    connectionStatus.value = 'disconnected';
  }
  
  /**
   * Handle WebSocket connection open
   */
  function handleWebSocketOpen() {
    console.log('WebSocket connected');
    connectionStatus.value = 'connected';
    reconnectAttempts = 0; // Reset reconnect counter on successful connection
    
    // Join active room if any
    if (activeRoomId.value) {
      joinRoom(activeRoomId.value);
    }
  }
  
  /**
   * Handle WebSocket connection close
   */
  function handleWebSocketClose(event: CloseEvent) {
    console.log(`WebSocket closed: ${event.code} ${event.reason}`);
    connectionStatus.value = 'disconnected';
    wsConnection.value = null;
    
    // Attempt to reconnect if not closed intentionally
    if (event.code !== 1000) {
      attemptReconnect();
    }
  }
  
  /**
   * Handle WebSocket error
   */
  function handleWebSocketError(event: Event) {
    console.error('WebSocket error:', event);
    // Error handling is done in onclose handler
  }
  
  /**
   * Attempt to reconnect to WebSocket server with exponential backoff
   */
  function attemptReconnect() {
    if (reconnectAttempts >= maxReconnectAttempts) {
      console.error('Maximum reconnect attempts reached');
      notificationService.error('Connection lost. Please refresh the page.');
      return;
    }
    
    reconnectAttempts++;
    const delay = reconnectDelay * Math.pow(1.5, reconnectAttempts - 1);
    
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${reconnectAttempts})`);
    
    reconnectTimer = setTimeout(() => {
      console.log(`Reconnecting... (attempt ${reconnectAttempts})`);
      connectWebSocket();
    }, delay);
  }
  
  /**
   * Handle incoming WebSocket messages
   */
  function handleWebSocketMessage(event: MessageEvent) {
    try {
      const response: WebSocketResponse = JSON.parse(event.data);
      
      // Process message based on type
      switch (response.type) {
        case 'connected':
          handleConnectedMessage(response);
          break;
        
        case 'room_list':
          handleRoomListMessage(response);
          break;
        
        case 'room_joined':
          handleRoomJoinedMessage(response);
          break;
        
        case 'user_joined':
          handleUserJoinedMessage(response);
          break;
        
        case 'user_left':
          handleUserLeftMessage(response);
          break;
        
        case 'new_message':
          handleNewMessageMessage(response);
          break;
        
        case 'message_sent':
          handleMessageSentMessage(response);
          break;
        
        case 'message_history':
          handleMessageHistoryMessage(response);
          break;
        
        case 'user_typing':
          handleUserTypingMessage(response);
          break;
        
        case 'user_typing_stopped':
          handleUserTypingStoppedMessage(response);
          break;
        
        case 'reaction_added':
          handleReactionAddedMessage(response);
          break;
        
        case 'reaction_removed':
          handleReactionRemovedMessage(response);
          break;
        
        case 'message_edited':
          handleMessageEditedMessage(response);
          break;
        
        case 'message_deleted':
          handleMessageDeletedMessage(response);
          break;
        
        case 'error':
          handleErrorMessage(response);
          break;
        
        default:
          console.warn(`Unknown message type: ${response.type}`, response);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error, event.data);
    }
  }
  
  /**
   * Handle 'connected' WebSocket message
   */
  function handleConnectedMessage(response: WebSocketResponse) {
    console.log('Connected to chat server', response.data);
  }
  
  /**
   * Handle 'room_list' WebSocket message
   */
  function handleRoomListMessage(response: WebSocketResponse) {
    const rooms = response.data.rooms as ChatRoom[];
    
    // Update room list
    rooms.forEach(room => {
      chatRooms[room.id] = room;
    });
  }
  
  /**
   * Handle 'room_joined' WebSocket message
   */
  function handleRoomJoinedMessage(response: WebSocketResponse) {
    const roomInfo = response.data as ChatRoom;
    
    // Update room data
    chatRooms[roomInfo.id] = roomInfo;
    
    // Update members
    if (roomInfo.members) {
      members[roomInfo.id] = roomInfo.members;
    }
    
    // Fetch message history if this is the active room
    if (activeRoomId.value === roomInfo.id) {
      fetchMessageHistory(roomInfo.id);
    }
  }
  
  /**
   * Handle 'user_joined' WebSocket message
   */
  function handleUserJoinedMessage(response: WebSocketResponse) {
    const { room_id, user } = response.data;
    
    // Update room member count
    if (chatRooms[room_id]) {
      chatRooms[room_id].member_count = (chatRooms[room_id].member_count || 0) + 1;
    }
    
    // Add to room members if we have the member list
    if (members[room_id]) {
      const existingMember = members[room_id].find(m => m.user_id === user.id);
      
      if (!existingMember) {
        members[room_id].push({
          user_id: user.id,
          user_name: user.name,
          role: ChatMemberRole.MEMBER,
          is_online: true
        });
      } else {
        // Update existing member's online status
        existingMember.is_online = true;
      }
    }
    
    // Add system message
    if (messages[room_id]) {
      const systemMessage: ChatMessage = {
        id: `system-${Date.now()}`,
        room_id,
        sender_id: null,
        sender_name: null,
        message_type: MessageType.SYSTEM,
        content: `${user.name} joined the room`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_edited: false,
        is_deleted: false,
        reactions: {},
        metadata: {}
      };
      
      messages[room_id].push(systemMessage);
    }
  }
  
  /**
   * Handle 'user_left' WebSocket message
   */
  function handleUserLeftMessage(response: WebSocketResponse) {
    const { room_id, user_id } = response.data;
    
    // Update room member count
    if (chatRooms[room_id]) {
      chatRooms[room_id].member_count = Math.max(0, (chatRooms[room_id].member_count || 1) - 1);
    }
    
    // Update member list if we have it
    if (members[room_id]) {
      const memberIndex = members[room_id].findIndex(m => m.user_id === user_id);
      
      if (memberIndex !== -1) {
        const userName = members[room_id][memberIndex].user_name;
        members[room_id].splice(memberIndex, 1);
        
        // Add system message
        if (messages[room_id]) {
          const systemMessage: ChatMessage = {
            id: `system-${Date.now()}`,
            room_id,
            sender_id: null,
            sender_name: null,
            message_type: MessageType.SYSTEM,
            content: `${userName} left the room`,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            is_edited: false,
            is_deleted: false,
            reactions: {},
            metadata: {}
          };
          
          messages[room_id].push(systemMessage);
        }
      }
    }
  }
  
  /**
   * Handle 'new_message' WebSocket message
   */
  function handleNewMessageMessage(response: WebSocketResponse) {
    const messageData = response.data as ChatMessage;
    
    // Add message to room
    if (!messages[messageData.room_id]) {
      messages[messageData.room_id] = [];
    }
    
    messages[messageData.room_id].push(messageData);
    
    // Update room's last message
    if (chatRooms[messageData.room_id]) {
      chatRooms[messageData.room_id].last_message = messageData;
      
      // Increment unread count if this is not the active room
      if (activeRoomId.value !== messageData.room_id) {
        chatRooms[messageData.room_id].unread_count = 
          (chatRooms[messageData.room_id].unread_count || 0) + 1;
      }
    }
    
    // Play notification sound if not active room
    if (activeRoomId.value !== messageData.room_id) {
      playNotificationSound();
    }
  }
  
  /**
   * Handle 'message_sent' WebSocket message
   */
  function handleMessageSentMessage(response: WebSocketResponse) {
    const messageData = response.data as ChatMessage;
    
    // Ensure message list exists
    if (!messages[messageData.room_id]) {
      messages[messageData.room_id] = [];
    }
    
    // Check if this is a temporary message being confirmed
    const tempIndex = messages[messageData.room_id].findIndex(
      m => m.id.startsWith('temp-') && m.content === messageData.content
    );
    
    if (tempIndex !== -1) {
      // Replace temporary message with confirmed one
      messages[messageData.room_id][tempIndex] = messageData;
    } else {
      // Add as new message
      messages[messageData.room_id].push(messageData);
    }
    
    // Update room's last message
    if (chatRooms[messageData.room_id]) {
      chatRooms[messageData.room_id].last_message = messageData;
    }
  }
  
  /**
   * Handle 'message_history' WebSocket message
   */
  function handleMessageHistoryMessage(response: WebSocketResponse) {
    const { room_id, messages: messageHistory } = response.data;
    
    if (!messages[room_id]) {
      messages[room_id] = [];
    }
    
    // Prepend messages to the history (these are older messages)
    messages[room_id] = [...messageHistory, ...messages[room_id]];
  }
  
  /**
   * Handle 'user_typing' WebSocket message
   */
  function handleUserTypingMessage(response: WebSocketResponse) {
    const { room_id, user_id, user_name } = response.data;
    
    // Initialize typing record for room if needed
    if (!userTyping[room_id]) {
      userTyping[room_id] = {};
    }
    
    // Set typing timestamp for user
    userTyping[room_id][user_id] = Date.now();
    
    // Create typing timeout to auto-clear after 5 seconds of inactivity
    setTimeout(() => {
      if (userTyping[room_id] && userTyping[room_id][user_id]) {
        const elapsed = Date.now() - userTyping[room_id][user_id];
        if (elapsed > 5000) {
          delete userTyping[room_id][user_id];
        }
      }
    }, 5000);
  }
  
  /**
   * Handle 'user_typing_stopped' WebSocket message
   */
  function handleUserTypingStoppedMessage(response: WebSocketResponse) {
    const { room_id, user_id } = response.data;
    
    // Clear typing indicator for user
    if (userTyping[room_id] && userTyping[room_id][user_id]) {
      delete userTyping[room_id][user_id];
    }
  }
  
  /**
   * Handle 'reaction_added' WebSocket message
   */
  function handleReactionAddedMessage(response: WebSocketResponse) {
    const { room_id, message_id, reaction, user_id } = response.data;
    
    if (!messages[room_id]) return;
    
    // Find message
    const message = messages[room_id].find(m => m.id === message_id);
    if (!message) return;
    
    // Add reaction
    if (!message.reactions[reaction]) {
      message.reactions[reaction] = [];
    }
    
    if (!message.reactions[reaction].includes(user_id)) {
      message.reactions[reaction].push(user_id);
    }
  }
  
  /**
   * Handle 'reaction_removed' WebSocket message
   */
  function handleReactionRemovedMessage(response: WebSocketResponse) {
    const { room_id, message_id, reaction, user_id } = response.data;
    
    if (!messages[room_id]) return;
    
    // Find message
    const message = messages[room_id].find(m => m.id === message_id);
    if (!message || !message.reactions[reaction]) return;
    
    // Remove reaction
    const index = message.reactions[reaction].indexOf(user_id);
    if (index !== -1) {
      message.reactions[reaction].splice(index, 1);
      
      // Remove empty reaction arrays
      if (message.reactions[reaction].length === 0) {
        delete message.reactions[reaction];
      }
    }
  }
  
  /**
   * Handle 'message_edited' WebSocket message
   */
  function handleMessageEditedMessage(response: WebSocketResponse) {
    const { id, room_id, content, updated_at } = response.data;
    
    if (!messages[room_id]) return;
    
    // Find and update message
    const message = messages[room_id].find(m => m.id === id);
    if (message) {
      message.content = content;
      message.updated_at = updated_at;
      message.is_edited = true;
    }
  }
  
  /**
   * Handle 'message_deleted' WebSocket message
   */
  function handleMessageDeletedMessage(response: WebSocketResponse) {
    const { room_id, message_id } = response.data;
    
    if (!messages[room_id]) return;
    
    // Find and mark message as deleted
    const message = messages[room_id].find(m => m.id === message_id);
    if (message) {
      message.is_deleted = true;
      message.content = "This message was deleted";
    }
  }
  
  /**
   * Handle 'error' WebSocket message
   */
  function handleErrorMessage(response: WebSocketResponse) {
    console.error('WebSocket error:', response.error);
    notificationService.error(response.error || 'An error occurred');
  }
  
  /**
   * Send a WebSocket command
   */
  function sendCommand(command: WebSocketCommand) {
    if (connectionStatus.value !== 'connected' || !wsConnection.value) {
      console.error('Cannot send command: WebSocket not connected');
      return false;
    }
    
    try {
      wsConnection.value.send(JSON.stringify(command));
      return true;
    } catch (error) {
      console.error('Error sending WebSocket command:', error);
      return false;
    }
  }
  
  /**
   * Join a chat room
   */
  function joinRoom(roomId: string) {
    // Set as active room
    activeRoomId.value = roomId;
    
    // Send join command
    sendCommand({
      command: 'join_room',
      room_id: roomId,
      data: { room_id: roomId }
    });
    
    // Mark as read if we have unread messages
    if (chatRooms[roomId] && chatRooms[roomId].unread_count) {
      chatRooms[roomId].unread_count = 0;
    }
  }
  
  /**
   * Leave a chat room
   */
  function leaveRoom(roomId: string) {
    // Send leave command
    sendCommand({
      command: 'leave_room',
      room_id: roomId,
      data: { room_id: roomId }
    });
    
    // Clear active room if this is the active one
    if (activeRoomId.value === roomId) {
      activeRoomId.value = null;
    }
  }
  
  /**
   * Send a message to a room
   */
  function sendMessage(roomId: string, content: string, messageType = MessageType.TEXT) {
    if (!content.trim()) return false;
    
    // Create temporary message ID
    const tempId = `temp-${Date.now()}`;
    
    // Add temporary message to UI immediately
    if (!messages[roomId]) {
      messages[roomId] = [];
    }
    
    const tempMessage: ChatMessage = {
      id: tempId,
      room_id: roomId,
      sender_id: authStore.user?.id,
      sender_name: authStore.user?.full_name,
      message_type: messageType,
      content,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_edited: false,
      is_deleted: false,
      reactions: {},
      metadata: {}
    };
    
    messages[roomId].push(tempMessage);
    
    // Send the message
    return sendCommand({
      command: 'send_message',
      room_id: roomId,
      data: {
        room_id: roomId,
        content,
        message_type: messageType
      }
    });
  }
  
  /**
   * Edit a message
   */
  function editMessage(messageId: string, roomId: string, content: string) {
    if (!content.trim()) return false;
    
    return sendCommand({
      command: 'edit_message',
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        content
      }
    });
  }
  
  /**
   * Delete a message
   */
  function deleteMessage(messageId: string, roomId: string) {
    return sendCommand({
      command: 'delete_message',
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId
      }
    });
  }
  
  /**
   * Add a reaction to a message
   */
  function addReaction(messageId: string, roomId: string, reaction: string) {
    return sendCommand({
      command: 'add_reaction',
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }
  
  /**
   * Remove a reaction from a message
   */
  function removeReaction(messageId: string, roomId: string, reaction: string) {
    return sendCommand({
      command: 'remove_reaction',
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }
  
  /**
   * Send typing indicator
   */
  function sendTypingStart(roomId: string) {
    return sendCommand({
      command: 'typing_start',
      room_id: roomId,
      data: { room_id: roomId }
    });
  }
  
  /**
   * Send typing stopped indicator
   */
  function sendTypingStop(roomId: string) {
    return sendCommand({
      command: 'typing_stop',
      room_id: roomId,
      data: { room_id: roomId }
    });
  }
  
  /**
   * Fetch message history
   */
  function fetchMessageHistory(roomId: string, beforeId?: string) {
    return sendCommand({
      command: 'fetch_history',
      room_id: roomId,
      data: {
        room_id: roomId,
        before_id: beforeId,
        limit: 50
      }
    });
  }
  
  /**
   * Mark messages as read
   */
  function markAsRead(roomId: string, lastReadId: string) {
    return sendCommand({
      command: 'read_messages',
      room_id: roomId,
      data: {
        room_id: roomId,
        last_read_id: lastReadId
      }
    });
  }
  
  /**
   * Create a new room using REST API
   */
  async function createRoom(name: string, type: ChatRoomType, members?: any[]) {
    isLoading.value = true;
    
    try {
      const response = await api.post('/chat/rooms', {
        name,
        type,
        members
      });
      
      if (response.success && response.room) {
        // Add to room list
        chatRooms[response.room.id] = response.room;
        return response.room;
      }
      
      return null;
    } catch (error) {
      console.error('Error creating room:', error);
      notificationService.error('Failed to create room');
      return null;
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Create a direct chat with another user
   */
  async function createDirectChat(userId: string) {
    isLoading.value = true;
    
    try {
      const response = await api.post('/chat/direct-chats', {
        user_id: userId
      });
      
      if (response.success && response.room) {
        // Add to room list
        chatRooms[response.room.id] = response.room;
        return response.room;
      }
      
      return null;
    } catch (error) {
      console.error('Error creating direct chat:', error);
      notificationService.error('Failed to create direct chat');
      return null;
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Fetch rooms from the API
   */
  async function fetchRooms() {
    isLoading.value = true;
    
    try {
      const response = await api.get('/chat/rooms');
      
      if (response.success && response.rooms) {
        // Update room list
        response.rooms.forEach((room: ChatRoom) => {
          chatRooms[room.id] = room;
        });
      }
    } catch (error) {
      console.error('Error fetching rooms:', error);
      notificationService.error('Failed to fetch chat rooms');
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Add a member to a room
   */
  async function addMember(roomId: string, userId: string, role = ChatMemberRole.MEMBER) {
    isLoading.value = true;
    
    try {
      const response = await api.post(`/chat/rooms/${roomId}/members`, {
        user_id: userId,
        role
      });
      
      return response.success;
    } catch (error) {
      console.error('Error adding member:', error);
      notificationService.error('Failed to add member');
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Remove a member from a room
   */
  async function removeMember(roomId: string, userId: string) {
    isLoading.value = true;
    
    try {
      const response = await api.delete(`/chat/rooms/${roomId}/members/${userId}`);
      return response.success;
    } catch (error) {
      console.error('Error removing member:', error);
      notificationService.error('Failed to remove member');
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Update a member's role
   */
  async function updateMemberRole(roomId: string, userId: string, role: ChatMemberRole) {
    isLoading.value = true;
    
    try {
      const response = await api.put(`/chat/rooms/${roomId}/members/${userId}`, {
        role
      });
      
      return response.success;
    } catch (error) {
      console.error('Error updating member role:', error);
      notificationService.error('Failed to update member role');
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  
  /**
   * Get users who are currently typing in a room
   */
  function getTypingUsers(roomId: string): string[] {
    if (!userTyping[roomId]) return [];
    
    const now = Date.now();
    const typingUsers: string[] = [];
    
    // Gather user IDs who are typing
    Object.entries(userTyping[roomId]).forEach(([userId, timestamp]) => {
      // Consider typing active if within last 5 seconds
      if (now - timestamp < 5000) {
        // Find user name
        if (members[roomId]) {
          const member = members[roomId].find(m => m.user_id === userId);
          if (member) {
            typingUsers.push(member.user_name);
          }
        }
      } else {
        // Clean up expired typing indicators
        delete userTyping[roomId][userId];
      }
    });
    
    return typingUsers;
  }
  
  /**
   * Play notification sound
   */
  function playNotificationSound() {
    // Create and play a notification sound
    const audio = new Audio('/sounds/notification.mp3');
    audio.volume = 0.5;
    audio.play().catch(e => console.log('Failed to play notification sound:', e));
  }
  
  /**
   * Initialize chat service
   */
  function initialize() {
    // Connect WebSocket
    connectWebSocket();
    
    // Fetch initial room list
    fetchRooms();
    
    // Set up reconnection on visibility change
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible' && connectionStatus.value !== 'connected') {
        connectWebSocket();
      }
    });
    
    // Set up reconnection on network status change
    window.addEventListener('online', () => {
      if (connectionStatus.value !== 'connected') {
        connectWebSocket();
      }
    });
    
    // Set up automatic reconnection when user logs in
    watch(() => authStore.isLoggedIn, (isLoggedIn) => {
      if (isLoggedIn && connectionStatus.value !== 'connected') {
        connectWebSocket();
      } else if (!isLoggedIn) {
        disconnectWebSocket();
      }
    }, { immediate: true });
  }
  
  // Return public API
  return {
    // State
    chatRooms,
    messages,
    members,
    activeRoomId,
    activeRoom,
    activeRoomMessages,
    activeRoomMembers,
    isLoading,
    connectionStatus,
    totalUnreadCount,
    
    // Methods
    initialize,
    connectWebSocket,
    disconnectWebSocket,
    sendMessage,
    editMessage,
    deleteMessage,
    addReaction,
    removeReaction,
    joinRoom,
    leaveRoom,
    sendTypingStart,
    sendTypingStop,
    fetchMessageHistory,
    markAsRead,
    createRoom,
    createDirectChat,
    fetchRooms,
    addMember,
    removeMember,
    updateMemberRole,
    getTypingUsers
  };
}

// Create singleton instance
export const chatService = useChatService();
