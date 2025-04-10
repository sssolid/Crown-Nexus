// frontend/src/services/chat.ts
/**
 * Chat service module.
 *
 * This service provides functionality for real-time chat communication:
 * - WebSocket connection management
 * - Chat room operations (create, join, leave)
 * - Message handling (send, edit, delete)
 * - User presence and typing indicators
 * - Reaction management
 *
 * It builds on the base API service and adds chat-specific functionality.
 */

import { ref, reactive, computed, ComputedRef, watch } from 'vue';
import api, { ApiService } from '@/services/api';
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
import { notificationService } from '@/utils/notifications';

/**
 * Chat service for WebSocket and API interactions.
 */
export class ChatService extends ApiService {
  // State variables
  private chatRooms = reactive<Record<string, ChatRoom>>({});
  private activeRoomId = ref<string | null>(null);
  private messages = reactive<Record<string, ChatMessage[]>>({});
  private members = reactive<Record<string, ChatMember[]>>({});
  private isLoading = ref(false);
  private wsConnection = ref<WebSocket | null>(null);
  private connectionStatus = ref<'connected' | 'connecting' | 'disconnected'>('disconnected');
  private userPresence = reactive<Record<string, UserPresence>>({});
  private userTyping = reactive<Record<string, Record<string, number>>>({});

  // Connection retry variables
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000; // 2 seconds initial delay
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  // Computed properties
  public get rooms(): Record<string, ChatRoom> {
    return this.chatRooms;
  }

  public get currentRoomId(): string | null {
    return this.activeRoomId.value;
  }

  public get currentRoom(): ChatRoom | null {
    if (!this.activeRoomId.value) return null;
    return this.chatRooms[this.activeRoomId.value] || null;
  }

  public get currentRoomMessages(): ChatMessage[] {
    if (!this.activeRoomId.value) return [];
    return this.messages[this.activeRoomId.value] || [];
  }

  public get currentRoomMembers(): ChatMember[] {
    if (!this.activeRoomId.value) return [];
    return this.members[this.activeRoomId.value] || [];
  }

  public get loading(): boolean {
    return this.isLoading.value;
  }

  public get connectionState(): 'connected' | 'connecting' | 'disconnected' {
    return this.connectionStatus.value;
  }

  public get totalUnreadCount(): number {
    return Object.values(this.chatRooms).reduce((total, room) => {
      return total + (room.unread_count || 0);
    }, 0);
  }

  /**
   * Connect to the WebSocket server.
   *
   * Establishes a WebSocket connection to the chat server using the
   * current authentication token.
   *
   * @returns Success status of connection attempt
   */
  public connectWebSocket(): boolean {
    const authStore = useAuthStore();

    if (this.wsConnection.value && this.wsConnection.value.readyState < 2) {
      // Already connected or connecting
      return true;
    }

    if (!authStore.token) {
      console.error('Cannot connect WebSocket: No auth token');
      this.connectionStatus.value = 'disconnected';
      return false;
    }

    try {
      // Build WebSocket URL with authentication token
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      const wsUrl = `${protocol}//${host}/api/v1/ws/chat?token=${authStore.token}`;

      this.connectionStatus.value = 'connecting';
      this.wsConnection.value = new WebSocket(wsUrl);

      // Set up event handlers
      this.wsConnection.value.onopen = this.handleWebSocketOpen.bind(this);
      this.wsConnection.value.onmessage = this.handleWebSocketMessage.bind(this);
      this.wsConnection.value.onclose = this.handleWebSocketClose.bind(this);
      this.wsConnection.value.onerror = this.handleWebSocketError.bind(this);

      return true;
    } catch (error) {
      console.error('WebSocket connection error:', error);
      this.connectionStatus.value = 'disconnected';
      return false;
    }
  }

