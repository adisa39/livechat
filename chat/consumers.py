import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json['username']

        # conversation = Conversation.objects.get(pk=int(self.room_name))
        # user = User.objects.get(username=username)
        # conversation_message = ConversationMessage()
        # conversation_message.content = message
        # conversation_message.conversation = conversation
        # conversation_message.created_by = user
        # conversation_message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "username": username}))