import{ref,reactive,computed,ComputedRef,watch}from 'vue';import api,{ApiService}from '@/services/api';import{ChatRoom,ChatMessage,ChatMember,ChatRoomType,ChatMemberRole,MessageType,WebSocketCommand,WebSocketResponse,UserPresence}from '@/types/chat';import{useAuthStore}from '@/stores/auth';import{notificationService}from '@/utils/notifications';export class ChatService extends ApiService{private chatRooms=reactive<Record<string,ChatRoom>>({});private activeRoomId=ref<string|null>(null);private messages=reactive<Record<string,ChatMessage[]>>({});private members=reactive<Record<string,ChatMember[]>>({});private isLoading=ref(false);private wsConnection=ref<WebSocket|null>(null);private connectionStatus=ref<'connected'|'connecting'|'disconnected'>('disconnected');private userPresence=reactive<Record<string,UserPresence>>({});private userTyping=reactive<Record<string,Record<string,number>>>({});private reconnectAttempts=0;private maxReconnectAttempts=5;private reconnectDelay=2000;private reconnectTimer:ReturnType<typeof setTimeout>|null=null;public get rooms():Record<string,ChatRoom>{return this.chatRooms;}public get currentRoomId():string|null{return this.activeRoomId.value;}public get currentRoom():ChatRoom|null{if(!this.activeRoomId.value)return null;return this.chatRooms[this.activeRoomId.value]||null;}public get currentRoomMessages():ChatMessage[]{if(!this.activeRoomId.value)return[];return this.messages[this.activeRoomId.value]||[];}public get currentRoomMembers():ChatMember[]{if(!this.activeRoomId.value)return[];return this.members[this.activeRoomId.value]||[];}public get loading():boolean{return this.isLoading.value;}public get connectionState():'connected'|'connecting'|'disconnected'{return this.connectionStatus.value;}public get totalUnreadCount():number{return Object.values(this.chatRooms).reduce((total,room)=>{return total+(room.unread_count||0);},0);}public connectWebSocket():boolean{const authStore=useAuthStore();if(this.wsConnection.value&&this.wsConnection.value.readyState<2){return true;}if(!authStore.token){console.error('Cannot connect WebSocket: No auth token');this.connectionStatus.value='disconnected';return false;}try{const protocol=window.location.protocol==='https:'?'wss:':'ws:';const host=window.location.host;const wsUrl=`${protocol}

      this.connectionStatus.value = __STRING_18__;
      this.wsConnection.value = new WebSocket(wsUrl);

      
      this.wsConnection.value.onopen = this.handleWebSocketOpen.bind(this);
      this.wsConnection.value.onmessage = this.handleWebSocketMessage.bind(this);
      this.wsConnection.value.onclose = this.handleWebSocketClose.bind(this);
      this.wsConnection.value.onerror = this.handleWebSocketError.bind(this);

      return true;
    } catch (error) {
      console.error(__STRING_19__, error);
      this.connectionStatus.value = __STRING_20__;
      return false;
    }
  }

  
  public disconnectWebSocket(): void {
    if (this.wsConnection.value && this.wsConnection.value.readyState < 2) {
      this.wsConnection.value.close();
    }

    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.wsConnection.value = null;
    this.connectionStatus.value = __STRING_21__;
  }

  
  private handleWebSocketOpen(): void {
    console.log(__STRING_22__);
    this.connectionStatus.value = __STRING_23__;
    this.reconnectAttempts = 0; 

    
    if (this.activeRoomId.value) {
      this.joinRoom(this.activeRoomId.value);
    }
  }

  
  private handleWebSocketClose(event: CloseEvent): void {
    console.log(`WebSocket closed:${event.code}${event.reason}`);
    this.connectionStatus.value = __STRING_24__;
    this.wsConnection.value = null;

    
    if (event.code !== 1000) {
      this.attemptReconnect();
    }
  }

  
  private handleWebSocketError(event: Event): void {
    console.error(__STRING_25__, event);
    
  }

  
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error(__STRING_26__);
      notificationService.error(__STRING_27__);
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);

    console.log(`Attempting to reconnect in ${delay}ms(attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      console.log(`Reconnecting...(attempt ${this.reconnectAttempts})`);
      this.connectWebSocket();
    }, delay);
  }

  
  private handleWebSocketMessage(event: MessageEvent): void {
    try {
      const response: WebSocketResponse = JSON.parse(event.data);

      
      switch (response.type) {
        case __STRING_28__:
          this.handleConnectedMessage(response);
          break;

        case __STRING_29__:
          this.handleRoomListMessage(response);
          break;

        case __STRING_30__:
          this.handleRoomJoinedMessage(response);
          break;

        case __STRING_31__:
          this.handleUserJoinedMessage(response);
          break;

        case __STRING_32__:
          this.handleUserLeftMessage(response);
          break;

        case __STRING_33__:
          this.handleNewMessageMessage(response);
          break;

        case __STRING_34__:
          this.handleMessageSentMessage(response);
          break;

        case __STRING_35__:
          this.handleMessageHistoryMessage(response);
          break;

        case __STRING_36__:
          this.handleUserTypingMessage(response);
          break;

        case __STRING_37__:
          this.handleUserTypingStoppedMessage(response);
          break;

        case __STRING_38__:
          this.handleReactionAddedMessage(response);
          break;

        case __STRING_39__:
          this.handleReactionRemovedMessage(response);
          break;

        case __STRING_40__:
          this.handleMessageEditedMessage(response);
          break;

        case __STRING_41__:
          this.handleMessageDeletedMessage(response);
          break;

        case __STRING_42__:
          this.handleErrorMessage(response);
          break;

        default:
          console.warn(`Unknown message type:${response.type}`, response);
      }
    } catch (error) {
      console.error(__STRING_43__, error, event.data);
    }
  }

  
  private handleConnectedMessage(response: WebSocketResponse): void {
    console.log(__STRING_44__, response.data);
  }

  
  private handleRoomListMessage(response: WebSocketResponse): void {
    const rooms = response.data.rooms as ChatRoom[];

    
    rooms.forEach(room => {
      this.chatRooms[room.id] = room;
    });
  }

  
  private handleRoomJoinedMessage(response: WebSocketResponse): void {
    const roomInfo = response.data as ChatRoom;

    
    this.chatRooms[roomInfo.id] = roomInfo;

    
    if (roomInfo.members) {
      this.members[roomInfo.id] = roomInfo.members;
    }

    
    if (this.activeRoomId.value === roomInfo.id) {
      this.fetchMessageHistory(roomInfo.id);
    }
  }

  
  private handleUserJoinedMessage(response: WebSocketResponse): void {
    const { room_id, user } = response.data;

    
    if (this.chatRooms[room_id]) {
      this.chatRooms[room_id].member_count = (this.chatRooms[room_id].member_count || 0) + 1;
    }

    
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
        
        existingMember.is_online = true;
      }
    }

    
    if (this.messages[room_id]) {
      const systemMessage: ChatMessage = {
        id: `system-${Date.now()}`,
        room_id,
        sender_id: null,
        sender_name: null,
        message_type: MessageType.SYSTEM,
        content: `${user.name}joined the room`,
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

  
  private handleUserLeftMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    
    if (this.chatRooms[room_id]) {
      this.chatRooms[room_id].member_count = Math.max(0, (this.chatRooms[room_id].member_count || 1) - 1);
    }

    
    if (this.members[room_id]) {
      const memberIndex = this.members[room_id].findIndex(m => m.user_id === user_id);

      if (memberIndex !== -1) {
        const userName = this.members[room_id][memberIndex].user_name;
        this.members[room_id].splice(memberIndex, 1);

        
        if (this.messages[room_id]) {
          const systemMessage: ChatMessage = {
            id: `system-${Date.now()}`,
            room_id,
            sender_id: null,
            sender_name: null,
            message_type: MessageType.SYSTEM,
            content: `${userName}left the room`,
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

  
  private handleNewMessageMessage(response: WebSocketResponse): void {
    const messageData = response.data as ChatMessage;

    
    if (!this.messages[messageData.room_id]) {
      this.messages[messageData.room_id] = [];
    }

    this.messages[messageData.room_id].push(messageData);

    
    if (this.chatRooms[messageData.room_id]) {
      this.chatRooms[messageData.room_id].last_message = messageData;

      
      if (this.activeRoomId.value !== messageData.room_id) {
        this.chatRooms[messageData.room_id].unread_count =
          (this.chatRooms[messageData.room_id].unread_count || 0) + 1;
      }
    }

    
    if (this.activeRoomId.value !== messageData.room_id) {
      this.playNotificationSound();
    }
  }

  
  private handleMessageSentMessage(response: WebSocketResponse): void {
    const messageData = response.data as ChatMessage;

    
    if (!this.messages[messageData.room_id]) {
      this.messages[messageData.room_id] = [];
    }

    
    const tempIndex = this.messages[messageData.room_id].findIndex(
      m => m.id.startsWith(__STRING_45__) && m.content === messageData.content
    );

    if (tempIndex !== -1) {
      
      this.messages[messageData.room_id][tempIndex] = messageData;
    } else {
      
      this.messages[messageData.room_id].push(messageData);
    }

    
    if (this.chatRooms[messageData.room_id]) {
      this.chatRooms[messageData.room_id].last_message = messageData;
    }
  }

  
  private handleMessageHistoryMessage(response: WebSocketResponse): void {
    const { room_id, messages: messageHistory } = response.data;

    if (!this.messages[room_id]) {
      this.messages[room_id] = [];
    }

    
    this.messages[room_id] = [...messageHistory, ...this.messages[room_id]];
  }

  
  private handleUserTypingMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    
    if (!this.userTyping[room_id]) {
      this.userTyping[room_id] = {};
    }

    
    this.userTyping[room_id][user_id] = Date.now();

    
    setTimeout(() => {
      if (this.userTyping[room_id] && this.userTyping[room_id][user_id]) {
        const elapsed = Date.now() - this.userTyping[room_id][user_id];
        if (elapsed > 5000) {
          delete this.userTyping[room_id][user_id];
        }
      }
    }, 5000);
  }

  
  private handleUserTypingStoppedMessage(response: WebSocketResponse): void {
    const { room_id, user_id } = response.data;

    
    if (this.userTyping[room_id] && this.userTyping[room_id][user_id]) {
      delete this.userTyping[room_id][user_id];
    }
  }

  
  private handleReactionAddedMessage(response: WebSocketResponse): void {
    const { room_id, message_id, reaction, user_id } = response.data;

    if (!this.messages[room_id]) return;

    
    const message = this.messages[room_id].find(m => m.id === message_id);
    if (!message) return;

    
    if (!message.reactions[reaction]) {
      message.reactions[reaction] = [];
    }

    if (!message.reactions[reaction].includes(user_id)) {
      message.reactions[reaction].push(user_id);
    }
  }

  
  private handleReactionRemovedMessage(response: WebSocketResponse): void {
    const { room_id, message_id, reaction, user_id } = response.data;

    if (!this.messages[room_id]) return;

    
    const message = this.messages[room_id].find(m => m.id === message_id);
    if (!message || !message.reactions[reaction]) return;

    
    const index = message.reactions[reaction].indexOf(user_id);
    if (index !== -1) {
      message.reactions[reaction].splice(index, 1);

      
      if (message.reactions[reaction].length === 0) {
        delete message.reactions[reaction];
      }
    }
  }

  
  private handleMessageEditedMessage(response: WebSocketResponse): void {
    const { id, room_id, content, updated_at } = response.data;

    if (!this.messages[room_id]) return;

    
    const message = this.messages[room_id].find(m => m.id === id);
    if (message) {
      message.content = content;
      message.updated_at = updated_at;
      message.is_edited = true;
    }
  }

  
  private handleMessageDeletedMessage(response: WebSocketResponse): void {
    const { room_id, message_id } = response.data;

    if (!this.messages[room_id]) return;

    
    const message = this.messages[room_id].find(m => m.id === message_id);
    if (message) {
      message.is_deleted = true;
      message.content = __STRING_0__;
    }
  }

  
  private handleErrorMessage(response: WebSocketResponse): void {
    console.error(__STRING_46__, response.error);
    notificationService.error(response.error || __STRING_47__);
  }

  
  private sendCommand(command: WebSocketCommand): boolean {
    if (this.connectionStatus.value !== __STRING_48__ || !this.wsConnection.value) {
      console.error(__STRING_49__);
      return false;
    }

    try {
      this.wsConnection.value.send(JSON.stringify(command));
      return true;
    } catch (error) {
      console.error(__STRING_50__, error);
      return false;
    }
  }

  
  public joinRoom(roomId: string): boolean {
    
    this.activeRoomId.value = roomId;

    
    const success = this.sendCommand({
      command: __STRING_51__,
      room_id: roomId,
      data: { room_id: roomId }
    });

    
    if (this.chatRooms[roomId] && this.chatRooms[roomId].unread_count) {
      this.chatRooms[roomId].unread_count = 0;
    }

    return success;
  }

  
  public leaveRoom(roomId: string): boolean {
    
    const success = this.sendCommand({
      command: __STRING_52__,
      room_id: roomId,
      data: { room_id: roomId }
    });

    
    if (this.activeRoomId.value === roomId) {
      this.activeRoomId.value = null;
    }

    return success;
  }

  
  public sendMessage(roomId: string, content: string, messageType = MessageType.TEXT): boolean {
    if (!content.trim()) return false;

    const authStore = useAuthStore();

    
    const tempId = `temp-${Date.now()}`;

    
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

    
    return this.sendCommand({
      command: __STRING_53__,
      room_id: roomId,
      data: {
        room_id: roomId,
        content,
        message_type: messageType
      }
    });
  }

  
  public editMessage(messageId: string, roomId: string, content: string): boolean {
    if (!content.trim()) return false;

    return this.sendCommand({
      command: __STRING_54__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        content
      }
    });
  }

  
  public deleteMessage(messageId: string, roomId: string): boolean {
    return this.sendCommand({
      command: __STRING_55__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId
      }
    });
  }

  
  public addReaction(messageId: string, roomId: string, reaction: string): boolean {
    return this.sendCommand({
      command: __STRING_56__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }

  
  public removeReaction(messageId: string, roomId: string, reaction: string): boolean {
    return this.sendCommand({
      command: __STRING_57__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }

  
  public sendTypingStart(roomId: string): boolean {
    return this.sendCommand({
      command: __STRING_58__,
      room_id: roomId,
      data: { room_id: roomId }
    });
  }

  
  public sendTypingStop(roomId: string): boolean {
    return this.sendCommand({
      command: __STRING_59__,
      room_id: roomId,
      data: { room_id: roomId }
    });
  }

  
  public fetchMessageHistory(roomId: string, beforeId?: string): boolean {
    return this.sendCommand({
      command: __STRING_60__,
      room_id: roomId,
      data: {
        room_id: roomId,
        before_id: beforeId,
        limit: 50
      }
    });
  }

  
  public markAsRead(roomId: string, lastReadId: string): boolean {
    return this.sendCommand({
      command: __STRING_61__,
      room_id: roomId,
      data: {
        room_id: roomId,
        last_read_id: lastReadId
      }
    });
  }

  
  public async createRoom(name: string, type: ChatRoomType, members?: any[]): Promise<ChatRoom | null> {
    this.isLoading.value = true;

    try {
      const response = await this.post(__STRING_62__, {
        name,
        type,
        members
      });

      if (response.success && response.room) {
        
        this.chatRooms[response.room.id] = response.room;
        return response.room;
      }

      return null;
    } catch (error) {
      console.error(__STRING_63__, error);
      notificationService.error(__STRING_64__);
      return null;
    } finally {
      this.isLoading.value = false;
    }
  }

  
  public async createDirectChat(userId: string): Promise<ChatRoom | null> {
    this.isLoading.value = true;

    try {
      const response = await this.post(__STRING_65__, {
        user_id: userId
      });

      if (response.success && response.room) {
        
        this.chatRooms[response.room.id] = response.room;
        return response.room;
      }

      return null;
    } catch (error) {
      console.error(__STRING_66__, error);
      notificationService.error(__STRING_67__);
      return null;
    } finally {
      this.isLoading.value = false;
    }
  }

  
  public async fetchRooms(): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.get(__STRING_68__);

      if (response.success && response.rooms) {
        
        response.rooms.forEach((room: ChatRoom) => {
          this.chatRooms[room.id] = room;
        });
        return true;
      }
      return false;
    } catch (error) {
      console.error(__STRING_69__, error);
      notificationService.error(__STRING_70__);
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  
  public async addMember(roomId: string, userId: string, role = ChatMemberRole.MEMBER): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.post(`/chat/rooms/${roomId}/members`, {
        user_id: userId,
        role
      });

      return response.success;
    } catch (error) {
      console.error(__STRING_71__, error);
      notificationService.error(__STRING_72__);
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  
  public async removeMember(roomId: string, userId: string): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.delete(`/chat/rooms/${roomId}/members/${userId}`);
      return response.success;
    } catch (error) {
      console.error(__STRING_73__, error);
      notificationService.error(__STRING_74__);
      return false;
    } finally {
      this.isLoading.value = false;
    }
  }

  
  public async updateMemberRole(roomId: string, userId: string, role: ChatMemberRole): Promise<boolean> {
    this.isLoading.value = true;

    try {
      const response = await this.put(`/chat/rooms/${roomId}/members/${userId}`,{role});return response.success;}catch(error){console.error('Error updating member role:',error);notificationService.error('Failed to update member role');return false;}finally{this.isLoading.value=false;}}public getTypingUsers(roomId:string):string[]{if(!this.userTyping[roomId])return[];const now=Date.now();const typingUsers:string[]=[];Object.entries(this.userTyping[roomId]).forEach(([userId,timestamp])=>{if(now-timestamp<5000){if(this.members[roomId]){const member=this.members[roomId].find(m=>m.user_id===userId);if(member){typingUsers.push(member.user_name);}}}else{delete this.userTyping[roomId][userId];}});return typingUsers;}private playNotificationSound():void{const audio=new Audio('/sounds/notification.mp3');audio.volume=0.5;audio.play().catch(e=>console.log('Failed to play notification sound:',e));}public initialize():void{const authStore=useAuthStore();this.connectWebSocket();this.fetchRooms();document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&this.connectionStatus.value!=='connected'){this.connectWebSocket();}});window.addEventListener('online',()=>{if(this.connectionStatus.value!=='connected'){this.connectWebSocket();}});watch(()=>authStore.isLoggedIn,(isLoggedIn)=>{if(isLoggedIn&&this.connectionStatus.value!=='connected'){this.connectWebSocket();}else if(!isLoggedIn){this.disconnectWebSocket();}},{immediate:true});}}export const chatService=new ChatService();export default chatService;