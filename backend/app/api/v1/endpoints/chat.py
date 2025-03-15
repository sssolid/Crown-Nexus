# backend/app/api/v1/endpoints/chat.py
"""
Chat system REST API endpoints.

This module provides HTTP endpoints for the chat system:
- Room management (create, list, get details)
- Member management (add, remove, update)
- Message retrieval and search
- Chat history and export

These endpoints complement the WebSocket interface for chat functionality.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.chat.schemas import ChatRoomSchema, ChatMessageSchema, ChatMemberSchema
from app.chat.service import ChatService
from app.db.session import get_db_context
from app.models.chat import ChatRoom, ChatMember, ChatMemberRole, ChatRoomType
from app.models.user import User


router = APIRouter()
logger = logging.getLogger(__name__)


class CreateRoomRequest(BaseModel):
    """Request model for creating a room."""
    name: Optional[str] = None
    type: str
    company_id: Optional[str] = None
    members: Optional[List[Dict[str, Any]]] = None
    
    @validator('type')
    def validate_type(cls, v: str) -> str:
        """Validate room type."""
        valid_types = [t.value for t in ChatRoomType]
        if v not in valid_types:
            raise ValueError(f"Invalid room type. Must be one of: {', '.join(valid_types)}")
        return v


class AddMemberRequest(BaseModel):
    """Request model for adding a member to a room."""
    user_id: str
    role: str = "member"
    
    @validator('role')
    def validate_role(cls, v: str) -> str:
        """Validate member role."""
        valid_roles = [r.value for r in ChatMemberRole]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v


class UpdateMemberRequest(BaseModel):
    """Request model for updating a member in a room."""
    role: str
    
    @validator('role')
    def validate_role(cls, v: str) -> str:
        """Validate member role."""
        valid_roles = [r.value for r in ChatMemberRole]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v


class CreateDirectChatRequest(BaseModel):
    """Request model for creating a direct chat."""
    user_id: str


@router.post("/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(
    request: CreateRoomRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Create a new chat room.
    
    Args:
        request: Room creation request
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Created room information
    """
    chat_service = ChatService(db)
    
    try:
        room = await chat_service.create_room(
            name=request.name,
            room_type=request.type,
            creator_id=str(current_user.id),
            company_id=request.company_id,
            members=request.members
        )
        
        # Get room info
        room_info = await chat_service.get_room_info(str(room.id))
        
        return {
            "success": True,
            "room": room_info
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error creating room: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating room"
        )


@router.get("/rooms")
async def get_rooms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get all rooms for the current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: List of rooms
    """
    chat_service = ChatService(db)
    
    try:
        rooms = await chat_service.get_user_rooms(str(current_user.id))
        
        return {
            "success": True,
            "rooms": rooms
        }
    except Exception as e:
        logger.exception(f"Error getting rooms: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting rooms"
        )


@router.get("/rooms/{room_id}")
async def get_room(
    room_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get information about a specific room.
    
    Args:
        room_id: Room ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Room information
    """
    chat_service = ChatService(db)
    
    # Check if user has access to the room
    has_access = await chat_service.check_room_access(str(current_user.id), room_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to room"
        )
    
    try:
        room_info = await chat_service.get_room_info(room_id)
        
        if not room_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        return {
            "success": True,
            "room": room_info
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting room: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting room"
        )


@router.post("/rooms/{room_id}/members")
async def add_room_member(
    room_id: str,
    request: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Add a member to a room.
    
    Args:
        room_id: Room ID
        request: Member addition request
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success response
    """
    chat_service = ChatService(db)
    
    # Check if user has admin access to the room
    # First verify user is a member
    has_access = await chat_service.check_room_access(str(current_user.id), room_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to room"
        )
    
    # Then check if user is admin or owner
    room = await chat_service.get_room_with_members(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    is_admin = False
    for member in room.members:
        if member.user_id == current_user.id and member.is_active:
            if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                is_admin = True
                break
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can add members"
        )
    
    try:
        success = await chat_service.add_member(
            room_id=room_id,
            user_id=request.user_id,
            role=ChatMemberRole(request.role)
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add member"
            )
        
        return {
            "success": True,
            "message": "Member added successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error adding member: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding member"
        )


@router.put("/rooms/{room_id}/members/{user_id}")
async def update_room_member(
    room_id: str,
    user_id: str,
    request: UpdateMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Update a member's role in a room.
    
    Args:
        room_id: Room ID
        user_id: User ID
        request: Member update request
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success response
    """
    chat_service = ChatService(db)
    
    # Check if user has admin access to the room
    room = await chat_service.get_room_with_members(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Verify current user is admin or owner
    is_admin = False
    current_user_role = None
    for member in room.members:
        if member.user_id == current_user.id and member.is_active:
            current_user_role = member.role
            if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                is_admin = True
                break
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update member roles"
        )
    
    # Find target member
    target_member = None
    for member in room.members:
        if str(member.user_id) == user_id and member.is_active:
            target_member = member
            break
    
    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Prevent role escalation (only owners can create owners)
    if request.role == ChatMemberRole.OWNER and current_user_role != ChatMemberRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can create new owners"
        )
    
    try:
        success = await chat_service.update_member_role(
            room_id=room_id,
            user_id=user_id,
            role=ChatMemberRole(request.role)
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update member role"
            )
        
        return {
            "success": True,
            "message": "Member role updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating member role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating member role"
        )


