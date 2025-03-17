from __future__ import annotations
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.exceptions import AuthenticationException, BusinessLogicException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger
from app.db.session import get_db_context
from app.models.chat import ChatMember, ChatMemberRole, ChatMessage, ChatRoom, ChatRoomType, MessageReaction, MessageType
from app.models.user import User
from app.utils.crypto import decrypt_message, encrypt_message
logger = get_logger('app.services.chat')
class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_room(self, name: Optional[str], room_type: str, creator_id: str, company_id: Optional[str]=None, members: Optional[List[Dict[str, Any]]]=None) -> ChatRoom:
        try:
            chat_room_type = ChatRoomType(room_type)
        except ValueError:
            valid_types = ', '.join((t.value for t in ChatRoomType))
            raise ValidationException(message=f'Invalid room type. Must be one of: {valid_types}')
        if chat_room_type == ChatRoomType.DIRECT and members and (len(members) != 2):
            raise ValidationException(message='Direct chat rooms must have exactly 2 members')
        if chat_room_type == ChatRoomType.COMPANY and (not company_id):
            raise ValidationException(message='Company rooms must have a company_id')
        try:
            room = ChatRoom(name=name, type=chat_room_type, company_id=uuid.UUID(company_id) if company_id else None, is_active=True, metadata={})
            self.db.add(room)
            await self.db.flush()
            creator_member = ChatMember(room_id=room.id, user_id=uuid.UUID(creator_id), role=ChatMemberRole.OWNER, is_active=True)
            self.db.add(creator_member)
            if members:
                for member_data in members:
                    if member_data.get('user_id') == creator_id:
                        continue
                    member_role = member_data.get('role', ChatMemberRole.MEMBER)
                    if not isinstance(member_role, ChatMemberRole):
                        try:
                            member_role = ChatMemberRole(member_role)
                        except ValueError:
                            valid_roles = ', '.join((r.value for r in ChatMemberRole))
                            raise ValidationException(message=f'Invalid member role. Must be one of: {valid_roles}')
                    member = ChatMember(room_id=room.id, user_id=uuid.UUID(member_data['user_id']), role=member_role, is_active=True)
                    self.db.add(member)
            await self.db.commit()
            await self.db.refresh(room)
            logger.info('chat_room_created', room_id=str(room.id), room_type=room_type, creator_id=creator_id)
            return room
        except ValidationException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error('chat_room_creation_failed', error=str(e), room_type=room_type, creator_id=creator_id)
            raise BusinessLogicException(message=f'Failed to create chat room: {str(e)}') from e
    async def get_room(self, room_id: str) -> Optional[ChatRoom]:
        try:
            query = select(ChatRoom).where(ChatRoom.id == uuid.UUID(room_id))
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error('get_room_failed', error=str(e), room_id=room_id)
            raise BusinessLogicException(message=f'Failed to get chat room: {str(e)}') from e
    async def get_room_with_members(self, room_id: str) -> Optional[ChatRoom]:
        try:
            query = select(ChatRoom).options(joinedload(ChatRoom.members).joinedload(ChatMember.user)).where(ChatRoom.id == uuid.UUID(room_id))
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error('get_room_with_members_failed', error=str(e), room_id=room_id)
            raise BusinessLogicException(message=f'Failed to get chat room with members: {str(e)}') from e
    async def check_room_access(self, user_id: str, room_id: str) -> bool:
        try:
            query = select(ChatMember).where(and_(ChatMember.room_id == uuid.UUID(room_id), ChatMember.user_id == uuid.UUID(user_id), ChatMember.is_active == True))
            result = await self.db.execute(query)
            member = result.scalar_one_or_none()
            return member is not None
        except Exception as e:
            logger.error('check_room_access_failed', error=str(e), user_id=user_id, room_id=room_id)
            raise BusinessLogicException(message=f'Failed to check room access: {str(e)}') from e
    async def create_message(self, room_id: str, sender_id: str, content: str, message_type: str='text', metadata: Optional[Dict[str, Any]]=None) -> ChatMessage:
        try:
            try:
                msg_type = MessageType(message_type)
            except ValueError:
                valid_types = ', '.join((t.value for t in MessageType))
                raise ValidationException(message=f'Invalid message type. Must be one of: {valid_types}')
            message = ChatMessage(room_id=uuid.UUID(room_id), sender_id=uuid.UUID(sender_id), message_type=msg_type, metadata=metadata or {}, is_deleted=False)
            message.content = content
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            logger.info('chat_message_created', message_id=str(message.id), room_id=room_id, sender_id=sender_id, message_type=message_type)
            return message
        except ValidationException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error('chat_message_creation_failed', error=str(e), room_id=room_id, sender_id=sender_id)
            raise BusinessLogicException(message=f'Failed to create chat message: {str(e)}') from e
    async def edit_message(self, message_id: str, content: str) -> Tuple[bool, Optional[ChatMessage]]:
        try:
            query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            result = await self.db.execute(query)
            message = result.scalar_one_or_none()
            if not message:
                return (False, None)
            message.content = content
            await self.db.commit()
            await self.db.refresh(message)
            logger.info('chat_message_edited', message_id=message_id)
            return (True, message)
        except Exception as e:
            await self.db.rollback()
            logger.error('chat_message_edit_failed', error=str(e), message_id=message_id)
            raise BusinessLogicException(message=f'Failed to edit chat message: {str(e)}') from e
    async def delete_message(self, message_id: str) -> bool:
        try:
            query = update(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id)).values(is_deleted=True, deleted_at=datetime.utcnow())
            result = await self.db.execute(query)
            await self.db.commit()
            success = result.rowcount > 0
            if success:
                logger.info('chat_message_deleted', message_id=message_id)
            return success
        except Exception as e:
            await self.db.rollback()
            logger.error('chat_message_deletion_failed', error=str(e), message_id=message_id)
            raise BusinessLogicException(message=f'Failed to delete chat message: {str(e)}') from e
    async def check_message_permission(self, message_id: str, user_id: str, require_admin: bool=False) -> bool:
        try:
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
        except Exception as e:
            logger.error('check_message_permission_failed', error=str(e), message_id=message_id, user_id=user_id)
            raise BusinessLogicException(message=f'Failed to check message permissions: {str(e)}') from e
    async def get_message_history(self, room_id: str, before_id: Optional[str]=None, limit: int=50) -> List[Dict[str, Any]]:
        try:
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
        except Exception as e:
            logger.error('get_message_history_failed', error=str(e), room_id=room_id)
            raise BusinessLogicException(message=f'Failed to get message history: {str(e)}') from e
    @classmethod
    def register(cls) -> None:
        from app.services import service_registry
        service_registry.register(cls, 'chat_service')
ChatService.register()