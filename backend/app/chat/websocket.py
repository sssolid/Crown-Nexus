# backend/app/chat/websocket.py
from __future__ import annotations

import asyncio
import json
import uuid
import datetime
from typing import Any, Dict, Optional, cast

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_ws, get_db
from app.chat.connection import manager, redis_manager
from app.chat.schemas import (
    ChatMessageSchema,
    CommandType,
    MessageType,
    WebSocketCommand,
    WebSocketResponse,
)
from app.chat.service import ChatService
from app.core.exceptions import (
    BusinessLogicException,
    ErrorCode,
    PermissionDeniedException,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.service_registry import get_service

from app.core.security import sanitize_input, moderate_content
from app.models.user import User
from app.services.audit_service import AuditEventType, AuditLogLevel, AuditService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService
from app.utils.redis_manager import rate_limit_check

logger = get_logger("app.chat.websocket")
router = APIRouter()


async def get_audit_service() -> AuditService:
    """Get the audit service instance."""
    return cast(AuditService, get_service("audit_service"))


async def get_metrics_service() -> MetricsService:
    """Get the metrics service instance."""
    return cast(MetricsService, get_service("metrics_service"))


async def get_validation_service() -> ValidationService:
    """Get the validation service instance."""
    return cast(ValidationService, get_service("validation_service"))


@router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
):
    """
    WebSocket endpoint for chat functionality.

    This endpoint manages the WebSocket connection for chat clients, handling
    commands for joining/leaving rooms, sending/receiving messages, and more.

    Args:
        websocket: The WebSocket connection
        db: Database session for database operations
        current_user: The authenticated user
    """
    connection_id = str(uuid.uuid4())
    user_id = str(current_user.id)

    # Get services
    chat_service = ChatService(db)
    audit_service = await get_audit_service()
    metrics_service = await get_metrics_service()
    validation_service = await get_validation_service()

    # Initialize metrics
    metrics_service.increment_counter(
        "websocket_connections_total", labels={"user_id": user_id}
    )

    # Log connection
    logger.info(
        "WebSocket connection initiated", connection_id=connection_id, user_id=user_id
    )

    # Audit log connection
    await audit_service.log_event(
        event_type=AuditEventType.USER_LOGIN,
        user_id=user_id,
        resource_type="websocket",
        resource_id=connection_id,
        details={"connection_type": "websocket", "source": "chat"},
        level=AuditLogLevel.INFO,
    )

    await redis_manager.start_pubsub_listener()

    try:
        # Accept the connection
        await manager.connect(websocket, connection_id, user_id)

        # Mark user as online
        online_key = f"user:online:{user_id}"
        await websocket.send_json(
            WebSocketResponse(
                type="connected",
                data={
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                },
            ).dict()
        )

        # Send the user's room list
        user_rooms = await chat_service.get_user_rooms(user_id)
        await websocket.send_json(
            WebSocketResponse(type="room_list", data={"rooms": user_rooms}).dict()
        )

        # Main WebSocket loop
        while True:
            # Receive and parse message
            data = await websocket.receive_text()

            # Check rate limiting
            is_limited, count = await rate_limit_check(
                f"rate:ws:{user_id}", limit=50, window=60
            )
            if is_limited:
                logger.warning(
                    "Rate limit exceeded for WebSocket user",
                    user_id=user_id,
                    count=count,
                )
                metrics_service.increment_counter(
                    "websocket_rate_limit_exceeded", labels={"user_id": user_id}
                )
                await websocket.send_json(
                    WebSocketResponse(
                        type="error",
                        success=False,
                        error="Rate limit exceeded. Please slow down.",
                    ).dict()
                )
                continue

            try:
                # Parse and validate command
                command_data = json.loads(data)

                # Security check for suspicious input
                if not validate_json_input(command_data):
                    logger.warning(
                        "Suspicious WebSocket input rejected",
                        user_id=user_id,
                        connection_id=connection_id,
                    )
                    await websocket.send_json(
                        WebSocketResponse(
                            type="error",
                            success=False,
                            error="Invalid or suspicious input detected",
                        ).dict()
                    )
                    continue

                command = WebSocketCommand(**command_data)

                # Process the command with metrics tracking
                with metrics_service.timer(
                    "histogram",
                    "websocket_command_processing_seconds",
                    {"command": command.command},
                ):
                    await process_command(
                        command=command,
                        websocket=websocket,
                        connection_id=connection_id,
                        user=current_user,
                        chat_service=chat_service,
                        audit_service=audit_service,
                    )

                # Increment command counter
                metrics_service.increment_counter(
                    "websocket_commands_processed",
                    labels={"command": command.command, "user_id": user_id},
                )

            except json.JSONDecodeError:
                logger.error(
                    "Invalid JSON received from client", connection_id=connection_id
                )
                await websocket.send_json(
                    WebSocketResponse(
                        type="error", success=False, error="Invalid JSON message format"
                    ).dict()
                )

            except ValidationException as e:
                logger.warning(
                    "Validation error processing WebSocket command",
                    error=str(e),
                    connection_id=connection_id,
                    user_id=user_id,
                )
                await websocket.send_json(
                    WebSocketResponse(
                        type="error", success=False, error=f"Validation error: {str(e)}"
                    ).dict()
                )

            except Exception as e:
                logger.exception(
                    "Error processing WebSocket message",
                    error=str(e),
                    connection_id=connection_id,
                    user_id=user_id,
                )
                await websocket.send_json(
                    WebSocketResponse(
                        type="error", success=False, error="Internal server error"
                    ).dict()
                )

    except WebSocketDisconnect:
        logger.info(
            "WebSocket disconnected",
            connection_id=connection_id,
            user_id=user_id,
        )

    except Exception as e:
        logger.exception(
            "Unexpected WebSocket error",
            error=str(e),
            connection_id=connection_id,
            user_id=user_id,
        )

    finally:
        # Clean up connection
        manager.disconnect(connection_id)

        # Update last seen time
        last_seen_key = f"user:last_seen:{user_id}"
        current_time = datetime.datetime.now(datetime.UTC).isoformat()

        # Log disconnection
        logger.info(
            "WebSocket connection terminated",
            connection_id=connection_id,
            user_id=user_id,
            last_seen=current_time,
        )

        # Audit log disconnection
        await audit_service.log_event(
            event_type=AuditEventType.USER_LOGOUT,
            user_id=user_id,
            resource_type="websocket",
            resource_id=connection_id,
            details={"connection_type": "websocket", "last_seen": current_time},
            level=AuditLogLevel.INFO,
        )