@router.delete("/rooms/{room_id}/members/{user_id}")
async def remove_room_member(
    room_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Remove a member from a room.
    
    Args:
        room_id: Room ID
        user_id: User ID
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Success response
    """
    chat_service = ChatService(db)
    
    # Check if user has admin access to the room
    room = await chat_service.get_room_with_members(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Allow users to remove themselves
    if str(current_user.id) == user_id:
        try:
            success = await chat_service.remove_member(
                room_id=room_id,
                user_id=user_id
            )
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to leave room"
                )
            
            return {
                "success": True,
                "message": "Left room successfully"
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Error leaving room: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error leaving room"
            )
    
    # Otherwise, verify current user is admin or owner
    is_admin = False
    for member in room.members:
        if member.user_id == current_user.id and member.is_active:
            if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                is_admin = True
                break
    
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can remove members"
        )
    
    # Find target member
    target_member = None
    for member in room.members:
        if str(member.user_id) == user_id and member.is_active:
            target_member = member
            break
    
    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Prevent removing owners (only other owners can)
    if target_member.role == ChatMemberRole.OWNER:
        # Check if current user is also an owner
        current_is_owner = False
        for member in room.members:
            if member.user_id == current_user.id and member.role == ChatMemberRole.OWNER:
                current_is_owner = True
                break
        
        if not current_is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only owners can remove other owners"
            )
    
    try:
        success = await chat_service.remove_member(
            room_id=room_id,
            user_id=user_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove member"
            )
        
        return {
            "success": True,
            "message": "Member removed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error removing member: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing member"
        )


@router.get("/rooms/{room_id}/messages")
async def get_room_messages(
    room_id: str,
    before_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get messages from a room.
    
    Args:
        room_id: Room ID
        before_id: Get messages before this ID (for pagination)
        limit: Maximum number of messages to return
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: List of messages
    """
    chat_service = ChatService(db)
    
    # Check if user has access to the room
    has_access = await chat_service.check_room_access(str(current_user.id), room_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to room"
        )
    
    try:
        messages = await chat_service.get_message_history(
            room_id=room_id,
            before_id=before_id,
            limit=limit
        )
        
        return {
            "success": True,
            "messages": messages
        }
    except Exception as e:
        logger.exception(f"Error getting messages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting messages"
        )


@router.post("/direct-chats")
async def create_direct_chat(
    request: CreateDirectChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Create or get a direct chat with another user.
    
    Args:
        request: Direct chat creation request
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Direct chat information
    """
    chat_service = ChatService(db)
    
    # Check if target user exists
    from sqlalchemy import select
    from app.models.user import User
    
    query = select(User).where(User.id == request.user_id)
    result = await db.execute(query)
    target_user = result.scalar_one_or_none()
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # Try to find existing direct chat
        room_id = await chat_service.find_direct_chat(
            user_id1=str(current_user.id),
            user_id2=request.user_id
        )
        
        # If not found, create a new one
        if not room_id:
            room_id = await chat_service.create_direct_chat(
                user_id1=str(current_user.id),
                user_id2=request.user_id
            )
        
        # Get room info
        room_info = await chat_service.get_room_info(room_id)
        
        return {
            "success": True,
            "room": room_info
        }
    except Exception as e:
        logger.exception(f"Error creating/getting direct chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating/getting direct chat"
        )
