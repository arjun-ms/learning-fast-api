# import asyncio
# import websockets
# import json
# import sys
# from datetime import datetime

# async def receive_messages(websocket):
#     """Handle incoming messages from server"""
#     while True:
#         try:
#             message = await websocket.recv()
#             data = json.loads(message)
#             timestamp = datetime.now().strftime("%H:%M:%S")
            
#             if data.get("type") == "chat_message":
#                 print(f"[{timestamp}] {data.get('username')}: {data.get('content')}")
#             elif data.get("type") == "system":
#                 print(f"[{timestamp}] SYSTEM: {data.get('content')}")
#             elif data.get("type") == "room_joined":
#                 print(f"[{timestamp}] Joined room: {data.get('room')}")
#                 participants = data.get('participants', [])
#                 if participants:
#                     print(f"[{timestamp}] Room participants: " + ", ".join(
#                         [p.get('username') for p in participants]
#                     ))
#             else:
#                 print(f"[{timestamp}] Received: {message}")
#         except websockets.exceptions.ConnectionClosed:
#             print("Connection closed")
#             break
#         except Exception as e:
#             print(f"Error: {e}")
#             break

# async def chat_client():
#     """Main chat client function"""
#     # Get or create username
#     username = input("Enter your username (leave blank for guest): ").strip()
    
#     # Ask for room
#     room = input("Enter room name to join: ").strip() or "general"
    
#     # Construct WebSocket URL with token if logged in as user
#     url = f"ws://localhost:8000/chat/ws"
#     if username:
#         # If you have a token for authentication:
#         # url += f"?token=YOUR_AUTH_TOKEN"
#         pass
    
#     print(f"Connecting to {url}...")
    
#     async with websockets.connect(url) as websocket:
#         # Start a task to receive messages
#         receive_task = asyncio.create_task(receive_messages(websocket))
        
#         # Join the specified room
#         await websocket.send(json.dumps({
#             "type": "join_room",
#             "room": room
#         }))
        
#         print(f"Connected! Type messages and press Enter to send. Type '/quit' to exit.")
#         print(f"Chat commands: '/join ROOM' to join a room, '/leave ROOM' to leave a room")
        
#         try:
#             while True:
#                 message = await asyncio.get_event_loop().run_in_executor(
#                     None, lambda: input("")
#                 )
                
#                 if not message:
#                     continue
                
#                 if message.lower() == '/quit':
#                     break
                
#                 elif message.startswith('/join '):
#                     new_room = message[6:].strip()
#                     if new_room:
#                         await websocket.send(json.dumps({
#                             "type": "join_room",
#                             "room": new_room
#                         }))
                
#                 elif message.startswith('/leave '):
#                     leave_room = message[7:].strip()
#                     if leave_room:
#                         await websocket.send(json.dumps({
#                             "type": "leave_room",
#                             "room": leave_room
#                         }))
                
#                 else:
#                     # Send regular chat message
#                     await websocket.send(json.dumps({
#                         "type": "chat_message",
#                         "room": room,
#                         "content": message,
#                         "timestamp": datetime.now().isoformat()
#                     }))
#         except KeyboardInterrupt:
#             print("Exiting...")
#         finally:
#             receive_task.cancel()

# if __name__ == "__main__":
#     asyncio.run(chat_client())
