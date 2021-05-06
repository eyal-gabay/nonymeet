from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .message import *

import json
import time


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        my_list = [message, self.scope["cookies"]["sid"].split(".")[0], self.room_group_name[5:],
                   time.strftime("%H:%M:%S", time.localtime())]
        if my_list[2] != "null":
            with open("database/chat_rooms/" + my_list[2], "a") as chatroom:
                chatroom.write(my_list[0] + "`" + my_list[3] + "`" + my_list[1] + "\n")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message + "`" + self.scope["cookies"]["sid"].split(".")[0] + "`" + time.strftime("%H:%M:%S", time.localtime())
        }))


class SendMessageToAll(WebsocketConsumer):
    def connect(self):
        self.accept()
        count = str(int(open("database/connected").read()) + 1)
        with open("database/connected", "w") as database:
            database.write(count)
        try:
            username = self.scope["cookies"]["sid"].split(".")[0]
            while read(username):
                self.send(read(username, True)[0][1])
                if read(username):
                    break
        except (KeyError, AttributeError):
            pass

    def receive(self, text_data="", bytes_data=None):
        self.user = text_data.split(".")[0]
        with open("database/users_that_login", "a") as database:
            database.write(self.user + "\n")

    def disconnect(self, code):
        with open("database/connected") as database:
            count = str(int(database.read()) - 1)
            with open("database/connected", "w") as db:
                db.write(count)
            with open("database/users_that_login") as users:
                for user in users.read().splitlines():
                    open("database/users_that_login", "w").close()
                    if user:
                        if user != self.user:
                            with open("database/users_that_login", "a") as login_users:
                                login_users.write(self.user + "\n")