  /**
   * Disconnect from the WebSocket server.
   */
  public disconnectWebSocket(): void {
    if (this.wsConnection.value && this.wsConnection.value.readyState < 2) {
      this.wsConnection.value.close();
    }

    // Clear reconnect timer if active
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.wsConnection.value = null;
    this.connectionStatus.value = 'disconnected';
  }

  /**
   * Handle WebSocket connection open.
   */
  private handleWebSocketOpen(): void {
    console.log('WebSocket connected');
    this.connectionStatus.value = 'connected';
    this.reconnectAttempts = 0; // Reset reconnect counter on successful connection

    // Join active room if any
    if (this.activeRoomId.value) {
      this.joinRoom(this.activeRoomId.value);
    }
  }

  /**
   * Handle WebSocket connection close.
   *
   * @param event - Close event
   */
  private handleWebSocketClose(event: CloseEvent): void {
    console.log(`WebSocket closed: ${event.code} ${event.reason}`);
    this.connectionStatus.value = 'disconnected';
    this.wsConnection.value = null;

    // Attempt to reconnect if not closed intentionally
    if (event.code !== 1000) {
      this.attemptReconnect();
    }
  }

  /**
   * Handle WebSocket error.
   *
   * @param event - Error event
   */
  private handleWebSocketError(event: Event): void {
    console.error('WebSocket error:', event);
    // Error handling is done in onclose handler
  }

  /**
   * Attempt to reconnect to WebSocket server with exponential backoff.
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Maximum reconnect attempts reached');
      notificationService.error('Connection lost. Please refresh the page.');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);

    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
      this.connectWebSocket();
    }, delay);
  }

  /**
   * Handle incoming WebSocket messages.
   *
   * @param event - Message event
   */
  private handleWebSocketMessage(event: MessageEvent): void {
    try {
      const response: WebSocketResponse = JSON.parse(event.data);

      // Process message based on type
      switch (response.type) {
        case 'connected':
          this.handleConnectedMessage(response);
          break;

        case 'room_list':
          this.handleRoomListMessage(response);
          break;

        case 'room_joined':
          this.handleRoomJoinedMessage(response);
          break;

        case 'user_joined':
          this.handleUserJoinedMessage(response);
          break;

        case 'user_left':
          this.handleUserLeftMessage(response);
          break;

        case 'new_message':
          this.handleNewMessageMessage(response);
          break;

        case 'message_sent':
          this.handleMessageSentMessage(response);
          break;

        case 'message_history':
          this.handleMessageHistoryMessage(response);
          break;

        case 'user_typing':
          this.handleUserTypingMessage(response);
          break;

        case 'user_typing_stopped':
          this.handleUserTypingStoppedMessage(response);
          break;

        case 'reaction_added':
          this.handleReactionAddedMessage(response);
          break;

        case 'reaction_removed':
          this.handleReactionRemovedMessage(response);
          break;

        case 'message_edited':
          this.handleMessageEditedMessage(response);
          break;

        case 'message_deleted':
          this.handleMessageDeletedMessage(response);
          break;

        case 'error':
          this.handleErrorMessage(response);
          break;

        default:
          console.warn(`Unknown message type: ${response.type}`, response);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error, event.data);
    }
  }

