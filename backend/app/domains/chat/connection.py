# backend/app/chat/connection.py
"""
WebSocket connection management.

This module manages WebSocket connections for the real-time chat system:
- Tracking active connections
- Sending messages to specific connections
- Broadcasting to multiple connections
- Connection authentication and validation

It provides the foundation for real-time communication in the chat system.
"""

from __future__ import annotations

import asyncio
import json
from typing import Dict, Optional, Set

from app.domains.chat.schemas import WebSocketCommand
from fastapi import WebSocket

from app.core.logging import get_logger
from app.utils.redis_manager import get_redis_pool

logger = get_logger("app.chat.connection")


class ConnectionManager:
    """
    WebSocket connection manager for the chat system.

    This class handles:
    - Active WebSocket connections
    - Connection groups by room ID
    - Message broadcasting
    - Connection authentication
    """

    def __init__(self) -> None:
        """Initialize the connection manager."""
        # All active connections
        self.active_connections: Dict[str, WebSocket] = {}
        # Connections by room_id
        self.room_connections: Dict[str, Set[str]] = {}
        # User to connection mapping
        self.user_connection_ids: Dict[str, Set[str]] = {}
        # Connection to user mapping
        self.connection_user_ids: Dict[str, str] = {}

    async def connect(
        self, websocket: WebSocket, connection_id: str, user_id: str
    ) -> None:
        """
        Accept a WebSocket connection and register it.

        Args:
            websocket: The WebSocket connection
            connection_id: Unique ID for this connection
            user_id: ID of the authenticated user
        """
        await websocket.accept()
        self.active_connections[connection_id] = websocket

        # Associate connection with user
        if user_id not in self.user_connection_ids:
            self.user_connection_ids[user_id] = set()
        self.user_connection_ids[user_id].add(connection_id)
        self.connection_user_ids[connection_id] = user_id

        logger.info(f"WebSocket connected: {connection_id} for user {user_id}")

    def disconnect(self, connection_id: str) -> None:
        """
        Remove a WebSocket connection.

        Args:
            connection_id: The ID of the connection to remove
        """
        if connection_id in self.active_connections:
            # Get user_id before removing connection
            user_id = self.connection_user_ids.get(connection_id)

            # Remove from active connections
            del self.active_connections[connection_id]

            # Remove from room connections
            for room_id, connections in self.room_connections.items():
                if connection_id in connections:
                    connections.remove(connection_id)
                    # Clean up empty room sets
                    if not connections:
                        del self.room_connections[room_id]

            # Remove from user mapping
            if user_id and user_id in self.user_connection_ids:
                if connection_id in self.user_connection_ids[user_id]:
                    self.user_connection_ids[user_id].remove(connection_id)
                # Clean up empty user sets
                if not self.user_connection_ids[user_id]:
                    del self.user_connection_ids[user_id]

            # Remove from connection to user mapping
            if connection_id in self.connection_user_ids:
                del self.connection_user_ids[connection_id]

            logger.info(f"WebSocket disconnected: {connection_id}")

    def join_room(self, connection_id: str, room_id: str) -> None:
        """
        Add a connection to a room group.

        Args:
            connection_id: The connection ID
            room_id: The room ID to join
        """
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(connection_id)
        logger.debug(f"Connection {connection_id} joined room {room_id}")

    def leave_room(self, connection_id: str, room_id: str) -> None:
        """
        Remove a connection from a room group.

        Args:
            connection_id: The connection ID
            room_id: The room ID to leave
        """
        if (
            room_id in self.room_connections
            and connection_id in self.room_connections[room_id]
        ):
            self.room_connections[room_id].remove(connection_id)
            # Clean up empty room sets
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]
            logger.debug(f"Connection {connection_id} left room {room_id}")

    async def send_personal_message(self, message: dict, connection_id: str) -> None:
        """
        Send a message to a specific connection.

        Args:
            message: The message data to send
            connection_id: The target connection ID
        """
        if connection_id in self.active_connections:
            await self.active_connections[connection_id].send_json(message)
            logger.debug(f"Sent message to connection {connection_id}")

    async def broadcast_to_room(
        self, message: dict, room_id: str, exclude: Optional[str] = None
    ) -> None:
        """
        Broadcast a message to all connections in a room.

        Args:
            message: The message data to send
            room_id: The room ID to broadcast to
            exclude: Optional connection ID to exclude from broadcast
        """
        if room_id in self.room_connections:
            for connection_id in self.room_connections[room_id]:
                if (
                    connection_id != exclude
                    and connection_id in self.active_connections
                ):
                    await self.active_connections[connection_id].send_json(message)
            logger.debug(
                f"Broadcast message to room {room_id} (excluding {exclude if exclude else 'none'})"
            )

    async def broadcast_to_user(self, message: dict, user_id: str) -> None:
        """
        Broadcast a message to all connections for a specific user.

        Args:
            message: The message data to send
            user_id: The user ID to broadcast to
        """
        if user_id in self.user_connection_ids:
            for connection_id in self.user_connection_ids[user_id]:
                if connection_id in self.active_connections:
                    await self.active_connections[connection_id].send_json(message)
            logger.debug(f"Broadcast message to user {user_id}")

    def get_connection_count(self) -> int:
        """
        Get the count of active connections.

        Returns:
            int: Number of active connections
        """
        return len(self.active_connections)

    def get_room_connection_count(self, room_id: str) -> int:
        """
        Get the count of connections in a specific room.

        Args:
            room_id: The room ID

        Returns:
            int: Number of connections in the room
        """
        if room_id in self.room_connections:
            return len(self.room_connections[room_id])
        return 0

    def get_user_connection_count(self, user_id: str) -> int:
        """
        Get the count of connections for a specific user.

        Args:
            user_id: The user ID

        Returns:
            int: Number of connections for the user
        """
        if user_id in self.user_connection_ids:
            return len(self.user_connection_ids[user_id])
        return 0


