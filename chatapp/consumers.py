import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("here")
        username = self.get_user_from_token(self.scope["query_string"])
        other_username = self.get_other_username(self.scope["query_string"])
        print(username, other_username)
        user = User.objects.get(username=username)
        other_user = User.objects.get(username=other_username)
        print("user", user, "other_user", other_user)

        if user == AnonymousUser or other_user.userprofile.is_online == False:
            self.close()
        else:
            self.room_group_name = self.create_room_identifier(user.id, other_user.id)

            self.channel_layer.group_add(self.room_group_name, self.channel_name)

            self.accept()

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.user = user
            self.other_user = other_user

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_username = text_data_json["sender_username"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_username": sender_username,
            },
        )

    def chat_message(self, event):
        message = event["message"]
        sender_username = event["sender_username"]
        print("message", message)
        print("chat_user", self.user, "chat_other_user", self.other_user)
        self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "message": message,
                    "sender_username": sender_username,
                }
            )
        )

    def get_user_from_token(self, query_string):
        query_dict = parse_qs(query_string.decode())
        token_value = query_dict.get("token", [None])[0]

        if token_value:
            try:
                token = Token.objects.get(key=token_value)
                user = token.user
                return user.username
            except Token.DoesNotExist:
                pass

        return AnonymousUser()

    def get_other_username(self, query_string):
        query_dict = parse_qs(query_string.decode())
        other_username = query_dict.get("other_user", [None])[0]
        return other_username

    def create_room_identifier(self, user1_id, user2_id):
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