  /**
   * Handle 'connected' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleConnectedMessage(response: WebSocketResponse): void {
    console.log('Connected to chat server', response.data);
  }

  /**
   * Handle 'room_list' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleRoomListMessage(response: WebSocketResponse): void {
    const rooms = response.data.rooms as ChatRoom[];

    // Update room list
    rooms.forEach(room => {
      this.chatRooms[room.id] = room;
    });
  }

  /**
   * Handle 'room_joined' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleRoomJoinedMessage(response: WebSocketResponse): void {
    const roomInfo = response.data as ChatRoom;

    // Update room data
    this.chatRooms[roomInfo.id] = roomInfo;

    // Update members
    if (roomInfo.members) {
      this.members[roomInfo.id] = roomInfo.members;
    }

    // Fetch message history if this is the active room
    if (this.activeRoomId.value === roomInfo.id) {
      this.fetchMessageHistory(roomInfo.id);
    }
  }

  /**
   * Handle 'user_joined' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleUserJoinedMessage(response: WebSocketResponse): void {
    const { room_id, user } = response.data;

    // Update room member count
    if (this.chatRooms[room_id]) {
      this.chatRooms[room_id].member_count = (this.chatRooms[room_id].member_count || 0) + 1;
    }

    // Add to room members if we have the member list
    if (this.members[room_id]) {
      const existingMember = this.members[room_id].find(m => m.user_id === user.id);

      if (!existingMember) {
        this.members[room_id].push({
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
    if (this.messages[room_id]) {
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

      this.messages[room_id].push(systemMessage);
    }
  }

  /**
   * Handle 'user_left' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleUserLeftMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    // Update room member count
    if (this.chatRooms[room_id]) {
      this.chatRooms[room_id].member_count = Math.max(0, (this.chatRooms[room_id].member_count || 1) - 1);
    }

    // Update member list if we have it
    if (this.members[room_id]) {
      const memberIndex = this.members[room_id].findIndex(m => m.user_id === user_id);

      if (memberIndex !== -1) {
        const userName = this.members[room_id][memberIndex].user_name;
        this.members[room_id].splice(memberIndex, 1);

        // Add system message
        if (this.messages[room_id]) {
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

          this.messages[room_id].push(systemMessage);
        }
      }
    }
  }

  /**
   * Handle 'new_message' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleNewMessageMessage(response: WebSocketResponse): void {
    const messageData = response.data as ChatMessage;

    // Add message to room
    if (!this.messages[messageData.room_id]) {
      this.messages[messageData.room_id] = [];
    }

    this.messages[messageData.room_id].push(messageData);

    // Update room's last message
    if (this.chatRooms[messageData.room_id]) {
      this.chatRooms[messageData.room_id].last_message = messageData;

      // Increment unread count if this is not the active room
      if (this.activeRoomId.value !== messageData.room_id) {
        this.chatRooms[messageData.room_id].unread_count =
          (this.chatRooms[messageData.room_id].unread_count || 0) + 1;
      }
    }

    // Play notification sound if not active room
    if (this.activeRoomId.value !== messageData.room_id) {
      this.playNotificationSound();
    }
  }

  /**
   * Handle 'message_sent' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleMessageSentMessage(response: WebSocketResponse): void {
    const messageData = response.data as ChatMessage;

    // Ensure message list exists
    if (!this.messages[messageData.room_id]) {
      this.messages[messageData.room_id] = [];
    }

    // Check if this is a temporary message being confirmed
    const tempIndex = this.messages[messageData.room_id].findIndex(
      m => m.id.startsWith('temp-') && m.content === messageData.content
    );

    if (tempIndex !== -1) {
      // Replace temporary message with confirmed one
      this.messages[messageData.room_id][tempIndex] = messageData;
    } else {
      // Add as new message
      this.messages[messageData.room_id].push(messageData);
    }

    // Update room's last message
    if (this.chatRooms[messageData.room_id]) {
      this.chatRooms[messageData.room_id].last_message = messageData;
    }
  }

  /**
   * Handle 'message_history' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleMessageHistoryMessage(response: WebSocketResponse): void {
    const { room_id, messages: messageHistory } = response.data;

    if (!this.messages[room_id]) {
      this.messages[room_id] = [];
    }

    // Prepend messages to the history (these are older messages)
    this.messages[room_id] = [...messageHistory, ...this.messages[room_id]];
  }

  /**
   * Handle 'user_typing' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleUserTypingMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    // Initialize typing record for room if needed
    if (!this.userTyping[room_id]) {
      this.userTyping[room_id] = {};
    }

    // Set typing timestamp for user
    this.userTyping[room_id][user_id] = Date.now();

    // Create typing timeout to auto-clear after 5 seconds of inactivity
    setTimeout(() => {
      if (this.userTyping[room_id] && this.userTyping[room_id][user_id]) {
        const elapsed = Date.now() - this.userTyping[room_id][user_id];
        if (elapsed > 5000) {
          delete this.userTyping[room_id][user_id];
        }
      }
    }, 5000);
  }

  /**
   * Handle 'user_typing_stopped' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleUserTypingStoppedMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    // Clear typing indicator for user
    if (this.userTyping[room_id] && this.userTyping[room_id][user_id]) {
      delete this.userTyping[room_id][user_id];
    }
  }

  /**
   * Handle 'reaction_added' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleReactionAddedMessage(response: WebSocketResponse): void {
    const { room_id, message_id, reaction, user_id } = response.data;

    if (!this.messages[room_id]) return;

    // Find message
    const message = this.messages[room_id].find(m => m.id === message_id);
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
   * Handle 'reaction_removed' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleReactionRemovedMessage(response: WebSocketResponse): void {
    const { room_id, message_id, reaction, user_id } = response.data;

    if (!this.messages[room_id]) return;

    // Find message
    const message = this.messages[room_id].find(m => m.id === message_id);
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
   * Handle 'message_edited' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleMessageEditedMessage(response: WebSocketResponse): void {
    const { id, room_id, content, updated_at } = response.data;

    if (!this.messages[room_id]) return;

    // Find and update message
    const message = this.messages[room_id].find(m => m.id === id);
    if (message) {
      message.content = content;
      message.updated_at = updated_at;
      message.is_edited = true;
    }
  }

  /**
   * Handle 'message_deleted' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleMessageDeletedMessage(response: WebSocketResponse): void {
    const { room_id, message_id } = response.data;

    if (!this.messages[room_id]) return;

    // Find and mark message as deleted
    const message = this.messages[room_id].find(m => m.id === message_id);
    if (message) {
      message.is_deleted = true;
      message.content = "This message was deleted";
    }
  }

  /**
   * Handle 'error' WebSocket message.
   *
   * @param response - WebSocket response
   */
  private handleErrorMessage(response: WebSocketResponse): void {
    console.error('WebSocket error:', response.error);
    notificationService.error(response.error || 'An error occurred');
  }

