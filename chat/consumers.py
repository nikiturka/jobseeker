from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass
