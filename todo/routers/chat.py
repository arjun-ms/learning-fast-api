from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlmodel import Session
from typing import List, Dict, Set
import json

from ..db.database import get_db
from ..db import models
from .. import auth

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Chat connection manager to handle multiple WebSocket connections
class ChatConnectionManager:
    def __init__(self):
        # Store active connections by room
        self.active_rooms: Dict[str, Dict[str, WebSocket]] = {}
        # Store user information
        self.connected_users: Dict[str, Dict] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        await websocket.accept()
        self.connected_users[user_id] = {
            "username": username,
            "websocket": websocket,
            "rooms": set()
        }
        
        # Send welcome message
        await self.send_personal_message(
            json.dumps({
                "type": "system",
                "content": f"Welcome {username}! You are now connected."
            }),
            websocket
        )
        
    def disconnect(self, user_id: str):
        if user_id in self.connected_users:
            # Get all rooms the user is in
            rooms = list(self.connected_users[user_id]["rooms"])
            
            # Leave all rooms
            for room_id in rooms:
                self.leave_room(user_id, room_id)
                
            # Remove user from connected users
            del self.connected_users[user_id]
    
    async def join_room(self, user_id: str, room_id: str):
        if user_id not in self.connected_users:
            return False
        
        # Create room if it doesn't exist
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = {}
        
        # Add user to room
        username = self.connected_users[user_id]["username"]
        self.active_rooms[room_id][user_id] = self.connected_users[user_id]["websocket"]
        self.connected_users[user_id]["rooms"].add(room_id)
        
        # Notify everyone in the room about the new user
        await self.broadcast_to_room(
            room_id,
            json.dumps({
                "type": "system",
                "content": f"{username} has joined the room",
                "username": username,
                "room": room_id
            })
        )
        
        return True
        
    async def leave_room(self, user_id: str, room_id: str):
        if user_id in self.connected_users and room_id in self.active_rooms:
            if user_id in self.active_rooms[room_id]:
                # Remove user from room
                username = self.connected_users[user_id]["username"]
                del self.active_rooms[room_id][user_id]
                self.connected_users[user_id]["rooms"].remove(room_id)
                
                # Remove room if empty
                if not self.active_rooms[room_id]:
                    del self.active_rooms[room_id]
                else:
                    # Notify others that user left
                    await self.broadcast_to_room(
                        room_id,
                        json.dumps({
                            "type": "system",
                            "content": f"{username} has left the room",
                            "username": username,
                            "room": room_id
                        })
                    )
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def broadcast_to_room(self, room_id: str, message: str):
        if room_id in self.active_rooms:
            for connection in self.active_rooms[room_id].values():
                await connection.send_text(message)
    
    def get_rooms(self):
        return list(self.active_rooms.keys())
    
    def get_room_participants(self, room_id: str):
        if room_id in self.active_rooms:
            return [
                {
                    "user_id": user_id,
                    "username": self.connected_users[user_id]["username"]
                }
                for user_id in self.active_rooms[room_id]
            ]
        return []

# Create a connection manager instance
chat_manager = ChatConnectionManager()

# Chat WebSocket endpoint
@router.websocket("/ws")
async def chat_websocket(
    websocket: WebSocket, 
    token: str = None, 
    db: Session = Depends(get_db)
):
    user = None
    user_id = None
    
    # Authenticate user if token provided
    if token:
        try:
            credentials_exception = Exception("Could not validate credentials")
            token_data = auth.verify_token(token, credentials_exception, "access")
            user = db.query(models.User).filter(models.User.email == token_data.email).first()
            if user is None:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
            user_id = str(user.id)
            username = user.username if hasattr(user, "username") else user.email.split("@")[0]
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    else:
        # Guest mode - generate random user ID
        import uuid
        user_id = f"guest-{uuid.uuid4().hex[:8]}"
        username = f"Guest-{user_id[-4:]}"
    
    # Accept connection
    await chat_manager.connect(websocket, user_id, username)
    
    try:
        # Main WebSocket loop
        while True:
            data = await websocket.receive_text()
            try:
                # Process received data
                message_data = json.loads(data)
                message_type = message_data.get("type", "")
                
                if message_type == "join_room":
                    room_id = message_data.get("room")
                    success = await chat_manager.join_room(user_id, room_id)
                    
                    if success:
                        # Send room participants
                        participants = chat_manager.get_room_participants(room_id)
                        await chat_manager.send_personal_message(
                            json.dumps({
                                "type": "room_joined",
                                "room": room_id,
                                "participants": participants
                            }),
                            websocket
                        )
                
                elif message_type == "leave_room":
                    room_id = message_data.get("room")
                    await chat_manager.leave_room(user_id, room_id)
                
                elif message_type == "chat_message":
                    room_id = message_data.get("room")
                    content = message_data.get("content", "")
                    
                    if room_id and content and room_id in chat_manager.connected_users[user_id]["rooms"]:
                        await chat_manager.broadcast_to_room(
                            room_id,
                            json.dumps({
                                "type": "chat_message",
                                "room": room_id,
                                "content": content,
                                "sender_id": user_id,
                                "username": username,
                                "timestamp": message_data.get("timestamp", None)
                            })
                        )
                
            except json.JSONDecodeError:
                await chat_manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "content": "Invalid JSON format"
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)

# API endpoints for chat information
@router.get("/rooms")
async def get_chat_rooms():
    """Get a list of all active chat rooms"""
    return {"rooms": chat_manager.get_rooms()}

@router.get("/rooms/{room_id}")
async def get_room_info(room_id: str):
    """Get information about a specific chat room"""
    participants = chat_manager.get_room_participants(room_id)
    return {
        "room_id": room_id,
        "participants_count": len(participants),
        "participants": participants
    }
