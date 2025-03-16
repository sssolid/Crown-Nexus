from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, validator
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.api.responses import created_response, error_response, success_response
from app.core.exceptions import AuthenticationException, BusinessLogicException, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger, log_execution_time
from app.db.session import AsyncSession
from app.models.chat import ChatMember, ChatMemberRole, ChatRoom, ChatRoomType, MessageType
from app.models.user import User
from app.services import get_chat_service
from app.schemas.responses import Response
router = APIRouter()
logger = get_logger('app.api.v1.endpoints.chat')
class CreateRoomRequest(BaseModel):
    name: Optional[str] = Field(None, description='Name of the chat room')
    type: str = Field(..., description='Type of chat room (direct, group, company)')
    company_id: Optional[str] = Field(None, description='Company ID (required for company rooms)')
    members: Optional[List[Dict[str, Any]]] = Field(None, description='List of members to add to the room')
    @validator('type')
    def validate_type(cls, v: str) -> str:
        valid_types = [t.value for t in ChatRoomType]
        if v not in valid_types:
            raise ValueError(f"Invalid room type. Must be one of: {', '.join(valid_types)}")
        return v
class AddMemberRequest(BaseModel):
    user_id: str = Field(..., description='ID of the user to add to the room')
    role: str = Field('member', description='Role of the user in the room (member, admin, owner)')
    @validator('role')
    def validate_role(cls, v: str) -> str:
        valid_roles = [r.value for r in ChatMemberRole]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v
class UpdateMemberRequest(BaseModel):
    role: str = Field(..., description='New role for the member')
    @validator('role')
    def validate_role(cls, v: str) -> str:
        valid_roles = [r.value for r in ChatMemberRole]
        if v not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        return v
class CreateDirectChatRequest(BaseModel):
    user_id: str = Field(..., description='ID of the user to chat with')
class CreateMessageRequest(BaseModel):
    content: str = Field(..., description='Message content')
    message_type: str = Field(MessageType.TEXT.value, description='Type of message (text, image, file, etc.)')
    metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional metadata for the message')
    @validator('message_type')
    def validate_message_type(cls, v: str) -> str:
        valid_types = [t.value for t in MessageType]
        if v not in valid_types:
            raise ValueError(f"Invalid message type. Must be one of: {', '.join(valid_types)}")
        return v
class EditMessageRequest(BaseModel):
    content: str = Field(..., description='New message content')
class ReactionRequest(BaseModel):
    reaction: str = Field(..., description='Reaction emoji or code')
