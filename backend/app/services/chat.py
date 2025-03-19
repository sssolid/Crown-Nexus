"""
Chat service for managing chat rooms, messages, and members.

This module provides the ChatService for creating and managing chat rooms,
sending and receiving messages, and controlling member access.
"""

from __future__ import annotations
import uuid
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.cache.decorators import cached
from app.core.exceptions import (
    AuthenticationException,
    BusinessException,
    ResourceNotFoundException,
    ValidationException,
    ErrorCode,
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
    """Service for managing chat rooms and messages."""

    def __init__(self, db: AsyncSession):
        """Initialize the chat service.

        Args:
            db: Database session for database operations.
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
            name: Room name.
            room_type: Type of chat room.
            creator_id: ID of the user creating the room.
            company_id: ID of the company if this is a company room.
            members: List of member data to add to the room.

        Returns:
            The newly created chat room.

        Raises:
            ValidationException: If the room type or member data is invalid.
            BusinessException: If there's an error creating the room.
        """
        try:
            try:
                chat_room_type = ChatRoomType(room_type)
            except ValueError:
                valid_types = ", ".join((t.value for t in ChatRoomType))
                logger.warning(
                    "Invalid chat room type",
                    room_type=room_type,
                    valid_types=valid_types,
                )
                raise ValidationException(
                    message=f"Invalid room type. Must be one of: {valid_types}"
                )

            if (
                chat_room_type == ChatRoomType.DIRECT
                and members
                and (len(members) != 2)
            ):
                logger.warning(
                    "Direct chat room requires exactly 2 members",
                    members_count=len(members) if members else 0,
                )
                raise ValidationException(
                    message="Direct chat rooms must have exactly 2 members"
                )

            if chat_room_type == ChatRoomType.COMPANY and (not company_id):
                logger.warning("Company chat room missing company_id")
                raise ValidationException(
                    message="Company rooms must have a company_id",
                )

            room = ChatRoom(
                name=name,
                type=chat_room_type,
                company_id=uuid.UUID(company_id) if company_id else None,
                is_active=True,
                metadata={},
            )
            self.db.add(room)
            await self.db.flush()

            creator_member = ChatMember(
                room_id=room.id,
                user_id=uuid.UUID(creator_id),
                role=ChatMemberRole.OWNER,
                is_active=True,
            )
            self.db.add(creator_member)

            if members:
                for member_data in members:
                    if member_data.get("user_id") == creator_id:
                        continue

                    member_role = member_data.get("role", ChatMemberRole.MEMBER)
                    if not isinstance(member_role, ChatMemberRole):
                        try:
                            member_role = ChatMemberRole(member_role)
                        except ValueError:
                            valid_roles = ", ".join((r.value for r in ChatMemberRole))
                            logger.warning(
                                "Invalid member role",
                                role=member_role,
                                valid_roles=valid_roles,
                            )
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
                "Chat room created",
                room_id=str(room.id),
                room_type=room_type,
                creator_id=creator_id,
                members_count=len(members) if members else 1,
            )
            return room

        except ValidationException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Chat room creation failed",
                error=str(e),
                room_type=room_type,
                creator_id=creator_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to create chat room: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    @cached(prefix="chat:room", ttl=300, backend="redis")
    async def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """Get a chat room by ID.

        Args:
            room_id: The chat room ID.

        Returns:
            The chat room, or None if not found.

        Raises:
            BusinessException: If there's an error retrieving the room.
        """
        try:
            query = select(ChatRoom).where(ChatRoom.id == uuid.UUID(room_id))
            result = await self.db.execute(query)
            room = result.scalar_one_or_none()

            if room:
                logger.debug("Chat room retrieved", room_id=room_id)
            else:
                logger.debug("Chat room not found", room_id=room_id)

            return room
        except Exception as e:
            logger.error(
                "Error getting chat room", error=str(e), room_id=room_id, exc_info=True
            )
            raise BusinessException(
                message=f"Failed to get chat room: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def get_room_with_members(self, room_id: str) -> Optional[ChatRoom]:
        """Get a chat room with its members.

        Args:
            room_id: The chat room ID.

        Returns:
            The chat room with members loaded, or None if not found.

        Raises:
            BusinessException: If there's an error retrieving the room.
        """
        try:
            query = (
                select(ChatRoom)
                .options(joinedload(ChatRoom.members).joinedload(ChatMember.user))
                .where(ChatRoom.id == uuid.UUID(room_id))
            )

            result = await self.db.execute(query)
            room = result.scalar_one_or_none()

            if room:
                logger.debug(
                    "Chat room with members retrieved",
                    room_id=room_id,
                    members_count=len(room.members),
                )
            else:
                logger.debug("Chat room not found", room_id=room_id)

            return room
        except Exception as e:
            logger.error(
                "Error getting chat room with members",
                error=str(e),
                room_id=room_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to get chat room with members: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def check_room_access(self, user_id: str, room_id: str) -> bool:
        """Check if a user has access to a chat room.

        Args:
            user_id: The user ID.
            room_id: The chat room ID.

        Returns:
            True if the user has access, False otherwise.

        Raises:
            BusinessException: If there's an error checking access.
        """
        try:
            query = select(ChatMember).where(
                and_(
                    ChatMember.room_id == uuid.UUID(room_id),
                    ChatMember.user_id == uuid.UUID(user_id),
                    ChatMember.is_active == True,
                )
            )
            result = await self.db.execute(query)
            member = result.scalar_one_or_none()

            has_access = member is not None
            logger.debug(
                "Checked room access",
                user_id=user_id,
                room_id=room_id,
                has_access=has_access,
            )

            return has_access
        except Exception as e:
            logger.error(
                "Error checking room access",
                error=str(e),
                user_id=user_id,
                room_id=room_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to check room access: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
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
            room_id: The chat room ID.
            sender_id: The sender user ID.
            content: Message content.
            message_type: Type of message.
            metadata: Additional message metadata.

        Returns:
            The created chat message.

        Raises:
            ValidationException: If the message type is invalid.
            BusinessException: If there's an error creating the message.
        """
        try:
            try:
                msg_type = MessageType(message_type)
            except ValueError:
                valid_types = ", ".join((t.value for t in MessageType))
                logger.warning(
                    "Invalid message type",
                    message_type=message_type,
                    valid_types=valid_types,
                )
                raise ValidationException(
                    message=f"Invalid message type. Must be one of: {valid_types}"
                )

            # Check access first
            has_access = await self.check_room_access(sender_id, room_id)
            if not has_access:
                logger.warning(
                    "User doesn't have access to room",
                    user_id=sender_id,
                    room_id=room_id,
                )
                raise BusinessException(
                    message="User doesn't have access to this chat room",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"user_id": sender_id, "room_id": room_id},
                )

            message = ChatMessage(
                room_id=uuid.UUID(room_id),
                sender_id=uuid.UUID(sender_id),
                message_type=msg_type,
                metadata=metadata or {},
                is_deleted=False,
            )

            # Encrypt content if it's not already encrypted
            if not content.startswith("enc:"):
                message.content = encrypt_message(content)
            else:
                message.content = content

            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)

            logger.info(
                "Chat message created",
                message_id=str(message.id),
                room_id=room_id,
                sender_id=sender_id,
                message_type=message_type,
            )

            return message
        except (ValidationException, BusinessException):
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Chat message creation failed",
                error=str(e),
                room_id=room_id,
                sender_id=sender_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to create chat message: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def edit_message(
        self, message_id: str, content: str
    ) -> Tuple[bool, Optional[ChatMessage]]:
        """Edit a chat message.

        Args:
            message_id: The message ID.
            content: New message content.

        Returns:
            Tuple of (success, updated_message).

        Raises:
            BusinessException: If there's an error editing the message.
        """
        try:
            query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            result = await self.db.execute(query)
            message = result.scalar_one_or_none()

            if not message:
                logger.warning("Message not found for editing", message_id=message_id)
                return (False, None)

            # Encrypt content if it's not already encrypted
            if not content.startswith("enc:"):
                message.content = encrypt_message(content)
            else:
                message.content = content

            await self.db.commit()
            await self.db.refresh(message)

            logger.info("Chat message edited", message_id=message_id)
            return (True, message)
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Chat message edit failed",
                error=str(e),
                message_id=message_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to edit chat message: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def delete_message(self, message_id: str) -> bool:
        """Delete a chat message (soft delete).

        Args:
            message_id: The message ID.

        Returns:
            True if successful, False otherwise.

        Raises:
            BusinessException: If there's an error deleting the message.
        """
        try:
            query = (
                update(ChatMessage)
                .where(ChatMessage.id == uuid.UUID(message_id))
                .values(is_deleted=True, deleted_at=datetime.datetime.now(datetime.UTC))
            )

            result = await self.db.execute(query)
            await self.db.commit()

            success = result.rowcount > 0
            if success:
                logger.info("Chat message deleted", message_id=message_id)
            else:
                logger.warning("Message not found for deletion", message_id=message_id)

            return success
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Chat message deletion failed",
                error=str(e),
                message_id=message_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to delete chat message: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def check_message_permission(
        self, message_id: str, user_id: str, require_admin: bool = False
    ) -> bool:
        """Check if a user has permission to manage a message.

        Args:
            message_id: The message ID.
            user_id: The user ID.
            require_admin: Whether to require admin role.

        Returns:
            True if the user has permission, False otherwise.

        Raises:
            BusinessException: If there's an error checking permission.
        """
        try:
            # Get the message
            message_query = select(ChatMessage).where(
                ChatMessage.id == uuid.UUID(message_id)
            )
            message_result = await self.db.execute(message_query)
            message = message_result.scalar_one_or_none()

            if not message:
                logger.warning(
                    "Message not found for permission check", message_id=message_id
                )
                return False

            # Message sender always has permission
            if message.sender_id == uuid.UUID(user_id):
                logger.debug(
                    "User is message sender, permission granted",
                    user_id=user_id,
                    message_id=message_id,
                )
                return True

            # Check if admin permission is required
            if require_admin:
                member_query = select(ChatMember).where(
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

                member_result = await self.db.execute(member_query)
                member = member_result.scalar_one_or_none()

                has_permission = member is not None
                logger.debug(
                    "Admin permission check",
                    user_id=user_id,
                    message_id=message_id,
                    has_permission=has_permission,
                )

                return has_permission

            return False
        except Exception as e:
            logger.error(
                "Error checking message permission",
                error=str(e),
                message_id=message_id,
                user_id=user_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to check message permissions: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    @cached(prefix="chat:messages", ttl=60, backend="redis")
    async def get_message_history(
        self, room_id: str, before_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get chat message history for a room.

        Args:
            room_id: The chat room ID.
            before_id: Get messages before this message ID.
            limit: Maximum number of messages to return.

        Returns:
            List of formatted message dictionaries.

        Raises:
            BusinessException: If there's an error retrieving messages.
        """
        try:
            # Build the query
            if before_id:
                before_query = select(ChatMessage.created_at).where(
                    ChatMessage.id == uuid.UUID(before_id)
                )
                before_result = await self.db.execute(before_query)
                before_time = before_result.scalar_one_or_none()

                if before_time:
                    query = (
                        select(ChatMessage)
                        .where(
                            and_(
                                ChatMessage.room_id == uuid.UUID(room_id),
                                ChatMessage.created_at < before_time,
                            )
                        )
                        .order_by(desc(ChatMessage.created_at))
                        .limit(limit)
                    )
                else:
                    query = (
                        select(ChatMessage)
                        .where(ChatMessage.room_id == uuid.UUID(room_id))
                        .order_by(desc(ChatMessage.created_at))
                        .limit(limit)
                    )
            else:
                query = (
                    select(ChatMessage)
                    .where(ChatMessage.room_id == uuid.UUID(room_id))
                    .order_by(desc(ChatMessage.created_at))
                    .limit(limit)
                )

            # Execute the query
            result = await self.db.execute(query)
            messages = result.scalars().all()

            # Sort in ascending order (oldest first)
            messages = list(reversed(messages))

            logger.debug(
                "Retrieved message history",
                room_id=room_id,
                message_count=len(messages),
            )

            # Format the messages
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

                # Get message reactions
                reactions_query = select(MessageReaction).where(
                    MessageReaction.message_id == message.id
                )
                reactions_result = await self.db.execute(reactions_query)
                reactions = reactions_result.scalars().all()

                reaction_data = {}
                for reaction in reactions:
                    if reaction.reaction not in reaction_data:
                        reaction_data[reaction.reaction] = []
                    reaction_data[reaction.reaction].append(str(reaction.user_id))

                # Decrypt message content if it's encrypted
                content = message.content
                if content and content.startswith("enc:"):
                    try:
                        content = decrypt_message(content[4:])
                    except Exception as e:
                        logger.warning(
                            "Failed to decrypt message",
                            message_id=str(message.id),
                            error=str(e),
                        )
                        # Leave as is if decryption fails

                # Format the message
                formatted_messages.append(
                    {
                        "id": str(message.id),
                        "room_id": str(message.room_id),
                        "sender_id": (
                            str(message.sender_id) if message.sender_id else None
                        ),
                        "sender_name": sender_name,
                        "message_type": message.message_type,
                        "content": content,
                        "created_at": message.created_at.isoformat(),
                        "updated_at": message.updated_at.isoformat(),
                        "is_deleted": message.is_deleted,
                        "reactions": reaction_data,
                        "metadata": message.metadata,
                    }
                )

            return formatted_messages
        except Exception as e:
            logger.error(
                "Error getting message history",
                error=str(e),
                room_id=room_id,
                exc_info=True,
            )
            raise BusinessException(
                message=f"Failed to get message history: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    @classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
        from app.services import service_registry

        service_registry.register(cls, "chat_service")


# Register the service
ChatService.register()