# Singleton connection manager instance
manager = ConnectionManager()


class RedisConnectionManager:
    """
    Redis-based connection manager for multi-instance scaling.

    This class extends the basic connection manager with Redis Pub/Sub
    to allow broadcasting messages across multiple application instances.
    """

    def __init__(self, local_manager: ConnectionManager) -> None:
        """
        Initialize the Redis connection manager.

        Args:
            local_manager: The local connection manager instance
        """
        self.local_manager = local_manager
        self.redis_pubsub_channel = "chat:messages"
        self._pubsub_task = None

    async def start_pubsub_listener(self) -> None:
        """Start the Redis Pub/Sub listener task."""
        if self._pubsub_task is None:
            self._pubsub_task = asyncio.create_task(self._listen_to_redis())

    async def _listen_to_redis(self) -> None:
        """Listen to Redis Pub/Sub messages and forward them to WebSocket clients."""
        try:
            redis_pool = await get_redis_pool()
            async with redis_pool.client() as client:
                pubsub = client.pubsub()
                await pubsub.subscribe(self.redis_pubsub_channel)

                logger.info("Started Redis Pub/Sub listener for chat messages")

                async for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])
                            # Handle different message types
                            if data.get("type") == "room_message":
                                await self.local_manager.broadcast_to_room(
                                    message=data["message"],
                                    room_id=data["room_id"],
                                    exclude=data.get("exclude"),
                                )
                            elif data.get("type") == "user_message":
                                await self.local_manager.broadcast_to_user(
                                    message=data["message"], user_id=data["user_id"]
                                )
                        except (json.JSONDecodeError, KeyError) as e:
                            logger.error(f"Error processing Redis message: {e}")
        except Exception as e:
            logger.error(f"Redis Pub/Sub listener error: {e}")
            # Restart the listener after a short delay
            await asyncio.sleep(5)
            self._pubsub_task = asyncio.create_task(self._listen_to_redis())

    async def broadcast_to_room(
        self, message: dict, room_id: str, exclude: Optional[str] = None
    ) -> None:
        """
        Broadcast a message to all connections in a room across all instances.

        Args:
            message: The message data to send
            room_id: The room ID to broadcast to
            exclude: Optional connection ID to exclude from broadcast
        """
        # Send to local connections
        await self.local_manager.broadcast_to_room(message, room_id, exclude)

        # Publish to Redis for other instances
        redis_message = {
            "type": "room_message",
            "room_id": room_id,
            "message": message,
            "exclude": exclude,
        }

        redis_pool = await get_redis_pool()
        async with redis_pool.client() as client:
            await client.publish(self.redis_pubsub_channel, json.dumps(redis_message))

    async def broadcast_to_user(self, message: dict, user_id: str) -> None:
        """
        Broadcast a message to all connections for a specific user across all instances.

        Args:
            message: The message data to send
            user_id: The user ID to broadcast to
        """
        # Send to local connections
        await self.local_manager.broadcast_to_user(message, user_id)

        # Publish to Redis for other instances
        redis_message = {"type": "user_message", "user_id": user_id, "message": message}

        redis_pool = await get_redis_pool()
        async with redis_pool.client() as client:
            await client.publish(self.redis_pubsub_channel, json.dumps(redis_message))


# Create Redis-enabled connection manager
redis_manager = RedisConnectionManager(manager)
