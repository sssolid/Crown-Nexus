from __future__ import annotations

"""Chat repository implementation.

This module provides data access and persistence operations for Chat entities.
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Set, Tuple

from sqlalchemy import select, and_, or_, func, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import (
    ChatRoom,
    ChatMember,
    ChatMessage,
    MessageReaction,
    RateLimitLog,
    ChatRoomType,
    ChatMemberRole,
    MessageType,
)
from app.repositories.base import BaseRepository
from app.core.exceptions import (
    ResourceNotFoundException,
    BusinessException,
    PermissionDeniedException,
    RateLimitException,
)


class ChatRoomRepository(BaseRepository[ChatRoom, uuid.UUID]):
    """Repository for ChatRoom entity operations.

    Provides methods for querying, creating, updating, and deleting
    ChatRoom entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the chat room repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ChatRoom, db=db)

    async def find_direct_chat(
        self, user1_id: uuid.UUID, user2_id: uuid.UUID
    ) -> Optional[ChatRoom]:
        """Find a direct chat between two users.

        Args:
            user1_id: First user ID.
            user2_id: Second user ID.

        Returns:
            The direct chat room if found, None otherwise.
        """
        # Find room IDs where both users are members
        subquery1 = (
            select(ChatMember.room_id)
            .where(ChatMember.user_id == user1_id, ChatMember.is_active == True)
            .subquery()
        )

        subquery2 = (
            select(ChatMember.room_id)
            .where(ChatMember.user_id == user2_id, ChatMember.is_active == True)
            .subquery()
        )

        # Find direct chat rooms that both users are members of
        query = select(ChatRoom).where(
            ChatRoom.id.in_(subquery1),
            ChatRoom.id.in_(subquery2),
            ChatRoom.type == ChatRoomType.DIRECT,
            ChatRoom.is_active == True,
            ChatRoom.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_rooms_for_user(
        self,
        user_id: uuid.UUID,
        room_type: Optional[ChatRoomType] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get paginated list of chat rooms for a user.

        Args:
            user_id: The user ID to filter by.
            room_type: Optional room type to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        # Build conditions
        conditions = [
            ChatMember.user_id == user_id,
            ChatMember.is_active == True,
            ChatRoom.is_active == True,
            ChatRoom.is_deleted == False,
        ]

        if room_type:
            conditions.append(ChatRoom.type == room_type)

        # Query rooms, joining with ChatMember to filter by user
        query = (
            select(ChatRoom)
            .join(ChatMember, ChatRoom.id == ChatMember.room_id)
            .where(and_(*conditions))
            .order_by(desc(ChatRoom.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def get_company_rooms(
        self, company_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of chat rooms for a company.

        Args:
            company_id: The company ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(ChatRoom)
            .where(
                ChatRoom.company_id == company_id,
                ChatRoom.is_active == True,
                ChatRoom.is_deleted == False,
            )
            .order_by(desc(ChatRoom.updated_at))
        )

        return await self.paginate(query, page, page_size)

    async def create_direct_chat(
        self, user1_id: uuid.UUID, user2_id: uuid.UUID
    ) -> Tuple[ChatRoom, List[ChatMember]]:
        """Create a direct chat between two users.

        Args:
            user1_id: First user ID.
            user2_id: Second user ID.

        Returns:
            Tuple containing (chat room, list of members).

        Raises:
            BusinessException: If a direct chat already exists between the users.
        """
        # Check if a direct chat already exists
        existing_chat = await self.find_direct_chat(user1_id, user2_id)
        if existing_chat:
            raise BusinessException(
                message="Direct chat already exists between these users",
                details={
                    "user1_id": str(user1_id),
                    "user2_id": str(user2_id),
                    "existing_chat_id": str(existing_chat.id),
                },
            )

        # Create new chat room
        room = ChatRoom(
            name=None,  # Direct chats don't need names
            type=ChatRoomType.DIRECT,
            company_id=None,  # Direct chats aren't associated with companies
            is_active=True,
        )

        self.db.add(room)
        await self.db.flush()

        # Create member records
        members = []
        member1 = ChatMember(
            room_id=room.id,
            user_id=user1_id,
            role=ChatMemberRole.MEMBER,
            is_active=True,
        )
        member2 = ChatMember(
            room_id=room.id,
            user_id=user2_id,
            role=ChatMemberRole.MEMBER,
            is_active=True,
        )

        self.db.add(member1)
        self.db.add(member2)
        await self.db.flush()

        members = [member1, member2]

        await self.db.refresh(room)
        for member in members:
            await self.db.refresh(member)

        return room, members

    async def create_group_chat(
        self,
        name: str,
        creator_id: uuid.UUID,
        member_ids: List[uuid.UUID],
        company_id: Optional[uuid.UUID] = None,
    ) -> Tuple[ChatRoom, List[ChatMember]]:
        """Create a group chat.

        Args:
            name: Group chat name.
            creator_id: ID of the user creating the chat.
            member_ids: List of member user IDs.
            company_id: Optional company ID to associate with the chat.

        Returns:
            Tuple containing (chat room, list of members).

        Raises:
            BusinessException: If no members are provided.
        """
        # Ensure we have members
        unique_member_ids = set(member_ids)
        unique_member_ids.add(creator_id)  # Ensure creator is a member

        if not unique_member_ids:
            raise BusinessException(message="Group chat must have at least one member")

        # Create chat room
        room = ChatRoom(
            name=name, type=ChatRoomType.GROUP, company_id=company_id, is_active=True
        )

        self.db.add(room)
        await self.db.flush()

        # Create member records
        members = []
        for user_id in unique_member_ids:
            # Creator is the owner, others are regular members
            role = (
                ChatMemberRole.OWNER if user_id == creator_id else ChatMemberRole.MEMBER
            )

            member = ChatMember(
                room_id=room.id, user_id=user_id, role=role, is_active=True
            )

            self.db.add(member)
            members.append(member)

        await self.db.flush()

        await self.db.refresh(room)
        for member in members:
            await self.db.refresh(member)

        return room, members

    async def add_members(
        self,
        room_id: uuid.UUID,
        user_ids: List[uuid.UUID],
        role: ChatMemberRole = ChatMemberRole.MEMBER,
        added_by_id: uuid.UUID = None,
    ) -> List[ChatMember]:
        """Add members to a chat room.

        Args:
            room_id: ID of the chat room.
            user_ids: List of user IDs to add.
            role: Role to assign to the new members.
            added_by_id: ID of the user adding the members.

        Returns:
            List of created member records.

        Raises:
            ResourceNotFoundException: If the room doesn't exist.
            PermissionDeniedException: If the user doesn't have permission.
        """
        # Check room exists
        room = await self.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(
                resource_type="ChatRoom", resource_id=str(room_id)
            )

        # If added_by_id is provided, check permissions
        if added_by_id:
            # Direct chats can't have additional members
            if room.type == ChatRoomType.DIRECT:
                raise BusinessException(message="Cannot add members to a direct chat")

            # Check if the user adding members has permission
            member_repo = ChatMemberRepository(self.db)
            adder_member = await member_repo.find_by_room_and_user(room_id, added_by_id)

            if not adder_member or adder_member.role not in [
                ChatMemberRole.OWNER,
                ChatMemberRole.ADMIN,
            ]:
                raise PermissionDeniedException(
                    message="You don't have permission to add members to this chat",
                    action="add_members",
                    resource_type="ChatRoom",
                )

        # Get existing members to avoid duplicates
        member_repo = ChatMemberRepository(self.db)
        existing_members = await member_repo.get_by_room(room_id)
        existing_user_ids = {member.user_id for member in existing_members}

        # Add new members
        new_members = []
        for user_id in user_ids:
            # Skip if already a member
            if user_id in existing_user_ids:
                continue

            member = ChatMember(
                room_id=room_id, user_id=user_id, role=role, is_active=True
            )

            self.db.add(member)
            new_members.append(member)

        if new_members:
            await self.db.flush()
            for member in new_members:
                await self.db.refresh(member)

        return new_members

    async def ensure_exists(self, room_id: uuid.UUID) -> ChatRoom:
        """Ensure a chat room exists by ID, raising an exception if not found.

        Args:
            room_id: The chat room ID to check.

        Returns:
            The chat room if found.

        Raises:
            ResourceNotFoundException: If the chat room is not found.
        """
        room = await self.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(
                resource_type="ChatRoom", resource_id=str(room_id)
            )
        return room


class ChatMemberRepository(BaseRepository[ChatMember, uuid.UUID]):
    """Repository for ChatMember entity operations.

    Provides methods for querying, creating, updating, and deleting
    ChatMember entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the chat member repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ChatMember, db=db)

    async def find_by_room_and_user(
        self, room_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[ChatMember]:
        """Find a chat membership for a specific room and user.

        Args:
            room_id: The chat room ID.
            user_id: The user ID.

        Returns:
            The chat member if found, None otherwise.
        """
        query = select(ChatMember).where(
            ChatMember.room_id == room_id,
            ChatMember.user_id == user_id,
            ChatMember.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_room(
        self, room_id: uuid.UUID, active_only: bool = True
    ) -> List[ChatMember]:
        """Get all members of a chat room.

        Args:
            room_id: The chat room ID.
            active_only: Whether to include only active members.

        Returns:
            List of chat members in the room.
        """
        conditions = [ChatMember.room_id == room_id, ChatMember.is_deleted == False]

        if active_only:
            conditions.append(ChatMember.is_active == True)

        query = select(ChatMember).where(and_(*conditions))

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_user(self, user_id: uuid.UUID) -> List[ChatMember]:
        """Get all chat memberships for a user.

        Args:
            user_id: The user ID.

        Returns:
            List of chat memberships for the user.
        """
        query = select(ChatMember).where(
            ChatMember.user_id == user_id,
            ChatMember.is_active == True,
            ChatMember.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_last_read(
        self,
        room_id: uuid.UUID,
        user_id: uuid.UUID,
        timestamp: Optional[datetime] = None,
    ) -> Optional[ChatMember]:
        """Update the last read timestamp for a member.

        Args:
            room_id: The chat room ID.
            user_id: The user ID.
            timestamp: Optional custom timestamp (defaults to now).

        Returns:
            The updated member if found, None otherwise.
        """
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

    async def update_role(
        self,
        room_id: uuid.UUID,
        user_id: uuid.UUID,
        new_role: ChatMemberRole,
        updated_by_id: uuid.UUID,
    ) -> Optional[ChatMember]:
        """Update the role of a chat member.

        Args:
            room_id: The chat room ID.
            user_id: The user ID.
            new_role: The new role to assign.
            updated_by_id: ID of the user making the change.

        Returns:
            The updated member if found, None otherwise.

        Raises:
            PermissionDeniedException: If the user doesn't have permission.
        """
        # Get the member to update
        member = await self.find_by_room_and_user(room_id, user_id)
        if not member:
            return None

        # Get the user making the change
        updater = await self.find_by_room_and_user(room_id, updated_by_id)
        if not updater or updater.role not in [
            ChatMemberRole.OWNER,
            ChatMemberRole.ADMIN,
        ]:
            raise PermissionDeniedException(
                message="You don't have permission to update member roles",
                action="update_role",
                resource_type="ChatMember",
            )

        # An admin can't change an owner's role
        if updater.role == ChatMemberRole.ADMIN and member.role == ChatMemberRole.OWNER:
            raise PermissionDeniedException(
                message="Administrators cannot change the role of the room owner",
                action="update_role",
                resource_type="ChatMember",
            )

        # Update the role
        member.role = new_role
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)

        return member

    async def remove_member(
        self, room_id: uuid.UUID, user_id: uuid.UUID, removed_by_id: uuid.UUID
    ) -> bool:
        """Remove a member from a chat room.

        Args:
            room_id: The chat room ID.
            user_id: The user ID to remove.
            removed_by_id: ID of the user performing the removal.

        Returns:
            True if the member was removed, False otherwise.

        Raises:
            PermissionDeniedException: If the user doesn't have permission.
        """
        # Get the member to remove
        member = await self.find_by_room_and_user(room_id, user_id)
        if not member:
            return False

        # Check if self-removal
        if user_id == removed_by_id:
            # Users can remove themselves
            return await self.delete(member.id)

        # Get the user performing the removal
        remover = await self.find_by_room_and_user(room_id, removed_by_id)
        if not remover or remover.role not in [
            ChatMemberRole.OWNER,
            ChatMemberRole.ADMIN,
        ]:
            raise PermissionDeniedException(
                message="You don't have permission to remove members from this chat",
                action="remove_member",
                resource_type="ChatMember",
            )

        # An admin can't remove an owner or another admin
        if remover.role == ChatMemberRole.ADMIN and member.role in [
            ChatMemberRole.OWNER,
            ChatMemberRole.ADMIN,
        ]:
            raise PermissionDeniedException(
                message="Administrators cannot remove owners or other administrators",
                action="remove_member",
                resource_type="ChatMember",
            )

        # Remove the member
        return await self.delete(member.id)

    async def ensure_exists(self, member_id: uuid.UUID) -> ChatMember:
        """Ensure a chat member exists by ID, raising an exception if not found.

        Args:
            member_id: The chat member ID to check.

        Returns:
            The chat member if found.

        Raises:
            ResourceNotFoundException: If the chat member is not found.
        """
        member = await self.get_by_id(member_id)
        if not member:
            raise ResourceNotFoundException(
                resource_type="ChatMember", resource_id=str(member_id)
            )
        return member


class ChatMessageRepository(BaseRepository[ChatMessage, uuid.UUID]):
    """Repository for ChatMessage entity operations.

    Provides methods for querying, creating, updating, and deleting
    ChatMessage entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the chat message repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ChatMessage, db=db)

    async def get_room_messages(
        self,
        room_id: uuid.UUID,
        limit: int = 50,
        before_id: Optional[uuid.UUID] = None,
        include_deleted: bool = False,
    ) -> List[ChatMessage]:
        """Get messages for a chat room.

        Args:
            room_id: The chat room ID.
            limit: Maximum number of messages to return.
            before_id: Optional message ID to get messages before.
            include_deleted: Whether to include deleted messages.

        Returns:
            List of chat messages.
        """
        conditions = [ChatMessage.room_id == room_id, ChatMessage.is_deleted == False]

        if not include_deleted:
            conditions.append(ChatMessage.is_deleted == False)

        if before_id:
            # Get the created_at timestamp of the reference message
            sub_query = select(ChatMessage.created_at).where(
                ChatMessage.id == before_id
            )
            sub_result = await self.db.execute(sub_query)
            reference_timestamp = sub_result.scalar()

            if reference_timestamp:
                conditions.append(ChatMessage.created_at < reference_timestamp)

        query = (
            select(ChatMessage)
            .where(and_(*conditions))
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
        )

        result = await self.db.execute(query)
        messages = list(result.scalars().all())

        # Return in ascending order (oldest first)
        return list(reversed(messages))

    async def send_message(
        self,
        room_id: uuid.UUID,
        sender_id: uuid.UUID,
        content: str,
        message_type: MessageType = MessageType.TEXT,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatMessage:
        """Send a message to a chat room.

        Args:
            room_id: The chat room ID.
            sender_id: The sender user ID.
            content: The message content.
            message_type: The message type.
            extra_metadata: Optional message metadata.

        Returns:
            The created message.

        Raises:
            ResourceNotFoundException: If the room doesn't exist.
            PermissionDeniedException: If the user isn't a member of the room.
        """
        # Check rate limits first
        await self.check_rate_limit(sender_id, room_id, "send_message")

        # Check room exists
        room_repo = ChatRoomRepository(self.db)
        room = await room_repo.get_by_id(room_id)
        if not room:
            raise ResourceNotFoundException(
                resource_type="ChatRoom", resource_id=str(room_id)
            )

        # Check sender is a member of the room
        member_repo = ChatMemberRepository(self.db)
        member = await member_repo.find_by_room_and_user(room_id, sender_id)
        if not member or not member.is_active:
            raise PermissionDeniedException(
                message="You are not a member of this chat room",
                action="send_message",
                resource_type="ChatRoom",
            )

        # Create the message
        message = ChatMessage(
            room_id=room_id,
            sender_id=sender_id,
            message_type=message_type,
            extra_metadata=extra_metadata or {},
        )
        message.content = content  # This will encrypt the content

        self.db.add(message)
        await self.db.flush()

        # Update member's last read timestamp
        await member_repo.update_last_read(room_id, sender_id)

        # Update room's updated_at timestamp
        room.updated_at = datetime.now()
        self.db.add(room)

        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def edit_message(
        self, message_id: uuid.UUID, new_content: str, edited_by_id: uuid.UUID
    ) -> Optional[ChatMessage]:
        """Edit a message.

        Args:
            message_id: The message ID.
            new_content: The new message content.
            edited_by_id: ID of the user making the edit.

        Returns:
            The updated message if found, None otherwise.

        Raises:
            PermissionDeniedException: If the user doesn't have permission.
        """
        message = await self.get_by_id(message_id)
        if not message or message.is_deleted:
            return None

        # Only the sender can edit their messages
        if message.sender_id != edited_by_id:
            raise PermissionDeniedException(
                message="You can only edit your own messages",
                action="edit_message",
                resource_type="ChatMessage",
            )

        # Update the message
        message.content = new_content
        message.updated_at = datetime.now()

        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def delete_message(
        self, message_id: uuid.UUID, deleted_by_id: uuid.UUID
    ) -> Optional[ChatMessage]:
        """Delete a message.

        Args:
            message_id: The message ID.
            deleted_by_id: ID of the user deleting the message.

        Returns:
            The deleted message if found, None otherwise.

        Raises:
            PermissionDeniedException: If the user doesn't have permission.
        """
        message = await self.get_by_id(message_id)
        if not message or message.is_deleted:
            return None

        # Check if user has permission to delete
        if message.sender_id != deleted_by_id:
            # If not the sender, check if admin/owner of the room
            member_repo = ChatMemberRepository(self.db)
            member = await member_repo.find_by_room_and_user(
                message.room_id, deleted_by_id
            )

            if not member or member.role not in [
                ChatMemberRole.OWNER,
                ChatMemberRole.ADMIN,
            ]:
                raise PermissionDeniedException(
                    message="You don't have permission to delete this message",
                    action="delete_message",
                    resource_type="ChatMessage",
                )

        # Soft delete the message
        message.is_deleted = True
        message.deleted_at = datetime.now()

        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)

        return message

    async def check_rate_limit(
        self,
        user_id: uuid.UUID,
        room_id: uuid.UUID,
        event_type: str,
        max_count: int = 10,
        window_seconds: int = 60,
    ) -> None:
        """Check if a user has exceeded rate limits for an event type.

        Args:
            user_id: The user ID.
            room_id: The chat room ID.
            event_type: The event type being limited.
            max_count: Maximum allowed events in the time window.
            window_seconds: Time window in seconds.

        Raises:
            RateLimitException: If the rate limit is exceeded.
        """
        # Calculate time window
        window_start = datetime.now() - timedelta(seconds=window_seconds)

        # Count events in the window
        query = (
            select(func.count())
            .select_from(RateLimitLog)
            .where(
                RateLimitLog.user_id == user_id,
                RateLimitLog.room_id == room_id,
                RateLimitLog.event_type == event_type,
                RateLimitLog.timestamp >= window_start,
            )
        )

        result = await self.db.execute(query)
        count = result.scalar() or 0

        if count >= max_count:
            # Get remaining time until oldest event expires
            oldest_query = (
                select(RateLimitLog.timestamp)
                .where(
                    RateLimitLog.user_id == user_id,
                    RateLimitLog.room_id == room_id,
                    RateLimitLog.event_type == event_type,
                    RateLimitLog.timestamp >= window_start,
                )
                .order_by(RateLimitLog.timestamp)
                .limit(1)
            )

            oldest_result = await self.db.execute(oldest_query)
            oldest_timestamp = oldest_result.scalar()

            if oldest_timestamp:
                reset_time = oldest_timestamp + timedelta(seconds=window_seconds)
                seconds_remaining = int((reset_time - datetime.now()).total_seconds())

                raise RateLimitException(
                    message=f"Rate limit exceeded for {event_type}. Try again later.",
                    headers={
                        "X-RateLimit-Limit": str(max_count),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(seconds_remaining),
                    },
                )

        # Log this event
        log = RateLimitLog(
            user_id=user_id,
            room_id=room_id,
            event_type=event_type,
            timestamp=datetime.now(),
            count=1,
        )

        self.db.add(log)
        await self.db.flush()

    async def ensure_exists(self, message_id: uuid.UUID) -> ChatMessage:
        """Ensure a chat message exists by ID, raising an exception if not found.

        Args:
            message_id: The chat message ID to check.

        Returns:
            The chat message if found.

        Raises:
            ResourceNotFoundException: If the chat message is not found.
        """
        message = await self.get_by_id(message_id)
        if not message:
            raise ResourceNotFoundException(
                resource_type="ChatMessage", resource_id=str(message_id)
            )
        return message


class MessageReactionRepository(BaseRepository[MessageReaction, uuid.UUID]):
    """Repository for MessageReaction entity operations.

    Provides methods for querying, creating, updating, and deleting
    MessageReaction entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the message reaction repository.

        Args:
            db: The database session.
        """
        super().__init__(model=MessageReaction, db=db)

    async def find_by_message_user_reaction(
        self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str
    ) -> Optional[MessageReaction]:
        """Find a reaction by message, user, and reaction type.

        Args:
            message_id: The message ID.
            user_id: The user ID.
            reaction: The reaction string.

        Returns:
            The reaction if found, None otherwise.
        """
        query = select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.user_id == user_id,
            MessageReaction.reaction == reaction,
            MessageReaction.is_deleted == False,
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_message(self, message_id: uuid.UUID) -> List[MessageReaction]:
        """Get all reactions for a message.

        Args:
            message_id: The message ID.

        Returns:
            List of reactions for the message.
        """
        query = select(MessageReaction).where(
            MessageReaction.message_id == message_id,
            MessageReaction.is_deleted == False,
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def add_reaction(
        self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str
    ) -> MessageReaction:
        """Add a reaction to a message.

        Args:
            message_id: The message ID.
            user_id: The user ID.
            reaction: The reaction string.

        Returns:
            The created or existing reaction.

        Raises:
            ResourceNotFoundException: If the message doesn't exist.
            PermissionDeniedException: If the user isn't a member of the room.
        """
        # Check if the reaction already exists
        existing_reaction = await self.find_by_message_user_reaction(
            message_id, user_id, reaction
        )

        if existing_reaction:
            return existing_reaction

        # Check message exists
        message_repo = ChatMessageRepository(self.db)
        message = await message_repo.get_by_id(message_id)
        if not message or message.is_deleted:
            raise ResourceNotFoundException(
                resource_type="ChatMessage", resource_id=str(message_id)
            )

        # Check user is a member of the room
        member_repo = ChatMemberRepository(self.db)
        member = await member_repo.find_by_room_and_user(message.room_id, user_id)
        if not member or not member.is_active:
            raise PermissionDeniedException(
                message="You are not a member of this chat room",
                action="add_reaction",
                resource_type="ChatRoom",
            )

        # Create the reaction
        reaction_obj = MessageReaction(
            message_id=message_id, user_id=user_id, reaction=reaction
        )

        self.db.add(reaction_obj)
        await self.db.flush()
        await self.db.refresh(reaction_obj)

        return reaction_obj

    async def remove_reaction(
        self, message_id: uuid.UUID, user_id: uuid.UUID, reaction: str
    ) -> bool:
        """Remove a reaction from a message.

        Args:
            message_id: The message ID.
            user_id: The user ID.
            reaction: The reaction string.

        Returns:
            True if the reaction was removed, False otherwise.
        """
        # Find the reaction
        existing_reaction = await self.find_by_message_user_reaction(
            message_id, user_id, reaction
        )

        if not existing_reaction:
            return False

        # Delete the reaction
        return await self.delete(existing_reaction.id)

    async def get_reaction_counts(self, message_id: uuid.UUID) -> Dict[str, int]:
        """Get counts of each reaction type for a message.

        Args:
            message_id: The message ID.

        Returns:
            Dictionary mapping reaction strings to counts.
        """
        query = (
            select(MessageReaction.reaction, func.count(MessageReaction.id))
            .where(
                MessageReaction.message_id == message_id,
                MessageReaction.is_deleted == False,
            )
            .group_by(MessageReaction.reaction)
        )

        result = await self.db.execute(query)
        return {reaction: count for reaction, count in result.all()}

    async def get_user_reactions(
        self, message_id: uuid.UUID, reaction: str
    ) -> List[uuid.UUID]:
        """Get user IDs who reacted with a specific reaction to a message.

        Args:
            message_id: The message ID.
            reaction: The reaction string.

        Returns:
            List of user IDs.
        """
        query = select(MessageReaction.user_id).where(
            MessageReaction.message_id == message_id,
            MessageReaction.reaction == reaction,
            MessageReaction.is_deleted == False,
        )

        result = await self.db.execute(query)
        return [row[0] for row in result.all()]