  /**
   * Send a WebSocket command.
   *
   * @param command - Command to send
   * @returns Success status
   */
  private sendCommand(command: WebSocketCommand): boolean {
    if (this.connectionStatus.value !== 'connected' || !this.wsConnection.value) {
      console.error('Cannot send command: WebSocket not connected');
      return false;
    }

    try {
      this.wsConnection.value.send(JSON.stringify(command));
      return true;
    } catch (error) {
      console.error('Error sending WebSocket command:', error);
      return false;
    }
  }

  /**
   * Join a chat room.
   *
   * @param roomId - Room ID to join
   * @returns Success status
   */
  public joinRoom(roomId: string): boolean {
    // Set as active room
    this.activeRoomId.value = roomId;

    // Send join command
    const success = this.sendCommand({
      command: 'join_room',
      room_id: roomId,
      data: { room_id: roomId }
    });

    // Mark as read if we have unread messages
    if (this.chatRooms[roomId] && this.chatRooms[roomId].unread_count) {
      this.chatRooms[roomId].unread_count = 0;
    }

    return success;
  }

  /**
   * Leave a chat room.
   *
   * @param roomId - Room ID to leave
   * @returns Success status
   */
  public leaveRoom(roomId: string): boolean {
    // Send leave command
    const success = this.sendCommand({
      command: 'leave_room',
      room_id: roomId,
      data: { room_id: roomId }
    });

    // Clear active room if this is the active one
    if (this.activeRoomId.value === roomId) {
      this.activeRoomId.value = null;
    }

    return success;
  }

