// frontend/src/types/chat.ts
export enum ChatRoomType {
  DIRECT = 'direct',
  GROUP = 'group',
  COMPANY = 'company',
  SUPPORT = 'support'
}

export enum ChatMemberRole {
  OWNER = 'owner',
  ADMIN = 'admin',
  MEMBER = 'member',
  GUEST = 'guest'
}

export enum MessageType {
  TEXT = 'text',
  IMAGE = 'image',
  FILE = 'file',
  SYSTEM = 'system',
  ACTION = 'action'
}

export interface ChatRoom {
  id: string;
  name: string | null;
  type: ChatRoomType;
  created_at: string;
  member_count: number;
  user_role?: ChatMemberRole;
  unread_count?: number;
  last_message?: ChatMessage | null;
  company_id?: string | null;
  metadata: Record<string, any>;
}

export interface ChatMember {
  user_id: string;
  user_name: string;
  role: ChatMemberRole;
  last_read_at?: string | null;
  is_online?: boolean;
}

export interface ChatMessage {
  id: string;
  room_id: string;
  sender_id: string | null;
  sender_name: string | null;
  message_type: MessageType;
  content: string;
  created_at: string;
  updated_at: string;
  is_edited: boolean;
  is_deleted: boolean;
  reactions: Record<string, string[]>;
  metadata: Record<string, any>;
}

export interface ChatNotification {
  id: string;
  room_id: string;
  message_id?: string;
  type: string;
  content: string;
  created_at: string;
  is_read: boolean;
}

export interface TypingIndicator {
  user_id: string;
  user_name: string;
  room_id: string;
  timestamp: number;
}

export interface ChatServiceState {
  chatRooms: Record<string, ChatRoom>;
  activeRoomId: string | null;
  activeRoom: ChatRoom | null;
  activeRoomMessages: ChatMessage[];
  activeRoomMembers: ChatMember[];
  typingUsers: Record<string, TypingIndicator[]>; // roomId -> list of typing users
}

export interface UserPresence {
  user_id: string;
  is_online: boolean;
  last_seen_at?: string | null;
  status?: string | null;
}

export interface WebSocketCommand {
  command: string;
  room_id?: string;
  data: Record<string, any>;
}

export interface WebSocketResponse {
  type: string;
  success: boolean;
  error?: string;
  data: Record<string, any>;
}
