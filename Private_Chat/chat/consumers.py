import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Debug log
        print(f"[DEBUG] Attempting to connect WebSocket to room: {self.room_name}")

        try:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"[DEBUG] WebSocket connected to room: {self.room_name}")
        except Exception as e:
            print(f"[ERROR] WebSocket connection failed: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Debug log
        print(f"[DEBUG] WebSocket disconnected from room: {self.room_name} with code {close_code}")

        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"[ERROR] WebSocket disconnection failed: {e}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Debug log
        print(f"[DEBUG] Message received in room {self.room_name}: {message}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Debug log
        print(f"[DEBUG] Message sent to WebSocket in room {self.room_name}: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