  /**
   * Send a message to a room.
   *
   * @param roomId - Room ID
   * @param content - Message content
   * @param messageType - Message type
   * @returns Success status
   */
  public sendMessage(roomId: string, content: string, messageType = MessageType.TEXT): boolean {
    if (!content.trim()) return false;

    const authStore = useAuthStore();

    // Create temporary message ID
    const tempId = `temp-${Date.now()}`;

    // Add temporary message to UI immediately
    if (!this.messages[roomId]) {
      this.messages[roomId] = [];
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

    this.messages[roomId].push(tempMessage);

    // Send the message
    return this.sendCommand({
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
   * Edit a message.
   *
   * @param messageId - Message ID
   * @param roomId - Room ID
   * @param content - New message content
   * @returns Success status
   */
  public editMessage(messageId: string, roomId: string, content: string): boolean {
    if (!content.trim()) return false;

    return this.sendCommand({
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
   * Delete a message.
   *
   * @param messageId - Message ID
   * @param roomId - Room ID
   * @returns Success status
   */
  public deleteMessage(messageId: string, roomId: string): boolean {
    return this.sendCommand({
      command: 'delete_message',
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId
      }
    });
  }

  /**
   * Add a reaction to a message.
   *
   * @param messageId - Message ID
   * @param roomId - Room ID
   * @param reaction - Reaction emoji
   * @returns Success status
   */
  public addReaction(messageId: string, roomId: string, reaction: string): boolean {
    return this.sendCommand({
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
   * Remove a reaction from a message.
   *
   * @param messageId - Message ID
   * @param roomId - Room ID
   * @param reaction - Reaction emoji
   * @returns Success status
   */
  public removeReaction(messageId: string, roomId: string, reaction: string): boolean {
    return this.sendCommand({
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
   * Send typing indicator.
   *
   * @param roomId - Room ID
   * @returns Success status
   */
  public sendTypingStart(roomId: string): boolean {
    return this.sendCommand({
      command: 'typing_start',
      room_id: roomId,
      data: { room_id: roomId }
    });
  }

  /**
   * Send typing stopped indicator.
   *
   * @param roomId - Room ID
   * @returns Success status
   */
  public sendTypingStop(roomId: string): boolean {
    return this.sendCommand({
      command: 'typing_stop',
      room_id: roomId,
      data: { room_id: roomId }
    });
  }

  /**
   * Fetch message history.
   *
   * @param roomId - Room ID
   * @param beforeId - Get messages before this ID
   * @returns Success status
   */
  public fetchMessageHistory(roomId: string, beforeId?: string): boolean {
    return this.sendCommand({
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
   * Mark messages as read.
   *
   * @param roomId - Room ID
   * @param lastReadId - Last read message ID
   * @returns Success status
   */
  public markAsRead(roomId: string, lastReadId: string): boolean {
    return this.sendCommand({
      command: 'read_messages',
      room_id: roomId,
      data: {
        room_id: roomId,
        last_read_id: lastReadId
      }
    });
  }

  /**
   * Create a new room using REST API.
   *
   * @param name - Room name
   * @param type - Room type
   * @param members - Initial members
   * @returns Created room or null
   */
  public async createRoom(name: string, type: ChatRoomType, members?: any[]): Promise<ChatRoom | null> {
    this.isLoading.value = true;

    try {
      const response = await this.post('/chat/rooms', {
        name,
        type,
        members
      });

      if (response.success && response.room) {
        // Add to room list
        this.chatRooms[response.room.id] = response.room;
        return response.room;
      }

      return null;
    } catch (error) {
      console.error('Error creating room:', error);
      notificationService.error('Failed to create room');
      return null;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Create a direct chat with another user.
   *
   * @param userId - User ID
   * @returns Created room or null
   */
  public async createDirectChat(userId: string): Promise<ChatRoom | null> {
    this.isLoading.value = true;

    try {
      const response = await this.post('/chat/direct-chats', {
        user_id: userId
      });

      if (response.success && response.room) {
        // Add to room list
        this.chatRooms[response.room.id] = response.room;
        return response.room;
      }

      return null;
    } catch (error) {
      console.error('Error creating direct chat:', error);
      notificationService.error('Failed to create direct chat');
      return null;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Fetch rooms from the API.
   *
   * @returns Success status
   */
  public async fetchRooms(): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.get('/chat/rooms');

      if (response.success && response.rooms) {
        // Update room list
        response.rooms.forEach((room: ChatRoom) => {
          this.chatRooms[room.id] = room;
        });
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error fetching rooms:', error);
      notificationService.error('Failed to fetch chat rooms');
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Add a member to a room.
   *
   * @param roomId - Room ID
   * @param userId - User ID
   * @param role - Member role
   * @returns Success status
   */
  public async addMember(roomId: string, userId: string, role = ChatMemberRole.MEMBER): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.post(`/chat/rooms/${roomId}/members`, {
        user_id: userId,
        role
      });

      return response.success;
    } catch (error) {
      console.error('Error adding member:', error);
      notificationService.error('Failed to add member');
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Remove a member from a room.
   *
   * @param roomId - Room ID
   * @param userId - User ID
   * @returns Success status
   */
  public async removeMember(roomId: string, userId: string): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.delete(`/chat/rooms/${roomId}/members/${userId}`);
      return response.success;
    } catch (error) {
      console.error('Error removing member:', error);
      notificationService.error('Failed to remove member');
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Update a member's role.
   *
   * @param roomId - Room ID
   * @param userId - User ID
   * @param role - New role
   * @returns Success status
   */
  public async updateMemberRole(roomId: string, userId: string, role: ChatMemberRole): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.put(`/chat/rooms/${roomId}/members/${userId}`, {
        role
      });

      return response.success;
    } catch (error) {
      console.error('Error updating member role:', error);
      notificationService.error('Failed to update member role');
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  /**
   * Get users who are currently typing in a room.
   *
   * @param roomId - Room ID
   * @returns List of typing user names
   */
  public getTypingUsers(roomId: string): string[] {
    if (!this.userTyping[roomId]) return [];

    const now = Date.now();
    const typingUsers: string[] = [];

    // Gather user IDs who are typing
    Object.entries(this.userTyping[roomId]).forEach(([userId, timestamp]) => {
      // Consider typing active if within last 5 seconds
      if (now - timestamp < 5000) {
        // Find user name
        if (this.members[roomId]) {
          const member = this.members[roomId].find(m => m.user_id === userId);
          if (member) {
            typingUsers.push(member.user_name);
          }
        }
      } else {
        // Clean up expired typing indicators
        delete this.userTyping[roomId][userId];
      }
    });

    return typingUsers;
  }

  /**
   * Play notification sound.
   */
  private playNotificationSound(): void {
    // Create and play a notification sound
    const audio = new Audio('/sounds/notification.mp3');
    audio.volume = 0.5;
    audio.play().catch(e => console.log('Failed to play notification sound:', e));
  }

  /**
   * Initialize chat service.
   */
  public initialize(): void {
    const authStore = useAuthStore();

    // Connect WebSocket
    this.connectWebSocket();

    // Fetch initial room list
    this.fetchRooms();

    // Set up reconnection on visibility change
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible' && this.connectionStatus.value !== 'connected') {
        this.connectWebSocket();
      }
    });

    // Set up reconnection on network status change
    window.addEventListener('online', () => {
      if (this.connectionStatus.value !== 'connected') {
        this.connectWebSocket();
      }
    });

    // Set up automatic reconnection when user logs in
    watch(() => authStore.isLoggedIn, (isLoggedIn) => {
      if (isLoggedIn && this.connectionStatus.value !== 'connected') {
        this.connectWebSocket();
      } else if (!isLoggedIn) {
        this.disconnectWebSocket();
      }
    }, { immediate: true });
  }
}

// Create and export a singleton instance
export const chatService = new ChatService();
export default chatService;
