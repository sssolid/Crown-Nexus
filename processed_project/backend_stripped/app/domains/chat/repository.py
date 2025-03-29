from __future__ import annotations
'Chat repository implementation.\n\nThis module provides data access and persistence operations for Chat entities.\n'
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.chat.models import ChatRoom, ChatMember, ChatMessage, MessageReaction, RateLimitLog, ChatRoomType, ChatMemberRole, MessageType
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException, PermissionDeniedException, RateLimitException
class ChatRoomRepository(BaseRepository[ChatRoom, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ChatRoom, db=db)
    async def find_direct_chat(self, user1_id: uuid.UUID, user2_id: uuid.UUID) -> Optional[ChatRoom]:
        subquery1 = select(ChatMember.room_id).where(ChatMember.user_id == user1_id, ChatMember.is_active == True).subquery()
        subquery2 = select(ChatMember.room_id).where(ChatMember.user_id == user2_id, ChatMember.is_active == True).subquery()
        query = select(ChatRoom).where(ChatRoom.id.in_(subquery1), ChatRoom.id.in_(subquery2), ChatRoom.type == ChatRoomType.DIRECT, ChatRoom.is_active == True, ChatRoom.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_rooms_for_user(self, user_id: uuid.UUID, room_type: Optional[ChatRoomType]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        conditions = [ChatMember.user_id == user_id, ChatMember.is_active == True, ChatRoom.is_active == True, ChatRoom.is_deleted == False]
        if room_type:
            conditions.append(ChatRoom.type == room_type)
        query = select(ChatRoom).join(ChatMember, ChatRoom.id == ChatMember.room_id).where(and_(*conditions)).order_by(desc(ChatRoom.updated_at))
        return await self.paginate(query, page, page_size)
    async def get_company_rooms(self, company_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(ChatRoom).where(ChatRoom.company_id == company_id, ChatRoom.is_active == True, ChatRoom.is_deleted == False).order_by(desc(ChatRoom.updated_at))
        return await self.paginate(query, page, page_size)
    async def create_direct_chat(self, user1_id: uuid.UUID, user2_id: uuid.UUID) -> Tuple[ChatRoom, List[ChatMember]]:
        existing_chat = await self.find_direct_chat(user1_id, user2_id)
        if existing_chat:
            raise BusinessException(message='Direct chat already exists between these users', details={'user1_id': str(user1_id), 'user2_id': str(user2_id), 'existing_chat_id': str(existing_chat.id)})
        room = ChatRoom(name=None, type=ChatRoomType.DIRECT, company_id=None, is_active=True)
        self.db.add(room)
        await self.db.flush()
        members = []
        member1 = ChatMember(room_id=room.id, user_id=user1_id, role=ChatMemberRole.MEMBER, is_active=True)
        member2 = ChatMember(room_id=room.id, user_id=user2_id, role=ChatMemberRole.MEMBER, is_active=True)
        self.db.add(member1)
        self.db.add(member2)
        await self.db.flush()
        members = [member1, member2]
        await self.db.refresh(room)
        for member in members:
            await self.db.refresh(member)
        return (room, members)
    async def create_group_chat(self, name: str, creator_id: uuid.UUID, member_ids: List[uuid.UUID], company_id: Optional[uuid.UUID]=None) -> Tuple[ChatRoom, List[ChatMember]]:
        unique_member_ids = set(member_ids)
        unique_member_ids.add(creator_id)
        if not unique_member_ids:
            raise BusinessException(message='Group chat must have at least one member')
        room = ChatRoom(name=name, type=ChatRoomType.GROUP, company_id=company_id, is_active=True)
        self.db.add(room)
        await self.db.flush()
        members = []
        for user_id in unique_member_ids:
            role = ChatMemberRole.OWNER if user_id == creator_id else ChatMemberRole.MEMBER
            member = ChatMember(room_id=room.id, user_id=user_id, role=role, is_active=True)
            self.db.add(member)
            members.append(member)
        await self.db.flush()
        await self.db.refresh(room)
        for member in members:
            await self.db.refresh(member)
        return (room, members)
    async def add_members(self, room_id: uuid.UUID, user_ids: List[uuid.UUID], role: ChatMemberRole=ChatMemberRole.MEMBER, added_by_id: uuid.UUID=None) -> List[ChatMember]:
        room = await self.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(resource_type='ChatRoom', resource_id=str(room_id))
        if added_by_id:
            if room.type == ChatRoomType.DIRECT:
                raise BusinessException(message='Cannot add members to a direct chat')
            member_repo = ChatMemberRepository(self.db)
            adder_member = await member_repo.find_by_room_and_user(room_id, added_by_id)
            if not adder_member or adder_member.role not in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
                raise PermissionDeniedException(message="You don't have permission to add members to this chat", action='add_members', resource_type='ChatRoom')
        member_repo = ChatMemberRepository(self.db)
        existing_members = await member_repo.get_by_room(room_id)
        existing_user_ids = {member.user_id for member in existing_members}
        new_members = []
        for user_id in user_ids:
            if user_id in existing_user_ids:
                continue
            member = ChatMember(room_id=room_id, user_id=user_id, role=role, is_active=True)
            self.db.add(member)
            new_members.append(member)
        if new_members:
            await self.db.flush()
            for member in new_members:
                await self.db.refresh(member)
        return new_members
    async def ensure_exists(self, room_id: uuid.UUID) -> ChatRoom:
        room = await self.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(resource_type='ChatRoom', resource_id=str(room_id))
        return room
class ChatMemberRepository(BaseRepository[ChatMember, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ChatMember, db=db)
    async def find_by_room_and_user(self, room_id: uuid.UUID, user_id: uuid.UUID) -> Optional[ChatMember]:
        query = select(ChatMember).where(ChatMember.room_id == room_id, ChatMember.user_id == user_id, ChatMember.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_room(self, room_id: uuid.UUID, active_only: bool=True) -> List[ChatMember]:
        conditions = [ChatMember.room_id == room_id, ChatMember.is_deleted == False]
        if active_only:
            conditions.append(ChatMember.is_active == True)
        query = select(ChatMember).where(and_(*conditions))
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_user(self, user_id: uuid.UUID) -> List[ChatMember]:
        query = select(ChatMember).where(ChatMember.user_id == user_id, ChatMember.is_active == True, ChatMember.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def update_last_read(self, room_id: uuid.UUID, user_id: uuid.UUID, timestamp: Optional[datetime]=None) -> Optional[ChatMember]:
        member = await self.find_by_room_and_user(room_id, user_id)
        if not member:
            return None
        if timestamp is None:
            timestamp = datetime.now()
        member.last_read_at = timestamp
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)
        return member
    async def update_role(self, room_id: uuid.UUID, user_id: uuid.UUID, new_role: ChatMemberRole, updated_by_id: uuid.UUID) -> Optional[ChatMember]:
        member = await self.find_by_room_and_user(room_id, user_id)
        if not member:
            return None
        updater = await self.find_by_room_and_user(room_id, updated_by_id)
        if not updater or updater.role not in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
            raise PermissionDeniedException(message="You don't have permission to update member roles", action='update_role', resource_type='ChatMember')
        if updater.role == ChatMemberRole.ADMIN and member.role == ChatMemberRole.OWNER:
            raise PermissionDeniedException(message='Administrators cannot change the role of the room owner', action='update_role', resource_type='ChatMember')
        member.role = new_role
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)
        return member
    async def remove_member(self, room_id: uuid.UUID, user_id: uuid.UUID, removed_by_id: uuid.UUID) -> bool:
        member = await self.find_by_room_and_user(room_id, user_id)
        if not member:
            return False
        if user_id == removed_by_id:
            return await self.delete(member.id)
        remover = await self.find_by_room_and_user(room_id, removed_by_id)
        if not remover or remover.role not in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
            raise PermissionDeniedException(message="You don't have permission to remove members from this chat", action='remove_member', resource_type='ChatMember')
        if remover.role == ChatMemberRole.ADMIN and member.role in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
            raise PermissionDeniedException(message='Administrators cannot remove owners or other administrators', action='remove_member', resource_type='ChatMember')
        return await self.delete(member.id)
    async def ensure_exists(self, member_id: uuid.UUID) -> ChatMember:
        member = await self.get_by_id(member_id)
        if not member:
            raise ResourceNotFoundException(resource_type='ChatMember', resource_id=str(member_id))
        return member
class ChatMessageRepository(BaseRepository[ChatMessage, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ChatMessage, db=db)
    async def get_room_messages(self, room_id: uuid.UUID, limit: int=50, before_id: Optional[uuid.UUID]=None, include_deleted: bool=False) -> List[ChatMessage]:
        conditions = [ChatMessage.room_id == room_id, ChatMessage.is_deleted == False]
        if not include_deleted:
            conditions.append(ChatMessage.is_deleted == False)
        if before_id:
            sub_query = select(ChatMessage.created_at).where(ChatMessage.id == before_id)
            sub_result = await self.db.execute(sub_query)
            reference_timestamp = sub_result.scalar()
            if reference_timestamp:
                conditions.append(ChatMessage.created_at < reference_timestamp)
        query = select(ChatMessage).where(and_(*conditions)).order_by(desc(ChatMessage.created_at)).limit(limit)
        result = await self.db.execute(query)
        messages = list(result.scalars().all())
        return list(reversed(messages))
    async def send_message(self, room_id: uuid.UUID, sender_id: uuid.UUID, content: str, message_type: MessageType=MessageType.TEXT, extra_metadata: Optional[Dict[str, Any]]=None) -> ChatMessage:
        await self.check_rate_limit(sender_id, room_id, 'send_message')
        room_repo = ChatRoomRepository(self.db)
        room = await room_repo.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(resource_type='ChatRoom', resource_id=str(room_id))
        member_repo = ChatMemberRepository(self.db)
        member = await member_repo.find_by_room_and_user(room_id, sender_id)
        if not member or not member.is_active:
            raise PermissionDeniedException(message='You are not a member of this chat room', action='send_message', resource_type='ChatRoom')
        message = ChatMessage(room_id=room_id, sender_id=sender_id, message_type=message_type, extra_metadata=extra_metadata or {})
        message.content = content
        self.db.add(message)
        await self.db.flush()
        await member_repo.update_last_read(room_id, sender_id)
        room.updated_at = datetime.now()
        self.db.add(room)
        await self.db.flush()
        await self.db.refresh(message)
        return message
    async def edit_message(self, message_id: uuid.UUID, new_content: str, edited_by_id: uuid.UUID) -> Optional[ChatMessage]:
        message = await self.get_by_id(message_id)
        if not message or message.is_deleted:
            return None
        if message.sender_id != edited_by_id:
            raise PermissionDeniedException(message='You can only edit your own messages', action='edit_message', resource_type='ChatMessage')
        message.content = new_content
        message.updated_at = datetime.now()
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message
    async def delete_message(self, message_id: uuid.UUID, deleted_by_id: uuid.UUID) -> Optional[ChatMessage]:
        message = await self.get_by_id(message_id)
        if not message or message.is_deleted:
            return None
        if message.sender_id != deleted_by_id:
            member_repo = ChatMemberRepository(self.db)
            member = await member_repo.find_by_room_and_user(message.room_id, deleted_by_id)
            if not member or member.role not in [ChatMemberRole.OWNER, ChatMemberRole.ADMIN]:
                raise PermissionDeniedException(message="You don't have permission to delete this message", action='delete_message', resource_type='ChatMessage')
        message.is_deleted = True
        message.deleted_at = datetime.now()
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message
    async def check_rate_limit(self, user_id: uuid.UUID, room_id: uuid.UUID, event_type: str, max_count: int=10, window_seconds: int=60) -> None:
        window_start = datetime.now() - timedelta(seconds=window_seconds)
        query = select(func.count()).select_from(RateLimitLog).where(RateLimitLog.user_id == user_id, RateLimitLog.room_id == room_id, RateLimitLog.event_type == event_type, RateLimitLog.timestamp >= window_start)
        result = await self.db.execute(query)
        count = result.scalar() or 0
        if count >= max_count:
            oldest_query = select(RateLimitLog.timestamp).where(RateLimitLog.user_id == user_id, RateLimitLog.room_id == room_id, RateLimitLog.event_type == event_type, RateLimitLog.timestamp >= window_start).order_by(RateLimitLog.timestamp).limit(1)
            oldest_result = await self.db.execute(oldest_query)
            oldest_timestamp = oldest_result.scalar()
            if oldest_timestamp:
                reset_time = oldest_timestamp + timedelta(seconds=window_seconds)
                seconds_remaining = int((reset_time - datetime.now()).total_seconds())
                raise RateLimitException(message=f'Rate limit exceeded for {event_type}. Try again later.', headers={'X-RateLimit-Limit': str(max_count), 'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(seconds_remaining)})
        log = RateLimitLog(user_id=user_id, room_id=room_id, event_type=event_type, timestamp=datetime.now(), count=1)
        self.db.add(log)
        await self.db.flush()
    async def ensure_exists(self, message_id: uuid.UUID) -> ChatMessage:
        message = await self.get_by_id(message_id)
        if not message:
            raise ResourceNotFoundException(resource_type='ChatMessage', resource_id=str(message_id))
        return message
class MessageReactionRepository(BaseRepository[MessageReaction, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=MessageReaction, db=db)
    async def find_by_message_user_reaction(self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str) -> Optional[MessageReaction]:
        query = select(MessageReaction).where(MessageReaction.message_id == message_id, MessageReaction.user_id == user_id, MessageReaction.reaction == reaction, MessageReaction.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_message(self, message_id: uuid.UUID) -> List[MessageReaction]:
        query = select(MessageReaction).where(MessageReaction.message_id == message_id, MessageReaction.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def add_reaction(self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str) -> MessageReaction:
        existing_reaction = await self.find_by_message_user_reaction(message_id, user_id, reaction)
        if existing_reaction:
            return existing_reaction
        message_repo = ChatMessageRepository(self.db)
        message = await message_repo.get_by_id(message_id)
        if not message or message.is_deleted:
            raise ResourceNotFoundException(resource_type='ChatMessage', resource_id=str(message_id))
        member_repo = ChatMemberRepository(self.db)
        member = await member_repo.find_by_room_and_user(message.room_id, user_id)
        if not member or not member.is_active:
            raise PermissionDeniedException(message='You are not a member of this chat room', action='add_reaction', resource_type='ChatRoom')
        reaction_obj = MessageReaction(message_id=message_id, user_id=user_id, reaction=reaction)
        self.db.add(reaction_obj)
        await self.db.flush()
        await self.db.refresh(reaction_obj)
        return reaction_obj
    async def remove_reaction(self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str) -> bool:
        existing_reaction = await self.find_by_message_user_reaction(message_id, user_id, reaction)
        if not existing_reaction:
            return False
        return await self.delete(existing_reaction.id)
    async def get_reaction_counts(self, message_id: uuid.UUID) -> Dict[str, int]:
        query = select(MessageReaction.reaction, func.count(MessageReaction.id)).where(MessageReaction.message_id == message_id, MessageReaction.is_deleted == False).group_by(MessageReaction.reaction)
        result = await self.db.execute(query)
        return {reaction: count for reaction, count in result.all()}
    async def get_user_reactions(self, message_id: uuid.UUID, reaction: str) -> List[uuid.UUID]:
        query = select(MessageReaction.user_id).where(MessageReaction.message_id == message_id, MessageReaction.reaction == reaction, MessageReaction.is_deleted == False)
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]