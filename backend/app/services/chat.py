# app/services/chat.py
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import (
    AuthenticationException,
    BusinessLogicException,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.logging import get_logger
from app.db.session import get_db_context
from app.models.chat import (
    ChatMember,
    ChatMemberRole,
    ChatMessage,
    ChatRoom,
    ChatRoomType,
    MessageReaction,
    MessageType,
)
from app.models.user import User
from app.utils.crypto import decrypt_message, encrypt_message

logger = get_logger("app.services.chat")

class ChatService:
    """Service for chat-related operations.
    
    This service handles all chat operations including:
    - Chat rooms (create, update, delete)
    - Chat messages (create, update, delete)
    - Chat members (add, remove, update roles)
    - Reactions (add, remove)
    - Reading status (mark as read, get unread count)
    """

    def __init__(self, db: AsyncSession):
        """Initialize the chat service.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def create_room(
        self,
        name: Optional[str],
        room_type: str,
        creator_id: str,
        company_id: Optional[str] = None,
        members: Optional[List[Dict[str, Any]]] = None,
    ) -> ChatRoom:
        """Create a new chat room.

        Args:
            name: Name of the chat room
            room_type: Type of chat room (direct, group, company)
            creator_id: ID of the user creating the room
            company_id: Optional company ID for company rooms
            members: Optional list of members to add (with user_id and role)

        Returns:
            The newly created chat room

        Raises:
            ValidationException: If room parameters are invalid
        """
        # Validate room type
        try:
            chat_room_type = ChatRoomType(room_type)
        except ValueError:
            valid_types = ", ".join(t.value for t in ChatRoomType)
            raise ValidationException(
                message=f"Invalid room type. Must be one of: {valid_types}"
            )

        # Validate room parameters
        if chat_room_type == ChatRoomType.DIRECT and members and len(members) != 2:
            raise ValidationException(
                message="Direct chat rooms must have exactly 2 members"
            )

        if chat_room_type == ChatRoomType.COMPANY and not company_id:
            raise ValidationException(
                message="Company rooms must have a company_id"
            )

        try:
            # Create the room
            room = ChatRoom(
                name=name,
                type=chat_room_type,
                company_id=uuid.UUID(company_id) if company_id else None,
                is_active=True,
                metadata={},
            )
            self.db.add(room)
            await self.db.flush()

            # Add the creator as the owner
            creator_member = ChatMember(
                room_id=room.id,
                user_id=uuid.UUID(creator_id),
                role=ChatMemberRole.OWNER,
                is_active=True,
            )
            self.db.add(creator_member)

            # Add other members if provided
            if members:
                for member_data in members:
                    if member_data.get("user_id") == creator_id:
                        continue
                    
                    # Validate member role
                    member_role = member_data.get("role", ChatMemberRole.MEMBER)
                    if not isinstance(member_role, ChatMemberRole):
                        try:
                            member_role = ChatMemberRole(member_role)
                        except ValueError:
                            valid_roles = ", ".join(r.value for r in ChatMemberRole)
                            raise ValidationException(
                                message=f"Invalid member role. Must be one of: {valid_roles}"
                            )
                    
                    member = ChatMember(
                        room_id=room.id,
                        user_id=uuid.UUID(member_data["user_id"]),
                        role=member_role,
                        is_active=True,
                    )
                    self.db.add(member)

            await self.db.commit()
            await self.db.refresh(room)
            
            logger.info(
                "chat_room_created",
                room_id=str(room.id),
                room_type=room_type,
                creator_id=creator_id,
            )
            
            return room
        except ValidationException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "chat_room_creation_failed",
                error=str(e),
                room_type=room_type,
                creator_id=creator_id,
            )
            raise BusinessLogicException(
                message=f"Failed to create chat room: {str(e)}"
            ) from e

    async def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """Get a chat room by ID.

        Args:
            room_id: ID of the chat room

        Returns:
            The chat room if found, None otherwise
        """
        try:
            query = select(ChatRoom).where(ChatRoom.id == uuid.UUID(room_id))
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(
                "get_room_failed",
                error=str(e),
                room_id=room_id,
            )
            raise BusinessLogicException(
                message=f"Failed to get chat room: {str(e)}"
            ) from e

    async def get_room_with_members(self, room_id: str) -> Optional[ChatRoom]:
        """Get a chat room with its members.

        Args:
            room_id: ID of the chat room

        Returns:
            The chat room with members if found, None otherwise
        """
        try:
            query = (
                select(ChatRoom)
                .options(
                    joinedload(ChatRoom.members)
                    .joinedload(ChatMember.user)
                )
                .where(ChatRoom.id == uuid.UUID(room_id))
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(
                "get_room_with_members_failed",
                error=str(e),
                room_id=room_id,
            )
            raise BusinessLogicException(
                message=f"Failed to get chat room with members: {str(e)}"
            ) from e

    async def check_room_access(self, user_id: str, room_id: str) -> bool:
        """Check if a user has access to a room.

        Args:
            user_id: ID of the user
            room_id: ID of the room

        Returns:
            True if the user has access, False otherwise
        """
        try:
            query = (
                select(ChatMember)
                .where(
                    and_(
                        ChatMember.room_id == uuid.UUID(room_id),
                        ChatMember.user_id == uuid.UUID(user_id),
                        ChatMember.is_active == True,
                    )
                )
            )
            result = await self.db.execute(query)
            member = result.scalar_one_or_none()
            return member is not None
        except Exception as e:
            logger.error(
                "check_room_access_failed",
                error=str(e),
                user_id=user_id,
                room_id=room_id,
            )
            raise BusinessLogicException(
                message=f"Failed to check room access: {str(e)}"
            ) from e

    async def create_message(
        self,
        room_id: str,
        sender_id: str,
        content: str,
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatMessage:
        """Create a new chat message.

        Args:
            room_id: ID of the chat room
            sender_id: ID of the message sender
            content: Message content
            message_type: Type of message (text, image, file, etc.)
            metadata: Additional metadata for the message

        Returns:
            The created message

        Raises:
            ValidationException: If message parameters are invalid
            BusinessLogicException: If message creation fails
        """
        try:
            # Validate message type
            try:
                msg_type = MessageType(message_type)
            except ValueError:
                valid_types = ", ".join(t.value for t in MessageType)
                raise ValidationException(
                    message=f"Invalid message type. Must be one of: {valid_types}"
                )
            
            # Create the message
            message = ChatMessage(
                room_id=uuid.UUID(room_id),
                sender_id=uuid.UUID(sender_id),
                message_type=msg_type,
                metadata=metadata or {},
                is_deleted=False,
            )
            message.content = content  # Using the property setter to encrypt
            
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            
            logger.info(
                "chat_message_created",
                message_id=str(message.id),
                room_id=room_id,
                sender_id=sender_id,
                message_type=message_type,
            )
            
            return message
        except ValidationException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "chat_message_creation_failed",
                error=str(e),
                room_id=room_id,
                sender_id=sender_id,
            )
            raise BusinessLogicException(
                message=f"Failed to create chat message: {str(e)}"
            ) from e

    async def edit_message(
        self,
        message_id: str,
        content: str,
    ) -> Tuple[bool, Optional[ChatMessage]]:
        """Edit an existing chat message.

        Args:
            message_id: ID of the message to edit
            content: New content for the message

        Returns:
            Tuple of (success, updated message or None)

        Raises:
            BusinessLogicException: If message editing fails
        """
        try:
            query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            result = await self.db.execute(query)
            message = result.scalar_one_or_none()
            
            if not message:
                return (False, None)
            
            message.content = content  # Using the property setter to encrypt
            await self.db.commit()
            await self.db.refresh(message)
            
            logger.info(
                "chat_message_edited",
                message_id=message_id,
            )
            
            return (True, message)
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "chat_message_edit_failed",
                error=str(e),
                message_id=message_id,
            )
            raise BusinessLogicException(
                message=f"Failed to edit chat message: {str(e)}"
            ) from e

    async def delete_message(self, message_id: str) -> bool:
        """Delete a chat message.

        Args:
            message_id: ID of the message to delete

        Returns:
            True if successful, False otherwise

        Raises:
            BusinessLogicException: If message deletion fails
        """
        try:
            query = (
                update(ChatMessage)
                .where(ChatMessage.id == uuid.UUID(message_id))
                .values(
                    is_deleted=True,
                    deleted_at=datetime.utcnow(),
                )
            )
            result = await self.db.execute(query)
            await self.db.commit()
            
            success = result.rowcount > 0
            if success:
                logger.info(
                    "chat_message_deleted",
                    message_id=message_id,
                )
            
            return success
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "chat_message_deletion_failed",
                error=str(e),
                message_id=message_id,
            )
            raise BusinessLogicException(
                message=f"Failed to delete chat message: {str(e)}"
            ) from e

    async def check_message_permission(
        self,
        message_id: str,
        user_id: str,
        require_admin: bool = False,
    ) -> bool:
        """Check if a user has permission to modify a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user
            require_admin: Whether to require admin permissions

        Returns:
            True if the user has permission, False otherwise
        """
        try:
            message_query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            message_result = await self.db.execute(message_query)
            message = message_result.scalar_one_or_none()
            
            if not message:
                return False
            
            # Users can always modify their own messages
            if message.sender_id == uuid.UUID(user_id):
                return True
            
            # If admin rights are required, check if the user is an admin
            if require_admin:
                member_query = (
                    select(ChatMember)
                    .where(
                        and_(
                            ChatMember.room_id == message.room_id,
                            ChatMember.user_id == uuid.UUID(user_id),
                            ChatMember.is_active == True,
                            or_(
                                ChatMember.role == ChatMemberRole.ADMIN,
                                ChatMember.role == ChatMemberRole.OWNER,
                            ),
                        )
                    )
                )
                member_result = await self.db.execute(member_query)
                member = member_result.scalar_one_or_none()
                return member is not None
            
            return False
        except Exception as e:
            logger.error(
                "check_message_permission_failed",
                error=str(e),
                message_id=message_id,
                user_id=user_id,
            )
            raise BusinessLogicException(
                message=f"Failed to check message permissions: {str(e)}"
            ) from e

    # Additional methods would be implemented similarly
    # ...

    async def get_message_history(
        self, 
        room_id: str, 
        before_id: Optional[str] = None, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get message history for a room.

        Args:
            room_id: ID of the room
            before_id: Get messages before this ID (for pagination)
            limit: Maximum number of messages to return

        Returns:
            List of message data dictionaries

        Raises:
            BusinessLogicException: If retrieving message history fails
        """
        try:
            # Build the query based on parameters
            if before_id:
                before_query = select(ChatMessage.created_at).where(
                    ChatMessage.id == uuid.UUID(before_id)
                )
                before_result = await self.db.execute(before_query)
                before_time = before_result.scalar_one_or_none()
                
                if before_time:
                    query = select(ChatMessage).where(
                        and_(
                            ChatMessage.room_id == uuid.UUID(room_id),
                            ChatMessage.created_at < before_time
                        )
                    ).order_by(desc(ChatMessage.created_at)).limit(limit)
                else:
                    query = select(ChatMessage).where(
                        ChatMessage.room_id == uuid.UUID(room_id)
                    ).order_by(desc(ChatMessage.created_at)).limit(limit)
            else:
                query = select(ChatMessage).where(
                    ChatMessage.room_id == uuid.UUID(room_id)
                ).order_by(desc(ChatMessage.created_at)).limit(limit)
            
            # Execute the query
            result = await self.db.execute(query)
            messages = result.scalars().all()
            
            # Reverse to get chronological order
            messages = list(reversed(messages))
            
            # Format messages with additional data
            formatted_messages = []
            for message in messages:
                # Get sender name
                sender_name = None
                if message.sender_id:
                    sender_query = select(User.full_name).where(
                        User.id == message.sender_id
                    )
                    sender_result = await self.db.execute(sender_query)
                    sender_name = sender_result.scalar_one_or_none()
                
                # Get reactions
                reactions_query = select(MessageReaction).where(
                    MessageReaction.message_id == message.id
                )
                reactions_result = await self.db.execute(reactions_query)
                reactions = reactions_result.scalars().all()
                
                # Format reactions
                reaction_data = {}
                for reaction in reactions:
                    if reaction.reaction not in reaction_data:
                        reaction_data[reaction.reaction] = []
                    reaction_data[reaction.reaction].append(str(reaction.user_id))
                
                # Format message
                formatted_messages.append({
                    'id': str(message.id),
                    'room_id': str(message.room_id),
                    'sender_id': str(message.sender_id) if message.sender_id else None,
                    'sender_name': sender_name,
                    'message_type': message.message_type,
                    'content': message.content,
                    'created_at': message.created_at.isoformat(),
                    'updated_at': message.updated_at.isoformat(),
                    'is_deleted': message.is_deleted,
                    'reactions': reaction_data,
                    'metadata': message.metadata
                })
            
            return formatted_messages
        except Exception as e:
            logger.error(
                "get_message_history_failed",
                error=str(e),
                room_id=room_id,
            )
            raise BusinessLogicException(
                message=f"Failed to get message history: {str(e)}"
            ) from e

    # Register the service with the service registry
    @classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
        from app.services import service_registry
        service_registry.register(cls, "chat_service")


# Register the service when this module is imported
ChatService.register()
