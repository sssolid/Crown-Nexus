from __future__ import annotations
import asyncio
import json
import logging
from typing import Dict, List, Optional, Set, Union
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from app.chat.schemas import WebSocketCommand
from app.utils.redis_manager import get_redis_pool
logger = logging.getLogger(__name__)
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, WebSocket] = {}
        self.room_connections: Dict[str, Set[str]] = {}
        self.user_connection_ids: Dict[str, Set[str]] = {}
        self.connection_user_ids: Dict[str, str] = {}
    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str) -> None:
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        if user_id not in self.user_connection_ids:
            self.user_connection_ids[user_id] = set()
        self.user_connection_ids[user_id].add(connection_id)
        self.connection_user_ids[connection_id] = user_id
        logger.info(f'WebSocket connected: {connection_id} for user {user_id}')
    def disconnect(self, connection_id: str) -> None:
        if connection_id in self.active_connections:
            user_id = self.connection_user_ids.get(connection_id)
            del self.active_connections[connection_id]
            for room_id, connections in self.room_connections.items():
                if connection_id in connections:
                    connections.remove(connection_id)
                    if not connections:
                        del self.room_connections[room_id]
            if user_id and user_id in self.user_connection_ids:
                if connection_id in self.user_connection_ids[user_id]:
                    self.user_connection_ids[user_id].remove(connection_id)
                if not self.user_connection_ids[user_id]:
                    del self.user_connection_ids[user_id]
            if connection_id in self.connection_user_ids:
                del self.connection_user_ids[connection_id]
            logger.info(f'WebSocket disconnected: {connection_id}')
    def join_room(self, connection_id: str, room_id: str) -> None:
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(connection_id)
        logger.debug(f'Connection {connection_id} joined room {room_id}')
    def leave_room(self, connection_id: str, room_id: str) -> None:
        if room_id in self.room_connections and connection_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(connection_id)
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]
            logger.debug(f'Connection {connection_id} left room {room_id}')
    async def send_personal_message(self, message: dict, connection_id: str) -> None:
        if connection_id in self.active_connections:
            await self.active_connections[connection_id].send_json(message)
            logger.debug(f'Sent message to connection {connection_id}')
    async def broadcast_to_room(self, message: dict, room_id: str, exclude: Optional[str]=None) -> None:
        if room_id in self.room_connections:
            for connection_id in self.room_connections[room_id]:
                if connection_id != exclude and connection_id in self.active_connections:
                    await self.active_connections[connection_id].send_json(message)
            logger.debug(f"Broadcast message to room {room_id} (excluding {(exclude if exclude else 'none')})")
    async def broadcast_to_user(self, message: dict, user_id: str) -> None:
        if user_id in self.user_connection_ids:
            for connection_id in self.user_connection_ids[user_id]:
                if connection_id in self.active_connections:
                    await self.active_connections[connection_id].send_json(message)
            logger.debug(f'Broadcast message to user {user_id}')
    def get_connection_count(self) -> int:
        return len(self.active_connections)
    def get_room_connection_count(self, room_id: str) -> int:
        if room_id in self.room_connections:
            return len(self.room_connections[room_id])
        return 0
    def get_user_connection_count(self, user_id: str) -> int:
        if user_id in self.user_connection_ids:
            return len(self.user_connection_ids[user_id])
        return 0
manager = ConnectionManager()
class RedisConnectionManager:
    def __init__(self, local_manager: ConnectionManager) -> None:
        self.local_manager = local_manager
        self.redis_pubsub_channel = 'chat:messages'
        self._pubsub_task = None
    async def start_pubsub_listener(self) -> None:
        if self._pubsub_task is None:
            self._pubsub_task = asyncio.create_task(self._listen_to_redis())
    async def _listen_to_redis(self) -> None:
        try:
            redis_pool = await get_redis_pool()
            async with redis_pool.client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe(self.redis_pubsub_channel)
                logger.info('Started Redis Pub/Sub listener for chat messages')
                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            data = json.loads(message['data'])
                            if data.get('type') == 'room_message':
                                await self.local_manager.broadcast_to_room(message=data['message'], room_id=data['room_id'], exclude=data.get('exclude'))
                            elif data.get('type') == 'user_message':
                                await self.local_manager.broadcast_to_user(message=data['message'], user_id=data['user_id'])
                        except (json.JSONDecodeError, KeyError) as e:
                            logger.error(f'Error processing Redis message: {e}')
        except Exception as e:
            logger.error(f'Redis Pub/Sub listener error: {e}')
            await asyncio.sleep(5)
            self._pubsub_task = asyncio.create_task(self._listen_to_redis())
    async def broadcast_to_room(self, message: dict, room_id: str, exclude: Optional[str]=None) -> None:
        await self.local_manager.broadcast_to_room(message, room_id, exclude)
        redis_message = {'type': 'room_message', 'room_id': room_id, 'message': message, 'exclude': exclude}
        redis_pool = await get_redis_pool()
        async with redis_pool.client() as client:
            await client.publish(self.redis_pubsub_channel, json.dumps(redis_message))
    async def broadcast_to_user(self, message: dict, user_id: str) -> None:
        await self.local_manager.broadcast_to_user(message, user_id)
        redis_message = {'type': 'user_message', 'user_id': user_id, 'message': message}
        redis_pool = await get_redis_pool()
        async with redis_pool.client() as client:
            await client.publish(self.redis_pubsub_channel, json.dumps(redis_message))
redis_manager = RedisConnectionManager(manager)