async def process_command(
    command: WebSocketCommand,
    websocket: WebSocket,
    connection_id: str,
    user: User,
    chat_service: ChatService,
    audit_service: AuditService,
) -> None:
    """
    Process a WebSocket command.

    Args:
        command: The command to process
        websocket: The WebSocket connection
        connection_id: Unique connection identifier
        user: The authenticated user
        chat_service: Chat service for chat operations
        audit_service: Audit service for logging events

    Raises:
        ValidationException: If the command data is invalid
        PermissionDeniedException: If the user lacks permission
        ResourceNotFoundException: If a required resource isn't found
        BusinessLogicException: If there's a logical error processing the command
    """
    user_id = str(user.id)

    # JOIN_ROOM command
    if command.command == CommandType.JOIN_ROOM:
        room_id = command.data.get("room_id") or command.room_id
        if not room_id:
            raise ValidationException(message="Room ID is required")

        # Sanitize input
        room_id = sanitize_input(room_id)

        # Check access permission
        has_access = await chat_service.check_room_access(user_id, room_id)
        if not has_access:
            logger.warning(
                "Access denied to room",
                user_id=user_id,
                room_id=room_id,
            )
            raise PermissionDeniedException(
                message="Access denied to room",
                details={"room_id": room_id},
            )

        # Join the room
        manager.join_room(connection_id, room_id)
        room_info = await chat_service.get_room_info(room_id)

        # Send response
        await websocket.send_json(
            WebSocketResponse(type="room_joined", data=room_info).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_joined",
                data={
                    "room_id": room_id,
                    "user": {"id": user_id, "name": user.full_name},
                },
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

        # Audit log
        await audit_service.log_event(
            event_type=AuditEventType.USER_LOGIN,
            user_id=user_id,
            resource_type="chat_room",
            resource_id=room_id,
            details={"action": "join_room"},
            level=AuditLogLevel.INFO,
        )

    # LEAVE_ROOM command
    elif command.command == CommandType.LEAVE_ROOM:
        room_id = command.data.get("room_id") or command.room_id
        if not room_id:
            raise ValidationException(message="Room ID is required")

        # Sanitize input
        room_id = sanitize_input(room_id)

        # Leave the room
        manager.leave_room(connection_id, room_id)

        # Send response
        await websocket.send_json(
            WebSocketResponse(type="room_left", data={"room_id": room_id}).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_left",
                data={"room_id": room_id, "user_id": user_id},
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

        # Audit log
        await audit_service.log_event(
            event_type=AuditEventType.USER_LOGOUT,
            user_id=user_id,
            resource_type="chat_room",
            resource_id=room_id,
            details={"action": "leave_room"},
            level=AuditLogLevel.INFO,
        )

    # SEND_MESSAGE command
    elif command.command == CommandType.SEND_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        content = command.data.get("content")
        message_type = command.data.get("message_type", "text")

        # Validate required fields
        if not room_id or not content:
            raise ValidationException(message="Room ID and content are required")

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        # We don't sanitize content to preserve message formatting, but we do validate message type
        if not is_valid_enum_value(message_type, MessageType):
            raise ValidationException(message=f"Invalid message type: {message_type}")

        # Check access permission
        has_access = await chat_service.check_room_access(user_id, room_id)
        if not has_access:
            logger.warning(
                "Access denied to room",
                user_id=user_id,
                room_id=room_id,
            )
            raise PermissionDeniedException(
                message="Access denied to room",
                details={"room_id": room_id},
            )

        # Content moderation
        filtered_content = await moderate_content(content)

        # Create message
        message = await chat_service.create_message(
            room_id=room_id,
            sender_id=user_id,
            content=filtered_content,
            message_type=message_type,
            metadata=command.data.get("metadata", {}),
        )

        # Format message data
        message_data = {
            "id": str(message.id),
            "room_id": room_id,
            "sender_id": user_id,
            "sender_name": user.full_name,
            "message_type": message.message_type,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
            "metadata": message.metadata,
        }

        # Send response
        await websocket.send_json(
            WebSocketResponse(type="message_sent", data=message_data).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(type="new_message", data=message_data).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

        # Audit log
        await audit_service.log_event(
            event_type=AuditEventType.USER_CREATED,
            user_id=user_id,
            resource_type="chat_message",
            resource_id=str(message.id),
            details={
                "room_id": room_id,
                "message_type": message_type,
            },
            level=AuditLogLevel.INFO,
        )

    # READ_MESSAGES command
    elif command.command == CommandType.READ_MESSAGES:
        room_id = command.data.get("room_id") or command.room_id
        last_read_id = command.data.get("last_read_id")

        # Validate required fields
        if not room_id or not last_read_id:
            raise ValidationException(
                message="Room ID and last_read_id are required",
            )

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        last_read_id = sanitize_input(last_read_id)

        # Mark messages as read
        success = await chat_service.mark_as_read(user_id, room_id, last_read_id)
        if not success:
            logger.warning(
                "Failed to mark messages as read",
                user_id=user_id,
                room_id=room_id,
                last_read_id=last_read_id,
            )

        # Send response
        await websocket.send_json(
            WebSocketResponse(
                type="messages_read",
                data={"room_id": room_id, "last_read_id": last_read_id},
            ).dict()
        )

    # TYPING_START command
    elif command.command == CommandType.TYPING_START:
        room_id = command.data.get("room_id") or command.room_id

        # Validate required fields
        if not room_id:
            raise ValidationException(
                message="Room ID is required",
            )

        # Sanitize input
        room_id = sanitize_input(room_id)

        # Broadcast typing status to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_typing",
                data={
                    "room_id": room_id,
                    "user_id": user_id,
                    "user_name": user.full_name,
                },
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

    # TYPING_STOP command
    elif command.command == CommandType.TYPING_STOP:
        room_id = command.data.get("room_id") or command.room_id

        # Validate required fields
        if not room_id:
            raise ValidationException(message="Room ID is required")

        # Sanitize input
        room_id = sanitize_input(room_id)

        # Broadcast typing stopped status to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_typing_stopped",
                data={"room_id": room_id, "user_id": user_id},
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

    # FETCH_HISTORY command
    elif command.command == CommandType.FETCH_HISTORY:
        room_id = command.data.get("room_id") or command.room_id
        before_id = command.data.get("before_id")
        limit = int(command.data.get("limit", 50))

        # Validate required fields
        if not room_id:
            raise ValidationException(message="Room ID is required")

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        if before_id:
            before_id = sanitize_input(before_id)

        # Validate limit range
        if limit < 1 or limit > 100:
            limit = 50

        # Check access permission
        has_access = await chat_service.check_room_access(user_id, room_id)
        if not has_access:
            logger.warning(
                "Access denied to room",
                user_id=user_id,
                room_id=room_id,
            )
            raise PermissionDeniedException(
                message="Access denied to room",
                details={"room_id": room_id},
            )

        # Fetch message history
        messages = await chat_service.get_message_history(room_id, before_id, limit)

        # Send response
        await websocket.send_json(
            WebSocketResponse(
                type="message_history",
                data={"room_id": room_id, "messages": messages},
            ).dict()
        )

    # ADD_REACTION command
    elif command.command == CommandType.ADD_REACTION:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        reaction = command.data.get("reaction")

        # Validate required fields
        if not room_id or not message_id or not reaction:
            raise ValidationException(
                message="Room ID, message ID, and reaction are required"
            )

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        message_id = sanitize_input(message_id)
        # Don't sanitize reaction to preserve emoji

        # Add reaction
        success = await chat_service.add_reaction(
            message_id=message_id, user_id=user_id, reaction=reaction
        )

        if not success:
            logger.warning(
                "Failed to add reaction",
                user_id=user_id,
                message_id=message_id,
                reaction=reaction,
            )
            raise BusinessLogicException(
                message="Failed to add reaction",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
            )

        # Send response
        await websocket.send_json(
            WebSocketResponse(
                type="reaction_added",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": user_id,
                },
            ).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="reaction_added",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": user_id,
                    "user_name": user.full_name,
                },
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

    # REMOVE_REACTION command
    elif command.command == CommandType.REMOVE_REACTION:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        reaction = command.data.get("reaction")

        # Validate required fields
        if not room_id or not message_id or not reaction:
            raise ValidationException(
                message="Room ID, message ID, and reaction are required"
            )

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        message_id = sanitize_input(message_id)
        # Don't sanitize reaction to preserve emoji

        # Remove reaction
        success = await chat_service.remove_reaction(
            message_id=message_id, user_id=user_id, reaction=reaction
        )

        if not success:
            logger.warning(
                "Failed to remove reaction",
                user_id=user_id,
                message_id=message_id,
                reaction=reaction,
            )
            raise BusinessLogicException(
                message="Failed to remove reaction",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
            )

        # Send response
        await websocket.send_json(
            WebSocketResponse(
                type="reaction_removed",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": user_id,
                },
            ).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="reaction_removed",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": user_id,
                },
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

    # EDIT_MESSAGE command
    elif command.command == CommandType.EDIT_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        content = command.data.get("content")

        # Validate required fields
        if not room_id or not message_id or not content:
            raise ValidationException(
                message="Room ID, message ID, and content are required"
            )

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        message_id = sanitize_input(message_id)
        # Don't sanitize content to preserve message formatting

        # Check permission to edit message
        can_edit = await chat_service.check_message_permission(
            message_id=message_id, user_id=user_id
        )

        if not can_edit:
            logger.warning(
                "Permission denied to edit message",
                user_id=user_id,
                message_id=message_id,
            )
            raise PermissionDeniedException(
                message="Permission denied to edit message",
                details={"message_id": message_id},
            )

        # Content moderation
        filtered_content = await moderate_content(content)

        # Edit message
        success, updated_message = await chat_service.edit_message(
            message_id=message_id, content=filtered_content
        )

        if not success or not updated_message:
            logger.warning(
                "Failed to edit message",
                user_id=user_id,
                message_id=message_id,
            )
            raise BusinessLogicException(
                message="Failed to edit message",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
            )

        # Format message data
        message_data = {
            "id": message_id,
            "room_id": room_id,
            "content": updated_message.content,
            "updated_at": updated_message.updated_at.isoformat(),
            "is_edited": True,
        }

        # Send response
        await websocket.send_json(
            WebSocketResponse(type="message_edited", data=message_data).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(type="message_edited", data=message_data).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

        # Audit log
        await audit_service.log_event(
            event_type=AuditEventType.USER_UPDATED,
            user_id=user_id,
            resource_type="chat_message",
            resource_id=message_id,
            details={"room_id": room_id, "action": "edit_message"},
            level=AuditLogLevel.INFO,
        )

    # DELETE_MESSAGE command
    elif command.command == CommandType.DELETE_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")

        # Validate required fields
        if not room_id or not message_id:
            raise ValidationException(
                message="Room ID and message ID are required",
            )

        # Sanitize inputs
        room_id = sanitize_input(room_id)
        message_id = sanitize_input(message_id)

        # Check permission to delete message
        can_delete = await chat_service.check_message_permission(
            message_id=message_id, user_id=user_id, require_admin=False
        )

        if not can_delete:
            logger.warning(
                "Permission denied to delete message",
                user_id=user_id,
                message_id=message_id,
            )
            raise PermissionDeniedException(
                message="Permission denied to delete message",
                details={"message_id": message_id},
            )

        # Delete message
        success = await chat_service.delete_message(message_id)

        if not success:
            logger.warning(
                "Failed to delete message",
                user_id=user_id,
                message_id=message_id,
            )
            raise BusinessLogicException(
                message="Failed to delete message",
                code=ErrorCode.BUSINESS_LOGIC_ERROR,
            )

        # Send response
        await websocket.send_json(
            WebSocketResponse(
                type="message_deleted",
                data={"room_id": room_id, "message_id": message_id},
            ).dict()
        )

        # Broadcast to other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="message_deleted",
                data={"room_id": room_id, "message_id": message_id},
            ).dict(),
            room_id=room_id,
            exclude=connection_id,
        )

        # Audit log
        await audit_service.log_event(
            event_type=AuditEventType.USER_DELETED,
            user_id=user_id,
            resource_type="chat_message",
            resource_id=message_id,
            details={"room_id": room_id, "action": "delete_message"},
            level=AuditLogLevel.INFO,
        )

    # Unknown command
    else:
        logger.warning(
            "Unknown command received",
            command=command.command,
            user_id=user_id,
        )
        raise ValidationException(
            message=f"Unknown command: {command.command}",
        )
