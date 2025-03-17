# backend/app/chat/service.py
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import (
    AuthenticationException,
    BusinessLogicException,
    DatabaseException,
    ErrorCode,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.permissions import PermissionChecker
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
    """
    Service for managing chat functionality including rooms, messages, and reactions.

    This service handles all operations related to chat, including:
    - Creating and managing chat rooms
    - Sending and retrieving messages
    - User permissions within chat rooms
    - Message reactions
    - Read status tracking
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the ChatService.

        Args:
            db: Database session for database operations
        """
        self.db = db

    async def create_room(
        self,
        name: Optional[str],
        room_type: ChatRoomType,
        creator_id: str,
        company_id: Optional[str] = None,
        members: Optional[List[Dict[str, Any]]] = None,
    ) -> ChatRoom:
        """
        Create a new chat room.

        Args:
            name: Optional name for the chat room
            room_type: Type of chat room (DIRECT, GROUP, COMPANY, SUPPORT)
            creator_id: User ID of the room creator
            company_id: Optional company ID for company rooms
            members: Optional list of initial members for the room

        Returns:
            The newly created ChatRoom instance

        Raises:
            ValidationException: If the input data is invalid
            DatabaseException: If a database error occurs
            BusinessLogicException: If there's a logical error creating the room
        """
        logger.info(
            "Creating chat room",
            room_type=room_type,
            creator_id=creator_id,
            company_id=company_id,
        )

        # Validate room type
        if not isinstance(room_type, ChatRoomType):
            try:
                room_type = ChatRoomType(room_type)
            except ValueError:
                valid_types = ", ".join(t.value for t in ChatRoomType)
                raise ValidationException(
                    message=f"Invalid room type. Must be one of: {valid_types}",
                    code=ErrorCode.VALIDATION_ERROR,
                )

        # Validate direct message requirements
        if room_type == ChatRoomType.DIRECT and members and (len(members) != 2):
            raise ValidationException(
                message="Direct chat rooms must have exactly 2 members",
                code=ErrorCode.VALIDATION_ERROR,
            )

        # Validate company room requirements
        if room_type == ChatRoomType.COMPANY and not company_id:
            raise ValidationException(
                message="Company rooms must have a company_id",
                code=ErrorCode.VALIDATION_ERROR,
            )

        try:
            # Create room
            room = ChatRoom(
                name=name,
                type=room_type,
                company_id=uuid.UUID(company_id) if company_id else None,
                is_active=True,
                metadata={},
            )
            self.db.add(room)
            await self.db.flush()

            # Add creator as a member
            creator_member = ChatMember(
                room_id=room.id,
                user_id=uuid.UUID(creator_id),
                role=ChatMemberRole.OWNER,
                is_active=True,
            )
            self.db.add(creator_member)

            # Add other members if any
            if members:
                for member_data in members:
                    if member_data.get("user_id") == creator_id:
                        continue

                    member_role = member_data.get("role", ChatMemberRole.MEMBER)
                    if not isinstance(member_role, ChatMemberRole):
                        try:
                            member_role = ChatMemberRole(member_role)
                        except ValueError:
                            valid_roles = ", ".join(r.value for r in ChatMemberRole)
                            raise ValidationException(
                                message=f"Invalid member role. Must be one of: {valid_roles}",
                                code=ErrorCode.VALIDATION_ERROR,
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
            )
            return room

        except ValidationException:
            await self.db.rollback()
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error creating chat room",
                error=str(e),
                room_type=room_type,
                creator_id=creator_id,
            )
            raise DatabaseException(
                message=f"Failed to create chat room due to database error: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Unexpected error creating chat room",
                error=str(e),
                room_type=room_type,
                creator_id=creator_id,
            )
            raise BusinessLogicException(
                message=f"Failed to create chat room: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """
        Get a chat room by ID.

        Args:
            room_id: The ID of the room to retrieve

        Returns:
            The ChatRoom instance if found, None otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug("Getting chat room", room_id=room_id)
        try:
            query = select(ChatRoom).where(ChatRoom.id == uuid.UUID(room_id))
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error("Database error getting chat room", error=str(e), room_id=room_id)
            raise DatabaseException(
                message=f"Failed to get chat room: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def get_room_with_members(self, room_id: str) -> Optional[ChatRoom]:
        """
        Get a chat room by ID with its members loaded.

        Args:
            room_id: The ID of the room to retrieve

        Returns:
            The ChatRoom instance with members if found, None otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug("Getting chat room with members", room_id=room_id)
        try:
            query = (
                select(ChatRoom)
                .options(joinedload(ChatRoom.members).joinedload(ChatMember.user))
                .where(ChatRoom.id == uuid.UUID(room_id))
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(
                "Database error getting chat room with members",
                error=str(e),
                room_id=room_id,
            )
            raise DatabaseException(
                message=f"Failed to get chat room with members: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def get_user_rooms(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all chat rooms for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of chat room data dictionaries with metadata

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug("Getting user rooms", user_id=user_id)
        try:
            query = (
                select(ChatRoom, ChatMember)
                .join(ChatMember, ChatRoom.id == ChatMember.room_id)
                .where(
                    and_(
                        ChatMember.user_id == uuid.UUID(user_id),
                        ChatMember.is_active == True,
                        ChatRoom.is_active == True,
                        )
                )
            )
            result = await self.db.execute(query)

            user_rooms = []
            for room, member in result:
                # Get last message
                last_message_query = (
                    select(ChatMessage)
                    .where(ChatMessage.room_id == room.id)
                    .order_by(desc(ChatMessage.created_at))
                    .limit(1)
                )
                last_message_result = await self.db.execute(last_message_query)
                last_message = last_message_result.scalar_one_or_none()

                # Get unread count
                unread_count = await self.get_unread_count(
                    str(room.id), user_id, member.last_read_at
                )

                # Get member count
                member_count_query = (
                    select(func.count())
                    .select_from(ChatMember)
                    .where(
                        and_(
                            ChatMember.room_id == room.id,
                            ChatMember.is_active == True,
                            )
                    )
                )
                member_count_result = await self.db.execute(member_count_query)
                member_count = member_count_result.scalar() or 0

                # Prepare room data
                room_data = {
                    "id": str(room.id),
                    "name": room.name,
                    "type": room.type,
                    "created_at": room.created_at.isoformat(),
                    "member_count": member_count,
                    "user_role": member.role,
                    "unread_count": unread_count,
                    "last_message": None,
                }

                # Add last message if any
                if last_message:
                    sender_query = select(User).where(User.id == last_message.sender_id)
                    sender_result = await self.db.execute(sender_query)
                    sender = sender_result.scalar_one_or_none()

                    room_data["last_message"] = {
                        "id": str(last_message.id),
                        "sender_id": str(last_message.sender_id) if last_message.sender_id else None,
                        "sender_name": sender.full_name if sender else None,
                        "content": last_message.content,
                        "message_type": last_message.message_type,
                        "created_at": last_message.created_at.isoformat(),
                        "is_deleted": last_message.is_deleted,
                    }

                user_rooms.append(room_data)

            return user_rooms

        except SQLAlchemyError as e:
            logger.error(
                "Database error getting user rooms",
                error=str(e),
                user_id=user_id
            )
            raise DatabaseException(
                message=f"Failed to get user chat rooms: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def get_room_info(self, room_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a chat room.

        Args:
            room_id: The ID of the room

        Returns:
            Dictionary with room information and members

        Raises:
            ResourceNotFoundException: If the room doesn't exist
            DatabaseException: If a database error occurs
        """
        logger.debug("Getting room info", room_id=room_id)
        try:
            room = await self.get_room_with_members(room_id)
            if not room:
                logger.warning("Chat room not found", room_id=room_id)
                raise ResourceNotFoundException(
                    message=f"Chat room with ID {room_id} not found",
                    code=ErrorCode.RESOURCE_NOT_FOUND,
                )

            # Format members data
            members = []
            for member in room.members:
                if member.is_active:
                    members.append({
                        "user_id": str(member.user_id),
                        "user_name": member.user.full_name if member.user else "Unknown",
                        "role": member.role,
                        "last_read_at": member.last_read_at.isoformat() if member.last_read_at else None,
                    })

            # Get last message
            last_message_query = (
                select(ChatMessage)
                .where(ChatMessage.room_id == room.id)
                .order_by(desc(ChatMessage.created_at))
                .limit(1)
            )
            last_message_result = await self.db.execute(last_message_query)
            last_message = last_message_result.scalar_one_or_none()

            # Prepare room data
            room_data = {
                "id": str(room.id),
                "name": room.name,
                "type": room.type,
                "created_at": room.created_at.isoformat(),
                "member_count": len(members),
                "members": members,
                "company_id": str(room.company_id) if room.company_id else None,
                "metadata": room.metadata,
                "last_message": None,
            }

            # Add last message if any
            if last_message:
                sender_query = select(User).where(User.id == last_message.sender_id)
                sender_result = await self.db.execute(sender_query)
                sender = sender_result.scalar_one_or_none()

                room_data["last_message"] = {
                    "id": str(last_message.id),
                    "sender_id": str(last_message.sender_id) if last_message.sender_id else None,
                    "sender_name": sender.full_name if sender else None,
                    "content": last_message.content,
                    "message_type": last_message.message_type,
                    "created_at": last_message.created_at.isoformat(),
                    "is_deleted": last_message.is_deleted,
                }

            return room_data

        except ResourceNotFoundException:
            raise
        except SQLAlchemyError as e:
            logger.error(
                "Database error getting room info",
                error=str(e),
                room_id=room_id
            )
            raise DatabaseException(
                message=f"Failed to get chat room info: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def check_room_access(self, user_id: str, room_id: str) -> bool:
        """
        Check if a user has access to a chat room.

        Args:
            user_id: ID of the user
            room_id: ID of the room

        Returns:
            True if the user has access, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug("Checking room access", user_id=user_id, room_id=room_id)
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
            return member is not None
        except SQLAlchemyError as e:
            logger.error(
                "Database error checking room access",
                error=str(e),
                user_id=user_id,
                room_id=room_id,
            )
            raise DatabaseException(
                message=f"Failed to check room access: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
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
        """
        Create a new message in a chat room.

        Args:
            room_id: ID of the chat room
            sender_id: ID of the message sender
            content: Message content
            message_type: Type of message (default: "text")
            metadata: Optional metadata for the message

        Returns:
            The created ChatMessage instance

        Raises:
            ValidationException: If the input data is invalid
            DatabaseException: If a database error occurs
            BusinessLogicException: If there's a logical error creating the message
        """
        logger.info(
            "Creating chat message",
            room_id=room_id,
            sender_id=sender_id,
            message_type=message_type,
        )

        # Validate message type
        try:
            msg_type = MessageType(message_type)
        except ValueError:
            valid_types = ", ".join(t.value for t in MessageType)
            raise ValidationException(
                message=f"Invalid message type. Must be one of: {valid_types}",
                code=ErrorCode.VALIDATION_ERROR,
            )

        try:
            # Create message with encrypted content
            message = ChatMessage(
                room_id=uuid.UUID(room_id),
                sender_id=uuid.UUID(sender_id),
                message_type=msg_type,
                metadata=metadata or {},
                is_deleted=False,
            )
            message.content = content  # This uses the property setter which encrypts content

            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)

            logger.info(
                "Chat message created",
                message_id=str(message.id),
                room_id=room_id,
                sender_id=sender_id,
            )
            return message

        except ValidationException:
            await self.db.rollback()
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error creating chat message",
                error=str(e),
                room_id=room_id,
                sender_id=sender_id,
            )
            raise DatabaseException(
                message=f"Failed to create chat message: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Unexpected error creating chat message",
                error=str(e),
                room_id=room_id,
                sender_id=sender_id,
            )
            raise BusinessLogicException(
                message=f"Failed to create chat message: {str(e)}",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
                original_exception=e,
            ) from e

    async def edit_message(self, message_id: str, content: str) -> Tuple[bool, Optional[ChatMessage]]:
        """
        Edit an existing message.

        Args:
            message_id: ID of the message to edit
            content: New content for the message

        Returns:
            Tuple of (success status, updated message if successful)

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.info("Editing chat message", message_id=message_id)
        try:
            query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            result = await self.db.execute(query)
            message = result.scalar_one_or_none()

            if not message:
                logger.warning("Message not found for editing", message_id=message_id)
                return (False, None)

            message.content = content  # This uses the property setter which encrypts
            await self.db.commit()
            await self.db.refresh(message)

            logger.info("Chat message edited", message_id=message_id)
            return (True, message)

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error editing chat message",
                error=str(e),
                message_id=message_id,
            )
            raise DatabaseException(
                message=f"Failed to edit chat message: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def delete_message(self, message_id: str) -> bool:
        """
        Soft delete a message.

        Args:
            message_id: ID of the message to delete

        Returns:
            True if the operation was successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.info("Deleting chat message", message_id=message_id)
        try:
            query = (
                update(ChatMessage)
                .where(ChatMessage.id == uuid.UUID(message_id))
                .values(is_deleted=True, deleted_at=datetime.utcnow())
            )
            result = await self.db.execute(query)
            await self.db.commit()

            success = result.rowcount > 0
            if success:
                logger.info("Chat message deleted", message_id=message_id)
            else:
                logger.warning("Message not found for deletion", message_id=message_id)

            return success

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error deleting chat message",
                error=str(e),
                message_id=message_id,
            )
            raise DatabaseException(
                message=f"Failed to delete chat message: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def check_message_permission(
        self, message_id: str, user_id: str, require_admin: bool = False
    ) -> bool:
        """
        Check if a user has permission to modify a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user
            require_admin: Whether to require admin privileges

        Returns:
            True if the user has permission, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Checking message permission",
            message_id=message_id,
            user_id=user_id,
            require_admin=require_admin,
        )
        try:
            # First get the message
            message_query = select(ChatMessage).where(ChatMessage.id == uuid.UUID(message_id))
            message_result = await self.db.execute(message_query)
            message = message_result.scalar_one_or_none()

            if not message:
                logger.warning("Message not found for permission check", message_id=message_id)
                return False

            # Own messages can always be modified
            if message.sender_id == uuid.UUID(user_id):
                return True

            # If admin permissions are required, check member role
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
                return member is not None

            return False

        except SQLAlchemyError as e:
            logger.error(
                "Database error checking message permission",
                error=str(e),
                message_id=message_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to check message permissions: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def mark_as_read(self, user_id: str, room_id: str, last_read_id: str) -> bool:
        """
        Mark messages in a room as read up to a specific message.

        Args:
            user_id: ID of the user
            room_id: ID of the chat room
            last_read_id: ID of the last read message

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Marking messages as read",
            user_id=user_id,
            room_id=room_id,
            last_read_id=last_read_id,
        )
        try:
            # First get the message's timestamp
            message_query = select(ChatMessage).where(
                and_(
                    ChatMessage.id == uuid.UUID(last_read_id),
                    ChatMessage.room_id == uuid.UUID(room_id),
                    )
            )
            message_result = await self.db.execute(message_query)
            message = message_result.scalar_one_or_none()

            if not message:
                logger.warning(
                    "Message not found for marking as read",
                    last_read_id=last_read_id,
                    room_id=room_id,
                )
                return False

            # Update the member's last_read_at timestamp
            member_query = (
                update(ChatMember)
                .where(
                    and_(
                        ChatMember.room_id == uuid.UUID(room_id),
                        ChatMember.user_id == uuid.UUID(user_id),
                        )
                )
                .values(last_read_at=message.created_at)
            )
            result = await self.db.execute(member_query)
            await self.db.commit()

            success = result.rowcount > 0
            if success:
                logger.debug(
                    "Messages marked as read",
                    user_id=user_id,
                    room_id=room_id,
                    last_read_id=last_read_id,
                )
            else:
                logger.warning(
                    "Failed to mark messages as read - member not found",
                    user_id=user_id,
                    room_id=room_id,
                )

            return success

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error marking messages as read",
                error=str(e),
                user_id=user_id,
                room_id=room_id,
            )
            raise DatabaseException(
                message=f"Failed to mark messages as read: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def get_unread_count(
        self, room_id: str, user_id: str, last_read_at: Optional[datetime] = None
    ) -> int:
        """
        Get count of unread messages for a user in a room.

        Args:
            room_id: ID of the chat room
            user_id: ID of the user
            last_read_at: Optional timestamp of last read message

        Returns:
            Count of unread messages

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Getting unread message count",
            user_id=user_id,
            room_id=room_id,
        )
        try:
            # If last_read_at not provided, get it from the member record
            if not last_read_at:
                member_query = select(ChatMember.last_read_at).where(
                    and_(
                        ChatMember.room_id == uuid.UUID(room_id),
                        ChatMember.user_id == uuid.UUID(user_id),
                        )
                )
                member_result = await self.db.execute(member_query)
                member_last_read = member_result.scalar_one_or_none()

                if not member_last_read:
                    # If no last read time, count all messages not from user
                    count_query = (
                        select(func.count())
                        .select_from(ChatMessage)
                        .where(
                            and_(
                                ChatMessage.room_id == uuid.UUID(room_id),
                                ChatMessage.sender_id != uuid.UUID(user_id),
                                )
                        )
                    )
                else:
                    # Count messages after last read time and not from user
                    count_query = (
                        select(func.count())
                        .select_from(ChatMessage)
                        .where(
                            and_(
                                ChatMessage.room_id == uuid.UUID(room_id),
                                ChatMessage.created_at > member_last_read,
                                ChatMessage.sender_id != uuid.UUID(user_id),
                                )
                        )
                    )
            else:
                # Count messages after provided last read time and not from user
                count_query = (
                    select(func.count())
                    .select_from(ChatMessage)
                    .where(
                        and_(
                            ChatMessage.room_id == uuid.UUID(room_id),
                            ChatMessage.created_at > last_read_at,
                            ChatMessage.sender_id != uuid.UUID(user_id),
                            )
                    )
                )

            # Execute the query
            count_result = await self.db.execute(count_query)
            return count_result.scalar() or 0

        except SQLAlchemyError as e:
            logger.error(
                "Database error getting unread count",
                error=str(e),
                user_id=user_id,
                room_id=room_id,
            )
            raise DatabaseException(
                message=f"Failed to get unread message count: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def get_message_history(
        self, room_id: str, before_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get message history for a chat room.

        Args:
            room_id: ID of the chat room
            before_id: Optional ID of message to get history before
            limit: Maximum number of messages to return

        Returns:
            List of formatted message dictionaries

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Getting message history",
            room_id=room_id,
            before_id=before_id,
            limit=limit,
        )
        try:
            if before_id:
                # If before_id provided, get message timestamp first
                before_query = select(ChatMessage.created_at).where(
                    ChatMessage.id == uuid.UUID(before_id)
                )
                before_result = await self.db.execute(before_query)
                before_time = before_result.scalar_one_or_none()

                if before_time:
                    # Get messages before this time
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
                    # If before_id doesn't exist, get latest messages
                    query = (
                        select(ChatMessage)
                        .where(ChatMessage.room_id == uuid.UUID(room_id))
                        .order_by(desc(ChatMessage.created_at))
                        .limit(limit)
                    )
            else:
                # Get latest messages
                query = (
                    select(ChatMessage)
                    .where(ChatMessage.room_id == uuid.UUID(room_id))
                    .order_by(desc(ChatMessage.created_at))
                    .limit(limit)
                )

            # Execute the query
            result = await self.db.execute(query)
            messages = result.scalars().all()

            # Reverse to get chronological order
            messages = list(reversed(messages))

            # Format messages
            formatted_messages = []
            for message in messages:
                # Get sender name
                sender_name = None
                if message.sender_id:
                    sender_query = select(User.full_name).where(User.id == message.sender_id)
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
                    "id": str(message.id),
                    "room_id": str(message.room_id),
                    "sender_id": str(message.sender_id) if message.sender_id else None,
                    "sender_name": sender_name,
                    "message_type": message.message_type,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                    "updated_at": message.updated_at.isoformat(),
                    "is_deleted": message.is_deleted,
                    "reactions": reaction_data,
                    "metadata": message.metadata,
                })

            return formatted_messages

        except SQLAlchemyError as e:
            logger.error(
                "Database error getting message history",
                error=str(e),
                room_id=room_id,
            )
            raise DatabaseException(
                message=f"Failed to get message history: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def add_reaction(self, message_id: str, user_id: str, reaction: str) -> bool:
        """
        Add a reaction to a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user adding the reaction
            reaction: Reaction string/emoji

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Adding message reaction",
            message_id=message_id,
            user_id=user_id,
            reaction=reaction,
        )
        try:
            # Check if reaction already exists
            query = select(MessageReaction).where(
                and_(
                    MessageReaction.message_id == uuid.UUID(message_id),
                    MessageReaction.user_id == uuid.UUID(user_id),
                    MessageReaction.reaction == reaction,
                    )
            )
            result = await self.db.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                logger.debug(
                    "Reaction already exists",
                    message_id=message_id,
                    user_id=user_id,
                    reaction=reaction,
                )
                return True

            # Create new reaction
            message_reaction = MessageReaction(
                message_id=uuid.UUID(message_id),
                user_id=uuid.UUID(user_id),
                reaction=reaction,
            )
            self.db.add(message_reaction)

            try:
                await self.db.commit()
                logger.info(
                    "Message reaction added",
                    message_id=message_id,
                    user_id=user_id,
                    reaction=reaction,
                )
                return True
            except Exception as e:
                await self.db.rollback()
                logger.error(
                    "Error adding reaction",
                    error=str(e),
                    message_id=message_id,
                    user_id=user_id,
                )
                return False

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error adding message reaction",
                error=str(e),
                message_id=message_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to add message reaction: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def remove_reaction(self, message_id: str, user_id: str, reaction: str) -> bool:
        """
        Remove a reaction from a message.

        Args:
            message_id: ID of the message
            user_id: ID of the user removing the reaction
            reaction: Reaction string/emoji

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Removing message reaction",
            message_id=message_id,
            user_id=user_id,
            reaction=reaction,
        )
        try:
            # Find the reaction
            query = select(MessageReaction).where(
                and_(
                    MessageReaction.message_id == uuid.UUID(message_id),
                    MessageReaction.user_id == uuid.UUID(user_id),
                    MessageReaction.reaction == reaction,
                    )
            )
            result = await self.db.execute(query)
            reaction_obj = result.scalar_one_or_none()

            if not reaction_obj:
                logger.warning(
                    "Reaction not found for removal",
                    message_id=message_id,
                    user_id=user_id,
                    reaction=reaction,
                )
                return False

            # Delete the reaction
            await self.db.delete(reaction_obj)

            try:
                await self.db.commit()
                logger.info(
                    "Message reaction removed",
                    message_id=message_id,
                    user_id=user_id,
                    reaction=reaction,
                )
                return True
            except Exception as e:
                await self.db.rollback()
                logger.error(
                    "Error removing reaction",
                    error=str(e),
                    message_id=message_id,
                    user_id=user_id,
                )
                return False

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error removing message reaction",
                error=str(e),
                message_id=message_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to remove message reaction: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def add_member(
        self, room_id: str, user_id: str, role: ChatMemberRole = ChatMemberRole.MEMBER
    ) -> bool:
        """
        Add a member to a chat room.

        Args:
            room_id: ID of the chat room
            user_id: ID of the user to add
            role: Role of the user in the room

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.info(
            "Adding chat room member",
            room_id=room_id,
            user_id=user_id,
            role=role,
        )
        try:
            # Check if member already exists
            query = select(ChatMember).where(
                and_(
                    ChatMember.room_id == uuid.UUID(room_id),
                    ChatMember.user_id == uuid.UUID(user_id),
                    )
            )
            result = await self.db.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                # If member exists but inactive, reactivate
                if not existing.is_active:
                    existing.is_active = True
                    existing.role = role
                    await self.db.commit()
                    logger.info(
                        "Reactivated existing chat room member",
                        room_id=room_id,
                        user_id=user_id,
                    )
                return True

            # Add new member
            member = ChatMember(
                room_id=uuid.UUID(room_id),
                user_id=uuid.UUID(user_id),
                role=role,
                is_active=True,
            )
            self.db.add(member)

            try:
                await self.db.commit()
                logger.info(
                    "Chat room member added",
                    room_id=room_id,
                    user_id=user_id,
                    role=role,
                )
                return True
            except Exception as e:
                await self.db.rollback()
                logger.error(
                    "Error adding member",
                    error=str(e),
                    room_id=room_id,
                    user_id=user_id,
                )
                return False

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error adding chat room member",
                error=str(e),
                room_id=room_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to add chat room member: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def remove_member(self, room_id: str, user_id: str) -> bool:
        """
        Remove a member from a chat room.

        Args:
            room_id: ID of the chat room
            user_id: ID of the user to remove

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.info(
            "Removing chat room member",
            room_id=room_id,
            user_id=user_id,
        )
        try:
            # Find the member
            query = select(ChatMember).where(
                and_(
                    ChatMember.room_id == uuid.UUID(room_id),
                    ChatMember.user_id == uuid.UUID(user_id),
                    ChatMember.is_active == True,
                    )
            )
            result = await self.db.execute(query)
            member = result.scalar_one_or_none()

            if not member:
                logger.warning(
                    "Member not found for removal",
                    room_id=room_id,
                    user_id=user_id,
                )
                return False

            # Soft delete by marking inactive
            member.is_active = False

            try:
                await self.db.commit()
                logger.info(
                    "Chat room member removed",
                    room_id=room_id,
                    user_id=user_id,
                )
                return True
            except Exception as e:
                await self.db.rollback()
                logger.error(
                    "Error removing member",
                    error=str(e),
                    room_id=room_id,
                    user_id=user_id,
                )
                return False

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error removing chat room member",
                error=str(e),
                room_id=room_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to remove chat room member: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def update_member_role(self, room_id: str, user_id: str, role: ChatMemberRole) -> bool:
        """
        Update a member's role in a chat room.

        Args:
            room_id: ID of the chat room
            user_id: ID of the user
            role: New role for the user

        Returns:
            True if successful, False otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.info(
            "Updating chat room member role",
            room_id=room_id,
            user_id=user_id,
            role=role,
        )
        try:
            # Find the member
            query = select(ChatMember).where(
                and_(
                    ChatMember.room_id == uuid.UUID(room_id),
                    ChatMember.user_id == uuid.UUID(user_id),
                    ChatMember.is_active == True,
                    )
            )
            result = await self.db.execute(query)
            member = result.scalar_one_or_none()

            if not member:
                logger.warning(
                    "Member not found for role update",
                    room_id=room_id,
                    user_id=user_id,
                )
                return False

            # Update role
            member.role = role

            try:
                await self.db.commit()
                logger.info(
                    "Chat room member role updated",
                    room_id=room_id,
                    user_id=user_id,
                    role=role,
                )
                return True
            except Exception as e:
                await self.db.rollback()
                logger.error(
                    "Error updating member role",
                    error=str(e),
                    room_id=room_id,
                    user_id=user_id,
                )
                return False

        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(
                "Database error updating member role",
                error=str(e),
                room_id=room_id,
                user_id=user_id,
            )
            raise DatabaseException(
                message=f"Failed to update member role: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def find_direct_chat(self, user_id1: str, user_id2: str) -> Optional[str]:
        """
        Find a direct chat room between two users.

        Args:
            user_id1: ID of the first user
            user_id2: ID of the second user

        Returns:
            Room ID if found, None otherwise

        Raises:
            DatabaseException: If a database error occurs
        """
        logger.debug(
            "Finding direct chat",
            user_id1=user_id1,
            user_id2=user_id2,
        )
        try:
            # Find rooms where user1 is a member
            query = (
                select(ChatRoom)
                .join(ChatMember, ChatRoom.id == ChatMember.room_id)
                .where(
                    and_(
                        ChatRoom.type == ChatRoomType.DIRECT,
                        ChatRoom.is_active == True,
                        ChatMember.user_id == uuid.UUID(user_id1),
                        ChatMember.is_active == True,
                        )
                )
            )
            result = await self.db.execute(query)
            rooms = result.scalars().all()

            # Check each room to see if user2 is also a member
            for room in rooms:
                member_query = select(ChatMember).where(
                    and_(
                        ChatMember.room_id == room.id,
                        ChatMember.user_id == uuid.UUID(user_id2),
                        ChatMember.is_active == True,
                        )
                )
                member_result = await self.db.execute(member_query)
                member = member_result.scalar_one_or_none()

                if member:
                    logger.debug(
                        "Found direct chat",
                        room_id=str(room.id),
                        user_id1=user_id1,
                        user_id2=user_id2,
                    )
                    return str(room.id)

            logger.debug(
                "No direct chat found",
                user_id1=user_id1,
                user_id2=user_id2,
            )
            return None

        except SQLAlchemyError as e:
            logger.error(
                "Database error finding direct chat",
                error=str(e),
                user_id1=user_id1,
                user_id2=user_id2,
            )
            raise DatabaseException(
                message=f"Failed to find direct chat: {str(e)}",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    async def create_direct_chat(self, user_id1: str, user_id2: str) -> str:
        """
        Create a direct chat room between two users or return existing one.

        Args:
            user_id1: ID of the first user
            user_id2: ID of the second user

        Returns:
            ID of the created/existing direct chat room

        Raises:
            ValidationException: If the input data is invalid
            DatabaseException: If a database error occurs
            BusinessLogicException: If there's a logical error creating the room
        """
        logger.info(
            "Creating direct chat",
            user_id1=user_id1,
            user_id2=user_id2,
        )

        # Check for existing direct chat
        existing_room_id = await self.find_direct_chat(user_id1, user_id2)
        if existing_room_id:
            logger.debug(
                "Using existing direct chat",
                room_id=existing_room_id,
                user_id1=user_id1,
                user_id2=user_id2,
            )
            return existing_room_id

        # Create new direct chat
        members = [
            {"user_id": user_id1, "role": ChatMemberRole.MEMBER},
            {"user_id": user_id2, "role": ChatMemberRole.MEMBER},
        ]

        room = await self.create_room(
            name=None,
            room_type=ChatRoomType.DIRECT,
            creator_id=user_id1,
            members=members,
        )

        logger.info(
            "Created new direct chat",
            room_id=str(room.id),
            user_id1=user_id1,
            user_id2=user_id2,
        )

        return str(room.id)

    @classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
        from app.services import service_registry
        service_registry.register(cls, "chat_service")