@router.post('/rooms', status_code=status.HTTP_201_CREATED)
@log_execution_time(logger)
async def create_room(request: CreateRoomRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Creating chat room', user_id=str(current_user.id), room_type=request.type, company_id=request.company_id)
        room = await chat_service.create_room(name=request.name, room_type=request.type, creator_id=str(current_user.id), company_id=request.company_id, members=request.members)
        room_info = await chat_service.get_room_info(str(room.id))
        logger.info('Chat room created successfully', user_id=str(current_user.id), room_id=str(room.id), room_type=request.type)
        return created_response(data={'room': room_info}, message='Chat room created successfully')
    except ValidationException as e:
        logger.warning('Chat room creation validation failed', user_id=str(current_user.id), error=str(e), room_type=request.type)
        return error_response(message=str(e), code=status.HTTP_400_BAD_REQUEST)
    except BusinessLogicException as e:
        logger.error('Chat room creation failed', user_id=str(current_user.id), error=str(e), room_type=request.type, exc_info=True)
        return error_response(message='Failed to create chat room', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.get('/rooms')
@log_execution_time(logger)
async def get_rooms(db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Fetching user rooms', user_id=str(current_user.id))
        rooms = await chat_service.get_user_rooms(str(current_user.id))
        logger.info('User rooms fetched successfully', user_id=str(current_user.id), room_count=len(rooms))
        return success_response(data={'rooms': rooms}, message='Rooms retrieved successfully')
    except BusinessLogicException as e:
        logger.error('Failed to get user rooms', user_id=str(current_user.id), error=str(e), exc_info=True)
        return error_response(message='Failed to retrieve chat rooms', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.get('/rooms/{room_id}')
@log_execution_time(logger)
async def get_room(room_id: str, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Fetching room details', user_id=str(current_user.id), room_id=room_id)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        room_info = await chat_service.get_room_info(room_id)
        if not room_info:
            logger.warning('Room not found', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Room not found', code=status.HTTP_404_NOT_FOUND)
        logger.info('Room details fetched successfully', user_id=str(current_user.id), room_id=room_id)
        return success_response(data={'room': room_info}, message='Room retrieved successfully')
    except BusinessLogicException as e:
        logger.error('Failed to get room details', user_id=str(current_user.id), room_id=room_id, error=str(e), exc_info=True)
        return error_response(message='Failed to retrieve room details', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.post('/rooms/{room_id}/members')
@log_execution_time(logger)
async def add_room_member(room_id: str, request: AddMemberRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Adding member to room', user_id=str(current_user.id), room_id=room_id, target_user_id=request.user_id, role=request.role)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        room = await chat_service.get_room_with_members(room_id)
        if not room:
            logger.warning('Room not found', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Room not found', code=status.HTTP_404_NOT_FOUND)
        is_admin = False
        for member in room.members:
            if member.user_id == current_user.id and member.is_active:
                if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                    is_admin = True
                    break
        if not is_admin:
            logger.warning('Permission denied - only admins can add members', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Only admins can add members', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.add_member(room_id=room_id, user_id=request.user_id, role=ChatMemberRole(request.role))
        if not success:
            logger.error('Failed to add member to room', user_id=str(current_user.id), room_id=room_id, target_user_id=request.user_id)
            return error_response(message='Failed to add member', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Member added to room successfully', user_id=str(current_user.id), room_id=room_id, target_user_id=request.user_id, role=request.role)
        return success_response(message='Member added successfully')
    except ValidationException as e:
        logger.warning('Member addition validation failed', user_id=str(current_user.id), room_id=room_id, target_user_id=request.user_id, error=str(e))
        return error_response(message=str(e), code=status.HTTP_400_BAD_REQUEST)
    except BusinessLogicException as e:
        logger.error('Member addition failed', user_id=str(current_user.id), room_id=room_id, target_user_id=request.user_id, error=str(e), exc_info=True)
        return error_response(message='Failed to add member', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.put('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def update_room_member(room_id: str, user_id: str, request: UpdateMemberRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Updating member role', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id, new_role=request.role)
        room = await chat_service.get_room_with_members(room_id)
        if not room:
            logger.warning('Room not found', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Room not found', code=status.HTTP_404_NOT_FOUND)
        is_admin = False
        current_user_role = None
        for member in room.members:
            if member.user_id == current_user.id and member.is_active:
                current_user_role = member.role
                if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                    is_admin = True
                    break
        if not is_admin:
            logger.warning('Permission denied - only admins can update member roles', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Only admins can update member roles', code=status.HTTP_403_FORBIDDEN)
        target_member = None
        for member in room.members:
            if str(member.user_id) == user_id and member.is_active:
                target_member = member
                break
        if not target_member:
            logger.warning('Target member not found', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
            return error_response(message='Member not found', code=status.HTTP_404_NOT_FOUND)
        if request.role == ChatMemberRole.OWNER.value and current_user_role != ChatMemberRole.OWNER:
            logger.warning('Permission denied - only owners can create new owners', user_id=str(current_user.id), room_id=room_id, current_role=current_user_role)
            return error_response(message='Only owners can create new owners', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.update_member_role(room_id=room_id, user_id=user_id, role=ChatMemberRole(request.role))
        if not success:
            logger.error('Failed to update member role', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
            return error_response(message='Failed to update member role', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Member role updated successfully', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id, new_role=request.role)
        return success_response(message='Member role updated successfully')
    except ValidationException as e:
        logger.warning('Member role update validation failed', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id, error=str(e))
        return error_response(message=str(e), code=status.HTTP_400_BAD_REQUEST)
    except BusinessLogicException as e:
        logger.error('Member role update failed', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id, error=str(e), exc_info=True)
        return error_response(message='Failed to update member role', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.delete('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def remove_room_member(room_id: str, user_id: str, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Removing member from room', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
        room = await chat_service.get_room_with_members(room_id)
        if not room:
            logger.warning('Room not found', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Room not found', code=status.HTTP_404_NOT_FOUND)
        if str(current_user.id) == user_id:
            logger.info('User leaving room', user_id=str(current_user.id), room_id=room_id)
            success = await chat_service.remove_member(room_id=room_id, user_id=user_id)
            if not success:
                logger.error('Failed to leave room', user_id=str(current_user.id), room_id=room_id)
                return error_response(message='Failed to leave room', code=status.HTTP_400_BAD_REQUEST)
            logger.info('User left room successfully', user_id=str(current_user.id), room_id=room_id)
            return success_response(message='Left room successfully')
        is_admin = False
        for member in room.members:
            if member.user_id == current_user.id and member.is_active:
                if member.role in [ChatMemberRole.ADMIN, ChatMemberRole.OWNER]:
                    is_admin = True
                    break
        if not is_admin:
            logger.warning('Permission denied - only admins can remove members', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
            return error_response(message='Only admins can remove members', code=status.HTTP_403_FORBIDDEN)
        target_member = None
        for member in room.members:
            if str(member.user_id) == user_id and member.is_active:
                target_member = member
                break
        if not target_member:
            logger.warning('Target member not found', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
            return error_response(message='Member not found', code=status.HTTP_404_NOT_FOUND)
        if target_member.role == ChatMemberRole.OWNER:
            current_is_owner = False
            for member in room.members:
                if member.user_id == current_user.id and member.role == ChatMemberRole.OWNER:
                    current_is_owner = True
                    break
            if not current_is_owner:
                logger.warning('Permission denied - only owners can remove other owners', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
                return error_response(message='Only owners can remove other owners', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.remove_member(room_id=room_id, user_id=user_id)
        if not success:
            logger.error('Failed to remove member', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
            return error_response(message='Failed to remove member', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Member removed successfully', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id)
        return success_response(message='Member removed successfully')
    except BusinessLogicException as e:
        logger.error('Member removal failed', user_id=str(current_user.id), room_id=room_id, target_user_id=user_id, error=str(e), exc_info=True)
        return error_response(message='Failed to remove member', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.get('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def get_room_messages(room_id: str, before_id: Optional[str]=None, limit: int=Query(50, ge=1, le=100), db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Fetching room messages', user_id=str(current_user.id), room_id=room_id, before_id=before_id, limit=limit)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        messages = await chat_service.get_message_history(room_id=room_id, before_id=before_id, limit=limit)
        logger.info('Room messages fetched successfully', user_id=str(current_user.id), room_id=room_id, message_count=len(messages))
        return success_response(data={'messages': messages}, message='Messages retrieved successfully')
    except BusinessLogicException as e:
        logger.error('Failed to get room messages', user_id=str(current_user.id), room_id=room_id, error=str(e), exc_info=True)
        return error_response(message='Failed to retrieve messages', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.post('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def create_message(room_id: str, request: CreateMessageRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Creating message', user_id=str(current_user.id), room_id=room_id, message_type=request.message_type)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        message = await chat_service.create_message(room_id=room_id, sender_id=str(current_user.id), content=request.content, message_type=request.message_type, metadata=request.metadata)
        logger.info('Message created successfully', user_id=str(current_user.id), room_id=room_id, message_id=str(message.id))
        message_data = {'id': str(message.id), 'room_id': room_id, 'sender_id': str(current_user.id), 'sender_name': current_user.full_name, 'message_type': message.message_type, 'content': message.content, 'created_at': message.created_at.isoformat(), 'updated_at': message.updated_at.isoformat(), 'metadata': message.metadata, 'reactions': {}, 'is_deleted': False}
        return created_response(data={'message': message_data}, message='Message sent successfully')
    except ValidationException as e:
        logger.warning('Message creation validation failed', user_id=str(current_user.id), room_id=room_id, error=str(e))
        return error_response(message=str(e), code=status.HTTP_400_BAD_REQUEST)
    except BusinessLogicException as e:
        logger.error('Message creation failed', user_id=str(current_user.id), room_id=room_id, error=str(e), exc_info=True)
        return error_response(message='Failed to send message', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.put('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def edit_message(room_id: str, message_id: str, request: EditMessageRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Editing message', user_id=str(current_user.id), room_id=room_id, message_id=message_id)
        can_edit = await chat_service.check_message_permission(message_id=message_id, user_id=str(current_user.id))
        if not can_edit:
            logger.warning('Permission denied to edit message', user_id=str(current_user.id), message_id=message_id)
            return error_response(message='Permission denied to edit message', code=status.HTTP_403_FORBIDDEN)
        success, updated_message = await chat_service.edit_message(message_id=message_id, content=request.content)
        if not success or not updated_message:
            logger.error('Failed to edit message', user_id=str(current_user.id), message_id=message_id)
            return error_response(message='Failed to edit message', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Message edited successfully', user_id=str(current_user.id), message_id=message_id)
        message_data = {'id': str(updated_message.id), 'room_id': room_id, 'content': updated_message.content, 'updated_at': updated_message.updated_at.isoformat(), 'is_edited': True}
        return success_response(data={'message': message_data}, message='Message edited successfully')
    except ValidationException as e:
        logger.warning('Message edit validation failed', user_id=str(current_user.id), message_id=message_id, error=str(e))
        return error_response(message=str(e), code=status.HTTP_400_BAD_REQUEST)
    except BusinessLogicException as e:
        logger.error('Message edit failed', user_id=str(current_user.id), message_id=message_id, error=str(e), exc_info=True)
        return error_response(message='Failed to edit message', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.delete('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def delete_message(room_id: str, message_id: str, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Deleting message', user_id=str(current_user.id), room_id=room_id, message_id=message_id)
        can_delete = await chat_service.check_message_permission(message_id=message_id, user_id=str(current_user.id), require_admin=False)
        if not can_delete:
            logger.warning('Permission denied to delete message', user_id=str(current_user.id), message_id=message_id)
            return error_response(message='Permission denied to delete message', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.delete_message(message_id)
        if not success:
            logger.error('Failed to delete message', user_id=str(current_user.id), message_id=message_id)
            return error_response(message='Failed to delete message', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Message deleted successfully', user_id=str(current_user.id), message_id=message_id)
        return success_response(message='Message deleted successfully')
    except BusinessLogicException as e:
        logger.error('Message deletion failed', user_id=str(current_user.id), message_id=message_id, error=str(e), exc_info=True)
        return error_response(message='Failed to delete message', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.post('/rooms/{room_id}/messages/{message_id}/reactions')
@log_execution_time(logger)
async def add_reaction(room_id: str, message_id: str, request: ReactionRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Adding reaction to message', user_id=str(current_user.id), room_id=room_id, message_id=message_id, reaction=request.reaction)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.add_reaction(message_id=message_id, user_id=str(current_user.id), reaction=request.reaction)
        if not success:
            logger.error('Failed to add reaction', user_id=str(current_user.id), message_id=message_id, reaction=request.reaction)
            return error_response(message='Failed to add reaction', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Reaction added successfully', user_id=str(current_user.id), message_id=message_id, reaction=request.reaction)
        return success_response(data={'message_id': message_id, 'reaction': request.reaction, 'user_id': str(current_user.id)}, message='Reaction added successfully')
    except BusinessLogicException as e:
        logger.error('Adding reaction failed', user_id=str(current_user.id), message_id=message_id, reaction=request.reaction, error=str(e), exc_info=True)
        return error_response(message='Failed to add reaction', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.delete('/rooms/{room_id}/messages/{message_id}/reactions/{reaction}')
@log_execution_time(logger)
async def remove_reaction(room_id: str, message_id: str, reaction: str, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Removing reaction from message', user_id=str(current_user.id), room_id=room_id, message_id=message_id, reaction=reaction)
        has_access = await chat_service.check_room_access(str(current_user.id), room_id)
        if not has_access:
            logger.warning('Access denied to room', user_id=str(current_user.id), room_id=room_id)
            return error_response(message='Access denied to room', code=status.HTTP_403_FORBIDDEN)
        success = await chat_service.remove_reaction(message_id=message_id, user_id=str(current_user.id), reaction=reaction)
        if not success:
            logger.error('Failed to remove reaction', user_id=str(current_user.id), message_id=message_id, reaction=reaction)
            return error_response(message='Failed to remove reaction', code=status.HTTP_400_BAD_REQUEST)
        logger.info('Reaction removed successfully', user_id=str(current_user.id), message_id=message_id, reaction=reaction)
        return success_response(message='Reaction removed successfully')
    except BusinessLogicException as e:
        logger.error('Removing reaction failed', user_id=str(current_user.id), message_id=message_id, reaction=reaction, error=str(e), exc_info=True)
        return error_response(message='Failed to remove reaction', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
@router.post('/direct-chats')
@log_execution_time(logger)
async def create_direct_chat(request: CreateDirectChatRequest, db: AsyncSession=Depends(get_db), current_user: User=Depends(get_current_active_user)) -> Response:
    chat_service = get_chat_service(db)
    try:
        logger.info('Creating/getting direct chat', user_id=str(current_user.id), target_user_id=request.user_id)
        from sqlalchemy import select
        from app.models.user import User
        query = select(User).where(User.id == request.user_id)
        result = await db.execute(query)
        target_user = result.scalar_one_or_none()
        if not target_user:
            logger.warning('Target user not found', user_id=str(current_user.id), target_user_id=request.user_id)
            return error_response(message='User not found', code=status.HTTP_404_NOT_FOUND)
        room_id = await chat_service.find_direct_chat(user_id1=str(current_user.id), user_id2=request.user_id)
        if not room_id:
            room_id = await chat_service.create_direct_chat(user_id1=str(current_user.id), user_id2=request.user_id)
        room_info = await chat_service.get_room_info(room_id)
        logger.info('Direct chat found/created successfully', user_id=str(current_user.id), target_user_id=request.user_id, room_id=room_id)
        return success_response(data={'room': room_info}, message='Direct chat retrieved successfully')
    except BusinessLogicException as e:
        logger.error('Direct chat creation/retrieval failed', user_id=str(current_user.id), target_user_id=request.user_id, error=str(e), exc_info=True)
        return error_response(message='Failed to create/get direct chat', code=status.HTTP_500_INTERNAL_SERVER_ERROR)