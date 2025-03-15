# backend/app/chat/websocket.py
"""
WebSocket handler for chat functionality.

This module provides the WebSocket endpoint and handler for real-time chat:
- WebSocket connections with authentication
- Message processing and routing
- Room management
- Presence tracking
- Error handling

It serves as the entry point for WebSocket connections in the chat system.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, cast

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_ws, get_db
from app.chat.connection import manager, redis_manager
from app.chat.schemas import (
    ChatMessageSchema, 
    CommandType, 
    MessageType,
    WebSocketCommand, 
    WebSocketResponse
)
from app.chat.service import ChatService
from app.db.session import get_db_context
from app.models.chat import ChatMessage, ChatRoom, ChatMember, ChatMemberRole
from app.models.user import User
from app.utils.redis_manager import rate_limit_check, set_key, get_key


router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
):
    """
    WebSocket endpoint for chat connections.
    
    This endpoint handles:
    - WebSocket connection setup
    - Authentication via JWT token
    - Command processing
    - Error handling and graceful disconnection
    
    Args:
        websocket: The WebSocket connection
        db: Database session
        current_user: The authenticated user
    """
    connection_id = str(uuid.uuid4())
    user_id = str(current_user.id)
    
    # Start Redis Pub/Sub listener if not already running
    await redis_manager.start_pubsub_listener()
    
    try:
        # Accept the connection
        await manager.connect(websocket, connection_id, user_id)
        
        # Set user as online
        online_key = f"user:online:{user_id}"
        await set_key(online_key, True, 300)  # 5 minutes TTL
        
        # Create chat service
        chat_service = ChatService(db)
        
        # Send welcome message
        await websocket.send_json(WebSocketResponse(
            type="connected",
            data={
                "user_id": user_id,
                "connection_id": connection_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        ).dict())
        
        # Send list of active rooms for this user
        user_rooms = await chat_service.get_user_rooms(current_user.id)
        await websocket.send_json(WebSocketResponse(
            type="room_list",
            data={
                "rooms": user_rooms
            }
        ).dict())
        
        # Process incoming messages
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                # Check rate limits
                is_limited, count = await rate_limit_check(
                    f"rate:ws:{user_id}", 
                    limit=50,  # 50 operations
                    window=60   # per minute
                )
                
                if is_limited:
                    logger.warning(f"Rate limit exceeded for user {user_id}: {count}")
                    await websocket.send_json(WebSocketResponse(
                        type="error",
                        success=False,
                        error="Rate limit exceeded"
                    ).dict())
                    continue
                
                # Parse command
                command_data = json.loads(data)
                command = WebSocketCommand(**command_data)
                
                # Process command based on type
                await process_command(
                    command=command,
                    websocket=websocket,
                    connection_id=connection_id,
                    user=current_user,
                    chat_service=chat_service
                )
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from client {connection_id}")
                await websocket.send_json(WebSocketResponse(
                    type="error",
                    success=False,
                    error="Invalid JSON"
                ).dict())
            
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                await websocket.send_json(WebSocketResponse(
                    type="error",
                    success=False,
                    error=f"Validation error: {str(e)}"
                ).dict())
            
            except Exception as e:
                logger.exception(f"Error processing message: {e}")
                await websocket.send_json(WebSocketResponse(
                    type="error",
                    success=False,
                    error="Internal server error"
                ).dict())
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
    
    finally:
        # Handle disconnection cleanup
        manager.disconnect(connection_id)
        
        # Update user's last seen timestamp
        last_seen_key = f"user:last_seen:{user_id}"
        await set_key(last_seen_key, datetime.utcnow().isoformat(), 86400)  # 24 hours TTL


async def process_command(
    command: WebSocketCommand,
    websocket: WebSocket,
    connection_id: str,
    user: User,
    chat_service: ChatService
) -> None:
    """
    Process a WebSocket command.
    
    This function handles different command types and routes them
    to the appropriate handler functions.
    
    Args:
        command: The command to process
        websocket: The WebSocket connection
        connection_id: ID of this connection
        user: The authenticated user
        chat_service: Chat service instance
    """
    user_id = str(user.id)
    
    # Process based on command type
    if command.command == CommandType.JOIN_ROOM:
        # Validate room access
        room_id = command.data.get("room_id") or command.room_id
        if not room_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID is required"
            ).dict())
            return
        
        # Check if user has access to the room
        has_access = await chat_service.check_room_access(str(user.id), room_id)
        if not has_access:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Access denied to room"
            ).dict())
            return
        
        # Join the room
        manager.join_room(connection_id, room_id)
        
        # Get room info
        room_info = await chat_service.get_room_info(room_id)
        
        # Notify user of successful join
        await websocket.send_json(WebSocketResponse(
            type="room_joined",
            data=room_info
        ).dict())
        
        # Notify other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_joined",
                data={
                    "room_id": room_id,
                    "user": {
                        "id": str(user.id),
                        "name": user.full_name
                    }
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.LEAVE_ROOM:
        room_id = command.data.get("room_id") or command.room_id
        if not room_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID is required"
            ).dict())
            return
        
        # Leave the room
        manager.leave_room(connection_id, room_id)
        
        # Notify user of successful leave
        await websocket.send_json(WebSocketResponse(
            type="room_left",
            data={"room_id": room_id}
        ).dict())
        
        # Notify other room members
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_left",
                data={
                    "room_id": room_id,
                    "user_id": str(user.id)
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.SEND_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        content = command.data.get("content")
        message_type = command.data.get("message_type", "text")
        
        if not room_id or not content:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID and content are required"
            ).dict())
            return
        
        # Check if user has access to the room
        has_access = await chat_service.check_room_access(str(user.id), room_id)
        if not has_access:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Access denied to room"
            ).dict())
            return
        
        # Filter content if needed
        filtered_content = await filter_message_content(content)
        
        # Create and save message
        message = await chat_service.create_message(
            room_id=room_id,
            sender_id=str(user.id),
            content=filtered_content,
            message_type=message_type,
            metadata=command.data.get("metadata", {})
        )
        
        # Format message for response
        message_data = {
            "id": str(message.id),
            "room_id": room_id,
            "sender_id": str(user.id),
            "sender_name": user.full_name,
            "message_type": message.message_type,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
            "metadata": message.metadata
        }
        
        # Send confirmation to sender
        await websocket.send_json(WebSocketResponse(
            type="message_sent",
            data=message_data
        ).dict())
        
        # Broadcast to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="new_message",
                data=message_data
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.READ_MESSAGES:
        room_id = command.data.get("room_id") or command.room_id
        last_read_id = command.data.get("last_read_id")
        
        if not room_id or not last_read_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID and last_read_id are required"
            ).dict())
            return
        
        # Update last read timestamp
        await chat_service.mark_as_read(str(user.id), room_id, last_read_id)
        
        # Send confirmation
        await websocket.send_json(WebSocketResponse(
            type="messages_read",
            data={
                "room_id": room_id,
                "last_read_id": last_read_id
            }
        ).dict())
    
    elif command.command == CommandType.TYPING_START:
        room_id = command.data.get("room_id") or command.room_id
        
        if not room_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID is required"
            ).dict())
            return
        
        # Broadcast typing indicator
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_typing",
                data={
                    "room_id": room_id,
                    "user_id": str(user.id),
                    "user_name": user.full_name
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.TYPING_STOP:
        room_id = command.data.get("room_id") or command.room_id
        
        if not room_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID is required"
            ).dict())
            return
        
        # Broadcast typing stopped
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="user_typing_stopped",
                data={
                    "room_id": room_id,
                    "user_id": str(user.id)
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.FETCH_HISTORY:
        room_id = command.data.get("room_id") or command.room_id
        before_id = command.data.get("before_id")
        limit = int(command.data.get("limit", 50))
        
        if not room_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID is required"
            ).dict())
            return
        
        # Check if user has access to the room
        has_access = await chat_service.check_room_access(str(user.id), room_id)
        if not has_access:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Access denied to room"
            ).dict())
            return
        
        # Get message history
        messages = await chat_service.get_message_history(room_id, before_id, limit)
        
        # Send message history
        await websocket.send_json(WebSocketResponse(
            type="message_history",
            data={
                "room_id": room_id,
                "messages": messages
            }
        ).dict())
    
    elif command.command == CommandType.ADD_REACTION:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        reaction = command.data.get("reaction")
        
        if not room_id or not message_id or not reaction:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID, message ID, and reaction are required"
            ).dict())
            return
        
        # Add reaction
        success = await chat_service.add_reaction(
            message_id=message_id,
            user_id=str(user.id),
            reaction=reaction
        )
        
        if not success:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Failed to add reaction"
            ).dict())
            return
        
        # Send confirmation
        await websocket.send_json(WebSocketResponse(
            type="reaction_added",
            data={
                "room_id": room_id,
                "message_id": message_id,
                "reaction": reaction,
                "user_id": str(user.id)
            }
        ).dict())
        
        # Broadcast to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="reaction_added",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": str(user.id),
                    "user_name": user.full_name
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.REMOVE_REACTION:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        reaction = command.data.get("reaction")
        
        if not room_id or not message_id or not reaction:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID, message ID, and reaction are required"
            ).dict())
            return
        
        # Remove reaction
        success = await chat_service.remove_reaction(
            message_id=message_id,
            user_id=str(user.id),
            reaction=reaction
        )
        
        if not success:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Failed to remove reaction"
            ).dict())
            return
        
        # Send confirmation
        await websocket.send_json(WebSocketResponse(
            type="reaction_removed",
            data={
                "room_id": room_id,
                "message_id": message_id,
                "reaction": reaction,
                "user_id": str(user.id)
            }
        ).dict())
        
        # Broadcast to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="reaction_removed",
                data={
                    "room_id": room_id,
                    "message_id": message_id,
                    "reaction": reaction,
                    "user_id": str(user.id)
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.EDIT_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        content = command.data.get("content")
        
        if not room_id or not message_id or not content:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID, message ID, and content are required"
            ).dict())
            return
        
        # Check if user can edit the message
        can_edit = await chat_service.check_message_permission(
            message_id=message_id,
            user_id=str(user.id)
        )
        
        if not can_edit:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Permission denied to edit message"
            ).dict())
            return
        
        # Filter content if needed
        filtered_content = await filter_message_content(content)
        
        # Edit message
        success, updated_message = await chat_service.edit_message(
            message_id=message_id,
            content=filtered_content
        )
        
        if not success or not updated_message:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Failed to edit message"
            ).dict())
            return
        
        # Format message for response
        message_data = {
            "id": str(updated_message.id),
            "room_id": room_id,
            "content": updated_message.content,
            "updated_at": updated_message.updated_at.isoformat(),
            "is_edited": True
        }
        
        # Send confirmation
        await websocket.send_json(WebSocketResponse(
            type="message_edited",
            data=message_data
        ).dict())
        
        # Broadcast to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="message_edited",
                data=message_data
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    elif command.command == CommandType.DELETE_MESSAGE:
        room_id = command.data.get("room_id") or command.room_id
        message_id = command.data.get("message_id")
        
        if not room_id or not message_id:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Room ID and message ID are required"
            ).dict())
            return
        
        # Check if user can delete the message
        can_delete = await chat_service.check_message_permission(
            message_id=message_id,
            user_id=str(user.id),
            require_admin=False  # Allow message owners to delete
        )
        
        if not can_delete:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Permission denied to delete message"
            ).dict())
            return
        
        # Delete message
        success = await chat_service.delete_message(message_id)
        
        if not success:
            await websocket.send_json(WebSocketResponse(
                type="error",
                success=False,
                error="Failed to delete message"
            ).dict())
            return
        
        # Send confirmation
        await websocket.send_json(WebSocketResponse(
            type="message_deleted",
            data={
                "room_id": room_id,
                "message_id": message_id
            }
        ).dict())
        
        # Broadcast to room
        await redis_manager.broadcast_to_room(
            message=WebSocketResponse(
                type="message_deleted",
                data={
                    "room_id": room_id,
                    "message_id": message_id
                }
            ).dict(),
            room_id=room_id,
            exclude=connection_id
        )
    
    else:
        # Unknown command
        await websocket.send_json(WebSocketResponse(
            type="error",
            success=False,
            error=f"Unknown command: {command.command}"
        ).dict())


async def filter_message_content(content: str) -> str:
    """
    Filter message content for prohibited content.
    
    Args:
        content: The message content to filter
        
    Returns:
        str: Filtered content
    """
    # Load prohibited words from Redis or a configuration file
    prohibited_words = await get_key("chat:prohibited_words", default=[])
    
    # Simple filtering - replace prohibited words with asterisks
    if prohibited_words:
        filtered = content
        for word in prohibited_words:
            replacement = '*' * len(word)
            filtered = filtered.replace(word, replacement)
        return filtered
    
    return content
