from __future__ import annotations
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.db.session import get_db_context
from app.models.chat import ChatRoom, ChatMember, ChatMessage, MessageReaction, ChatRoomType, ChatMemberRole, MessageType
from app.models.user import User
logger = logging.getLogger(__name__)
class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_room(self, name: Optional[str], room_type: ChatRoomType, creator_id: str, company_id: Optional[str]=None, members: Optional[List[Dict[str, Any]]]=None) -> ChatRoom:
        if room_type == ChatRoomType.DIRECT and members and (len(members) != 2):
            raise ValueError('Direct chat rooms must have exactly 2 members')
        if room_type == ChatRoomType.COMPANY and (not company_id):
            raise ValueError('Company rooms must have a company_id')
        room = ChatRoom(name=name, type=room_type, company_id=uuid.UUID(company_id) if company_id else None, is_active=True, metadata={})
        self.db.add(room)
        await self.db.flush()
        creator_member = ChatMember(room_id=room.id, user_id=uuid.UUID(creator_id), role=ChatMemberRole.OWNER, is_active=True)
        self.db.add(creator_member)
        if members:
            for member_data in members:
                if member_data.get('user_id') == creator_id:
                    continue
                member = ChatMember(room_id=room.id, user_id=uuid.UUID(member_data['user_id']), role=member_data.get('role', ChatMemberRole.MEMBER), is_active=True)
                self.db.add(member)
        await self.db.commit()
        await self.db.refresh(room)
        return room
    async def get_room(self, room_id: str) -> Optional[ChatRoom]:
        query = select(ChatRoom).where(ChatRoom.id == uuid.UUID(room_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    async def get_room_with_members(self, room_id: str) -> Optional[ChatRoom]:
        query = select(ChatRoom).options(joinedload(ChatRoom.members).joinedload(ChatMember.user)).where(ChatRoom.id == uuid.UUID(room_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    async def get_user_rooms(self, user_id: str) -> List[Dict[str, Any]]:
        query = select(ChatRoom, ChatMember).join(ChatMember, ChatRoom.id == ChatMember.room_id).where(and_(ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True, ChatRoom.is_active == True))
        result = await self.db.execute(query)
        user_rooms = []
        for room, member in result:
            last_message_query = select(ChatMessage).where(ChatMessage.room_id == room.id).order_by(desc(ChatMessage.created_at)).limit(1)
            last_message_result = await self.db.execute(last_message_query)
            last_message = last_message_result.scalar_one_or_none()
            unread_count = await self.get_unread_count(str(room.id), user_id, member.last_read_at)
            member_count_query = select(func.count()).select_from(ChatMember).where(and_(ChatMember.room_id == room.id, ChatMember.is_active == True))
            member_count_result = await self.db.execute(member_count_query)
            member_count = member_count_result.scalar() or 0
            room_data = {'id': str(room.id), 'name': room.name, 'type': room.type, 'created_at': room.created_at.isoformat(), 'member_count': member_count, 'user_role': member.role, 'unread_count': unread_count, 'last_message': None}
            if last_message:
                sender_query = select(User).where(User.id == last_message.sender_id)
                sender_result = await self.db.execute(sender_query)
                sender = sender_result.scalar_one_or_none()
                room_data['last_message'] = {'id': str(last_message.id), 'sender_id': str(last_message.sender_id) if last_message.sender_id else None, 'sender_name': sender.full_name if sender else None, 'content': last_message.content, 'message_type': last_message.message_type, 'created_at': last_message.created_at.isoformat(), 'is_deleted': last_message.is_deleted}
            user_rooms.append(room_data)
        return user_rooms
    async def get_room_info(self, room_id: str) -> Dict[str, Any]:
        room = await self.get_room_with_members(room_id)
        if not room:
            return {}
        members = []
        for member in room.members:
            if member.is_active:
                members.append({'user_id': str(member.user_id), 'user_name': member.user.full_name if member.user else 'Unknown', 'role': member.role, 'last_read_at': member.last_read_at.isoformat() if member.last_read_at else None})
        last_message_query = select(ChatMessage).where(ChatMessage.room_id == room.id).order_by(desc(ChatMessage.created_at)).limit(1)
        last_message_result = await self.db.execute(last_message_query)
        last_message = last_message_result.scalar_one_or_none()
        room_data = {'id': str(room.id), 'name': room.name, 'type': room.type, 'created_at': room.created_at.isoformat(), 'member_count': len(members), 'members': members, 'company_id': str(room.company_id) if room.company_id else None, 'metadata': room.metadata, 'last_message': None}
        if last_message:
            sender_query = select(User).where(User.id == last_message.sender_id)
            sender_result = await self.db.execute(sender_query)
            sender = sender_result.scalar_one_or_none()
            room_data['last_message'] = {'id': str(last_message.id), 'sender_id': str(last_message.sender_id) if last_message.sender_id else None, 'sender_name': sender.full_name if sender else None, 'content': last_message.content, 'message_type': last_message.message_type, 'created_at': last_message.created_at.isoformat(), 'is_deleted': last_message.is_deleted}
        return room_data
    async def check_room_access(self, user_id: str, room_id: str) -> bool:
        query = select(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True))
        result = await self.db.execute(query)
        member = result.scalar_one_or_none()
        return member is not None
    async def create_message(self, room_id: str, sender_id: str, content: str, message_type: str='text', metadata: Optional[Dict[str, Any]]=None) -> ChatMessage:
        message = ChatMessage(room_id=uuid.UUID(room_id), sender_id=uuid.UUID(sender_id), message_type=message_type, metadata=metadata or {}, is_deleted=False)
        message.content = content
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message
    async def edit_message(self, message_id: str, content: str) -> Tuple[bool, Optional[ChatMessage]]:
        query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
        result = await self.db.execute(query)
        message = result.scalar_one_or_none()
        if not message:
            return (False, None)
        message.content = content
        await self.db.commit()
        await self.db.refresh(message)
        return (True, message)
    async def delete_message(self, message_id: str) -> bool:
        query = update(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id)).values(is_deleted=True, deleted_at=datetime.utcnow())
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
    async def check_message_permission(self, message_id: str, user_id: str, require_admin: bool=False) -> bool:
        message_query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
        message_result = await self.db.execute(message_query)
        message = message_result.scalar_one_or_none()
        if not message:
            return False
        if message.sender_id == uuid.UUID(user_id):
            return True
        if require_admin:
            member_query = select(ChatMember).where(and_(ChatMember.room_id == message.room_id, ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True, or_(ChatMember.role == ChatMemberRole.ADMIN, ChatMember.role == ChatMemberRole.OWNER)))
            member_result = await self.db.execute(member_query)
            member = member_result.scalar_one_or_none()
            return member is not None
        return False
    async def mark_as_read(self, user_id: str, room_id: str, last_read_id: str) -> bool:
        message_query = select(ChatMessage).where(and_(ChatMessage.id == uuid.UUID(last_read_id), ChatMessage.room_id == uuid.UUID(room_id)))
        message_result = await self.db.execute(message_query)
        message = message_result.scalar_one_or_none()
        if not message:
            return False
        member_query = update(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id))).values(last_read_at=message.created_at)
        result = await self.db.execute(member_query)
        await self.db.commit()
        return result.rowcount > 0
    async def get_unread_count(self, room_id: str, user_id: str, last_read_at: Optional[datetime]=None) -> int:
        if not last_read_at:
            member_query = select(ChatMember.last_read_at).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id)))
            member_result = await self.db.execute(member_query)
            member_last_read = member_result.scalar_one_or_none()
            if not member_last_read:
                count_query = select(func.count()).select_from(ChatMessage).where(and_(ChatMessage.room_id == uuid.UUID(room_id), ChatMessage.sender_id != uuid.UUID(user_id)))
            else:
                count_query = select(func.count()).select_from(ChatMessage).where(and_(ChatMessage.room_id == uuid.UUID(room_id), ChatMessage.created_at > member_last_read, ChatMessage.sender_id != uuid.UUID(user_id)))
        else:
            count_query = select(func.count()).select_from(ChatMessage).where(and_(ChatMessage.room_id == uuid.UUID(room_id), ChatMessage.created_at > last_read_at, ChatMessage.sender_id != uuid.UUID(user_id)))
        count_result = await self.db.execute(count_query)
        return count_result.scalar() or 0
    async def get_message_history(self, room_id: str, before_id: Optional[str]=None, limit: int=50) -> List[Dict[str, Any]]:
        if before_id:
            before_query = select(ChatMessage.created_at).where(ChatMessage.id == uuid.UUID(before_id))
            before_result = await self.db.execute(before_query)
            before_time = before_result.scalar_one_or_none()
            if before_time:
                query = select(ChatMessage).where(and_(ChatMessage.room_id == uuid.UUID(room_id), ChatMessage.created_at < before_time)).order_by(desc(ChatMessage.created_at)).limit(limit)
            else:
                query = select(ChatMessage).where(ChatMessage.room_id == uuid.UUID(room_id)).order_by(desc(ChatMessage.created_at)).limit(limit)
        else:
            query = select(ChatMessage).where(ChatMessage.room_id == uuid.UUID(room_id)).order_by(desc(ChatMessage.created_at)).limit(limit)
        result = await self.db.execute(query)
        messages = result.scalars().all()
        messages = list(reversed(messages))
        formatted_messages = []
        for message in messages:
            sender_name = None
            if message.sender_id:
                sender_query = select(User.full_name).where(User.id == message.sender_id)
                sender_result = await self.db.execute(sender_query)
                sender_name = sender_result.scalar_one_or_none()
            reactions_query = select(MessageReaction).where(MessageReaction.message_id == message.id)
            reactions_result = await self.db.execute(reactions_query)
            reactions = reactions_result.scalars().all()
            reaction_data = {}
            for reaction in reactions:
                if reaction.reaction not in reaction_data:
                    reaction_data[reaction.reaction] = []
                reaction_data[reaction.reaction].append(str(reaction.user_id))
            formatted_messages.append({'id': str(message.id), 'room_id': str(message.room_id), 'sender_id': str(message.sender_id) if message.sender_id else None, 'sender_name': sender_name, 'message_type': message.message_type, 'content': message.content, 'created_at': message.created_at.isoformat(), 'updated_at': message.updated_at.isoformat(), 'is_deleted': message.is_deleted, 'reactions': reaction_data, 'metadata': message.metadata})
        return formatted_messages
    async def add_reaction(self, message_id: str, user_id: str, reaction: str) -> bool:
        query = select(MessageReaction).where(and_(MessageReaction.message_id == uuid.UUID(message_id), MessageReaction.user_id == uuid.UUID(user_id), MessageReaction.reaction == reaction))
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            return True
        message_reaction = MessageReaction(message_id=uuid.UUID(message_id), user_id=uuid.UUID(user_id), reaction=reaction)
        self.db.add(message_reaction)
        try:
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error adding reaction: {e}')
            await self.db.rollback()
            return False
    async def remove_reaction(self, message_id: str, user_id: str, reaction: str) -> bool:
        query = select(MessageReaction).where(and_(MessageReaction.message_id == uuid.UUID(message_id), MessageReaction.user_id == uuid.UUID(user_id), MessageReaction.reaction == reaction))
        result = await self.db.execute(query)
        reaction_obj = result.scalar_one_or_none()
        if not reaction_obj:
            return False
        await self.db.delete(reaction_obj)
        try:
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error removing reaction: {e}')
            await self.db.rollback()
            return False
    async def add_member(self, room_id: str, user_id: str, role: ChatMemberRole=ChatMemberRole.MEMBER) -> bool:
        query = select(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id)))
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        if existing:
            if not existing.is_active:
                existing.is_active = True
                existing.role = role
                await self.db.commit()
            return True
        member = ChatMember(room_id=uuid.UUID(room_id), user_id=uuid.UUID(user_id), role=role, is_active=True)
        self.db.add(member)
        try:
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error adding member: {e}')
            await self.db.rollback()
            return False
    async def remove_member(self, room_id: str, user_id: str) -> bool:
        query = select(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True))
        result = await self.db.execute(query)
        member = result.scalar_one_or_none()
        if not member:
            return False
        member.is_active = False
        try:
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error removing member: {e}')
            await self.db.rollback()
            return False
    async def update_member_role(self, room_id: str, user_id: str, role: ChatMemberRole) -> bool:
        query = select(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True))
        result = await self.db.execute(query)
        member = result.scalar_one_or_none()
        if not member:
            return False
        member.role = role
        try:
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error updating member role: {e}')
            await self.db.rollback()
            return False
    async def find_direct_chat(self, user_id1: str, user_id2: str) -> Optional[str]:
        query = select(ChatRoom).join(ChatMember, ChatRoom.id == ChatMember.room_id).where(and_(ChatRoom.type == ChatRoomType.DIRECT, ChatRoom.is_active == True, ChatMember.user_id == uuid.UUID(user_id1), ChatMember.is_active == True))
        result = await self.db.execute(query)
        rooms = result.scalars().all()
        for room in rooms:
            member_query = select(ChatMember).where(and_(ChatMember.room_id == room.id, ChatMember.user_id == uuid.UUID(user_id2), ChatMember.is_active == True))
            member_result = await self.db.execute(member_query)
            member = member_result.scalar_one_or_none()
            if member:
                return str(room.id)
        return None
    async def create_direct_chat(self, user_id1: str, user_id2: str) -> str:
        existing_room_id = await self.find_direct_chat(user_id1, user_id2)
        if existing_room_id:
            return existing_room_id
        members = [{'user_id': user_id1, 'role': ChatMemberRole.MEMBER}, {'user_id': user_id2, 'role': ChatMemberRole.MEMBER}]
        room = await self.create_room(name=None, room_type=ChatRoomType.DIRECT, creator_id=user_id1, members=members)
        return str(room.id)