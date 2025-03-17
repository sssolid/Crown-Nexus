import{ref,reactive,computed,ComputedRef}from 'vue';import api from '@/services/api';import{ChatRoom,ChatMessage,ChatMember,ChatRoomType,ChatMemberRole,MessageType,WebSocketCommand,WebSocketResponse,UserPresence}from '@/types/chat';import{useAuthStore}from '@/stores/auth';import{notificationService}from '@/utils/notification';const chatRooms=reactive<Record<string,ChatRoom>>({});const activeRoomId=ref<string|null>(null);const messages=reactive<Record<string,ChatMessage[]>>({});const members=reactive<Record<string,ChatMember[]>>({});const isLoading=ref(false);const wsConnection=ref<WebSocket|null>(null);const connectionStatus=ref<'connected'|'connecting'|'disconnected'>('disconnected');const userPresence=reactive<Record<string,UserPresence>>({});const userTyping=reactive<Record<string,Record<string,number>>>({});let reconnectAttempts=0;const maxReconnectAttempts=5;const reconnectDelay=2000;let reconnectTimer:ReturnType<typeof setTimeout>|null=null;const activeRoom:ComputedRef<ChatRoom|null>=computed(()=>{if(!activeRoomId.value)return null;return chatRooms[activeRoomId.value]||null;});const activeRoomMessages:ComputedRef<ChatMessage[]>=computed(()=>{if(!activeRoomId.value)return[];return messages[activeRoomId.value]||[];});const activeRoomMembers:ComputedRef<ChatMember[]>=computed(()=>{if(!activeRoomId.value)return[];return members[activeRoomId.value]||[];});const totalUnreadCount:ComputedRef<number>=computed(()=>{return Object.values(chatRooms).reduce((total,room)=>{return total+(room.unread_count||0);},0);});export function useChatService(){const authStore=useAuthStore();function connectWebSocket(){if(wsConnection.value&&wsConnection.value.readyState<2){return;}if(!authStore.token){console.error('Cannot connect WebSocket: No auth token');connectionStatus.value='disconnected';return;}try{const protocol=window.location.protocol==='https:'?'wss:':'ws:';const host=window.location.host;const wsUrl=`${protocol}
      
      connectionStatus.value = __STRING_15__;
      wsConnection.value = new WebSocket(wsUrl);
      
      
      wsConnection.value.onopen = handleWebSocketOpen;
      wsConnection.value.onmessage = handleWebSocketMessage;
      wsConnection.value.onclose = handleWebSocketClose;
      wsConnection.value.onerror = handleWebSocketError;
    } catch (error) {
      console.error(__STRING_16__, error);
      connectionStatus.value = __STRING_17__;
    }
  }
  
  
  function disconnectWebSocket() {
    if (wsConnection.value && wsConnection.value.readyState < 2) {
      wsConnection.value.close();
    }
    
    
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    
    wsConnection.value = null;
    connectionStatus.value = __STRING_18__;
  }
  
  
  function handleWebSocketOpen() {
    console.log(__STRING_19__);
    connectionStatus.value = __STRING_20__;
    reconnectAttempts = 0; 
    
    
    if (activeRoomId.value) {
      joinRoom(activeRoomId.value);
    }
  }
  
  
  function handleWebSocketClose(event: CloseEvent) {
    console.log(`WebSocket closed:${event.code}${event.reason}`);
    connectionStatus.value = __STRING_21__;
    wsConnection.value = null;
    
    
    if (event.code !== 1000) {
      attemptReconnect();
    }
  }
  
  
  function handleWebSocketError(event: Event) {
    console.error(__STRING_22__, event);
    
  }
  
  
  function attemptReconnect() {
    if (reconnectAttempts >= maxReconnectAttempts) {
      console.error(__STRING_23__);
      notificationService.error(__STRING_24__);
      return;
    }
    
    reconnectAttempts++;
    const delay = reconnectDelay * Math.pow(1.5, reconnectAttempts - 1);
    
    console.log(`Attempting to reconnect in ${delay}ms(attempt ${reconnectAttempts})`);
    
    reconnectTimer = setTimeout(() => {
      console.log(`Reconnecting...(attempt ${reconnectAttempts})`);
      connectWebSocket();
    }, delay);
  }
  
  
  function handleWebSocketMessage(event: MessageEvent) {
    try {
      const response: WebSocketResponse = JSON.parse(event.data);
      
      
      switch (response.type) {
        case __STRING_25__:
          handleConnectedMessage(response);
          break;
        
        case __STRING_26__:
          handleRoomListMessage(response);
          break;
        
        case __STRING_27__:
          handleRoomJoinedMessage(response);
          break;
        
        case __STRING_28__:
          handleUserJoinedMessage(response);
          break;
        
        case __STRING_29__:
          handleUserLeftMessage(response);
          break;
        
        case __STRING_30__:
          handleNewMessageMessage(response);
          break;
        
        case __STRING_31__:
          handleMessageSentMessage(response);
          break;
        
        case __STRING_32__:
          handleMessageHistoryMessage(response);
          break;
        
        case __STRING_33__:
          handleUserTypingMessage(response);
          break;
        
        case __STRING_34__:
          handleUserTypingStoppedMessage(response);
          break;
        
        case __STRING_35__:
          handleReactionAddedMessage(response);
          break;
        
        case __STRING_36__:
          handleReactionRemovedMessage(response);
          break;
        
        case __STRING_37__:
          handleMessageEditedMessage(response);
          break;
        
        case __STRING_38__:
          handleMessageDeletedMessage(response);
          break;
        
        case __STRING_39__:
          handleErrorMessage(response);
          break;
        
        default:
          console.warn(`Unknown message type:${response.type}`, response);
      }
    } catch (error) {
      console.error(__STRING_40__, error, event.data);
    }
  }
  
  
  function handleConnectedMessage(response: WebSocketResponse) {
    console.log(__STRING_41__, response.data);
  }
  
  
  function handleRoomListMessage(response: WebSocketResponse) {
    const rooms = response.data.rooms as ChatRoom[];
    
    
    rooms.forEach(room => {
      chatRooms[room.id] = room;
    });
  }
  
  
  function handleRoomJoinedMessage(response: WebSocketResponse) {
    const roomInfo = response.data as ChatRoom;
    
    
    chatRooms[roomInfo.id] = roomInfo;
    
    
    if (roomInfo.members) {
      members[roomInfo.id] = roomInfo.members;
    }
    
    
    if (activeRoomId.value === roomInfo.id) {
      fetchMessageHistory(roomInfo.id);
    }
  }
  
  
  function handleUserJoinedMessage(response: WebSocketResponse) {
    const { room_id, user } = response.data;
    
    
    if (chatRooms[room_id]) {
      chatRooms[room_id].member_count = (chatRooms[room_id].member_count || 0) + 1;
    }
    
    
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
        
        existingMember.is_online = true;
      }
    }
    
    
    if (messages[room_id]) {
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
      
      messages[room_id].push(systemMessage);
    }
  }
  
  
  function handleUserLeftMessage(response: WebSocketResponse) {
    const { room_id, user_id } = response.data;
    
    
    if (chatRooms[room_id]) {
      chatRooms[room_id].member_count = Math.max(0, (chatRooms[room_id].member_count || 1) - 1);
    }
    
    
    if (members[room_id]) {
      const memberIndex = members[room_id].findIndex(m => m.user_id === user_id);
      
      if (memberIndex !== -1) {
        const userName = members[room_id][memberIndex].user_name;
        members[room_id].splice(memberIndex, 1);
        
        
        if (messages[room_id]) {
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
          
          messages[room_id].push(systemMessage);
        }
      }
    }
  }
  
  
  function handleNewMessageMessage(response: WebSocketResponse) {
    const messageData = response.data as ChatMessage;
    
    
    if (!messages[messageData.room_id]) {
      messages[messageData.room_id] = [];
    }
    
    messages[messageData.room_id].push(messageData);
    
    
    if (chatRooms[messageData.room_id]) {
      chatRooms[messageData.room_id].last_message = messageData;
      
      
      if (activeRoomId.value !== messageData.room_id) {
        chatRooms[messageData.room_id].unread_count = 
          (chatRooms[messageData.room_id].unread_count || 0) + 1;
      }
    }
    
    
    if (activeRoomId.value !== messageData.room_id) {
      playNotificationSound();
    }
  }
  
  
  function handleMessageSentMessage(response: WebSocketResponse) {
    const messageData = response.data as ChatMessage;
    
    
    if (!messages[messageData.room_id]) {
      messages[messageData.room_id] = [];
    }
    
    
    const tempIndex = messages[messageData.room_id].findIndex(
      m => m.id.startsWith(__STRING_42__) && m.content === messageData.content
    );
    
    if (tempIndex !== -1) {
      
      messages[messageData.room_id][tempIndex] = messageData;
    } else {
      
      messages[messageData.room_id].push(messageData);
    }
    
    
    if (chatRooms[messageData.room_id]) {
      chatRooms[messageData.room_id].last_message = messageData;
    }
  }
  
  
  function handleMessageHistoryMessage(response: WebSocketResponse) {
    const { room_id, messages: messageHistory } = response.data;
    
    if (!messages[room_id]) {
      messages[room_id] = [];
    }
    
    
    messages[room_id] = [...messageHistory, ...messages[room_id]];
  }
  
  
  function handleUserTypingMessage(response: WebSocketResponse) {
    const { room_id, user_id, user_name } = response.data;
    
    
    if (!userTyping[room_id]) {
      userTyping[room_id] = {};
    }
    
    
    userTyping[room_id][user_id] = Date.now();
    
    
    setTimeout(() => {
      if (userTyping[room_id] && userTyping[room_id][user_id]) {
        const elapsed = Date.now() - userTyping[room_id][user_id];
        if (elapsed > 5000) {
          delete userTyping[room_id][user_id];
        }
      }
    }, 5000);
  }
  
  
  function handleUserTypingStoppedMessage(response: WebSocketResponse) {
    const { room_id, user_id } = response.data;
    
    
    if (userTyping[room_id] && userTyping[room_id][user_id]) {
      delete userTyping[room_id][user_id];
    }
  }
  
  
  function handleReactionAddedMessage(response: WebSocketResponse) {
    const { room_id, message_id, reaction, user_id } = response.data;
    
    if (!messages[room_id]) return;
    
    
    const message = messages[room_id].find(m => m.id === message_id);
    if (!message) return;
    
    
    if (!message.reactions[reaction]) {
      message.reactions[reaction] = [];
    }
    
    if (!message.reactions[reaction].includes(user_id)) {
      message.reactions[reaction].push(user_id);
    }
  }
  
  
  function handleReactionRemovedMessage(response: WebSocketResponse) {
    const { room_id, message_id, reaction, user_id } = response.data;
    
    if (!messages[room_id]) return;
    
    
    const message = messages[room_id].find(m => m.id === message_id);
    if (!message || !message.reactions[reaction]) return;
    
    
    const index = message.reactions[reaction].indexOf(user_id);
    if (index !== -1) {
      message.reactions[reaction].splice(index, 1);
      
      
      if (message.reactions[reaction].length === 0) {
        delete message.reactions[reaction];
      }
    }
  }
  
  
  function handleMessageEditedMessage(response: WebSocketResponse) {
    const { id, room_id, content, updated_at } = response.data;
    
    if (!messages[room_id]) return;
    
    
    const message = messages[room_id].find(m => m.id === id);
    if (message) {
      message.content = content;
      message.updated_at = updated_at;
      message.is_edited = true;
    }
  }
  
  
  function handleMessageDeletedMessage(response: WebSocketResponse) {
    const { room_id, message_id } = response.data;
    
    if (!messages[room_id]) return;
    
    
    const message = messages[room_id].find(m => m.id === message_id);
    if (message) {
      message.is_deleted = true;
      message.content = __STRING_0__;
    }
  }
  
  
  function handleErrorMessage(response: WebSocketResponse) {
    console.error(__STRING_43__, response.error);
    notificationService.error(response.error || __STRING_44__);
  }
  
  
  function sendCommand(command: WebSocketCommand) {
    if (connectionStatus.value !== __STRING_45__ || !wsConnection.value) {
      console.error(__STRING_46__);
      return false;
    }
    
    try {
      wsConnection.value.send(JSON.stringify(command));
      return true;
    } catch (error) {
      console.error(__STRING_47__, error);
      return false;
    }
  }
  
  
  function joinRoom(roomId: string) {
    
    activeRoomId.value = roomId;
    
    
    sendCommand({
      command: __STRING_48__,
      room_id: roomId,
      data: { room_id: roomId }
    });
    
    
    if (chatRooms[roomId] && chatRooms[roomId].unread_count) {
      chatRooms[roomId].unread_count = 0;
    }
  }
  
  
  function leaveRoom(roomId: string) {
    
    sendCommand({
      command: __STRING_49__,
      room_id: roomId,
      data: { room_id: roomId }
    });
    
    
    if (activeRoomId.value === roomId) {
      activeRoomId.value = null;
    }
  }
  
  
  function sendMessage(roomId: string, content: string, messageType = MessageType.TEXT) {
    if (!content.trim()) return false;
    
    
    const tempId = `temp-${Date.now()}`;
    
    
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
    
    
    return sendCommand({
      command: __STRING_50__,
      room_id: roomId,
      data: {
        room_id: roomId,
        content,
        message_type: messageType
      }
    });
  }
  
  
  function editMessage(messageId: string, roomId: string, content: string) {
    if (!content.trim()) return false;
    
    return sendCommand({
      command: __STRING_51__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        content
      }
    });
  }
  
  
  function deleteMessage(messageId: string, roomId: string) {
    return sendCommand({
      command: __STRING_52__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId
      }
    });
  }
  
  
  function addReaction(messageId: string, roomId: string, reaction: string) {
    return sendCommand({
      command: __STRING_53__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }
  
  
  function removeReaction(messageId: string, roomId: string, reaction: string) {
    return sendCommand({
      command: __STRING_54__,
      room_id: roomId,
      data: {
        room_id: roomId,
        message_id: messageId,
        reaction
      }
    });
  }
  
  
  function sendTypingStart(roomId: string) {
    return sendCommand({
      command: __STRING_55__,
      room_id: roomId,
      data: { room_id: roomId }
    });
  }
  
  
  function sendTypingStop(roomId: string) {
    return sendCommand({
      command: __STRING_56__,
      room_id: roomId,
      data: { room_id: roomId }
    });
  }
  
  
  function fetchMessageHistory(roomId: string, beforeId?: string) {
    return sendCommand({
      command: __STRING_57__,
      room_id: roomId,
      data: {
        room_id: roomId,
        before_id: beforeId,
        limit: 50
      }
    });
  }
  
  
  function markAsRead(roomId: string, lastReadId: string) {
    return sendCommand({
      command: __STRING_58__,
      room_id: roomId,
      data: {
        room_id: roomId,
        last_read_id: lastReadId
      }
    });
  }
  
  
  async function createRoom(name: string, type: ChatRoomType, members?: any[]) {
    isLoading.value = true;
    
    try {
      const response = await api.post(__STRING_59__, {
        name,
        type,
        members
      });
      
      if (response.success && response.room) {
        
        chatRooms[response.room.id] = response.room;
        return response.room;
      }
      
      return null;
    } catch (error) {
      console.error(__STRING_60__, error);
      notificationService.error(__STRING_61__);
      return null;
    } finally {
      isLoading.value = false;
    }
  }
  
  
  async function createDirectChat(userId: string) {
    isLoading.value = true;
    
    try {
      const response = await api.post(__STRING_62__, {
        user_id: userId
      });
      
      if (response.success && response.room) {
        
        chatRooms[response.room.id] = response.room;
        return response.room;
      }
      
      return null;
    } catch (error) {
      console.error(__STRING_63__, error);
      notificationService.error(__STRING_64__);
      return null;
    } finally {
      isLoading.value = false;
    }
  }
  
  
  async function fetchRooms() {
    isLoading.value = true;
    
    try {
      const response = await api.get(__STRING_65__);
      
      if (response.success && response.rooms) {
        
        response.rooms.forEach((room: ChatRoom) => {
          chatRooms[room.id] = room;
        });
      }
    } catch (error) {
      console.error(__STRING_66__, error);
      notificationService.error(__STRING_67__);
    } finally {
      isLoading.value = false;
    }
  }
  
  
  async function addMember(roomId: string, userId: string, role = ChatMemberRole.MEMBER) {
    isLoading.value = true;
    
    try {
      const response = await api.post(`/chat/rooms/${roomId}/members`, {
        user_id: userId,
        role
      });
      
      return response.success;
    } catch (error) {
      console.error(__STRING_68__, error);
      notificationService.error(__STRING_69__);
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  
  
  async function removeMember(roomId: string, userId: string) {
    isLoading.value = true;
    
    try {
      const response = await api.delete(`/chat/rooms/${roomId}/members/${userId}`);
      return response.success;
    } catch (error) {
      console.error(__STRING_70__, error);
      notificationService.error(__STRING_71__);
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  
  
  async function updateMemberRole(roomId: string, userId: string, role: ChatMemberRole) {
    isLoading.value = true;
    
    try {
      const response = await api.put(`/chat/rooms/${roomId}/members/${userId}`,{role});return response.success;}catch(error){console.error('Error updating member role:',error);notificationService.error('Failed to update member role');return false;}finally{isLoading.value=false;}}function getTypingUsers(roomId:string):string[]{if(!userTyping[roomId])return[];const now=Date.now();const typingUsers:string[]=[];Object.entries(userTyping[roomId]).forEach(([userId,timestamp])=>{if(now-timestamp<5000){if(members[roomId]){const member=members[roomId].find(m=>m.user_id===userId);if(member){typingUsers.push(member.user_name);}}}else{delete userTyping[roomId][userId];}});return typingUsers;}function playNotificationSound(){const audio=new Audio('/sounds/notification.mp3');audio.volume=0.5;audio.play().catch(e=>console.log('Failed to play notification sound:',e));}function initialize(){connectWebSocket();fetchRooms();document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&connectionStatus.value!=='connected'){connectWebSocket();}});window.addEventListener('online',()=>{if(connectionStatus.value!=='connected'){connectWebSocket();}});watch(()=>authStore.isLoggedIn,(isLoggedIn)=>{if(isLoggedIn&&connectionStatus.value!=='connected'){connectWebSocket();}else if(!isLoggedIn){disconnectWebSocket();}},{immediate:true});}return{chatRooms,messages,members,activeRoomId,activeRoom,activeRoomMessages,activeRoomMembers,isLoading,connectionStatus,totalUnreadCount,initialize,connectWebSocket,disconnectWebSocket,sendMessage,editMessage,deleteMessage,addReaction,removeReaction,joinRoom,leaveRoom,sendTypingStart,sendTypingStop,fetchMessageHistory,markAsRead,createRoom,createDirectChat,fetchRooms,addMember,removeMember,updateMemberRole,getTypingUsers};}export const chatService=useChatService();