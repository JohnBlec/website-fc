import json

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import MatchEvent, Matches

Account = get_user_model()


class LiveConsumer(WebsocketConsumer):

    def fetch_event(self, data):
        events = MatchEvent.objects.filter(match_id=data['id']).order_by('timestamp').all()
        content = {
            'command': 'events',
            'events': self.events_to_json(events)
        }
        self.send_event(content)

    def new_event(self, data):
        author = data['from']
        author_user = Account.objects.get(email=author)
        mtch = Matches.objects.get(pk=data['match'])
        event = MatchEvent.objects.create(
            author=author_user,
            content=data['event'],
            type=data['type_event'],
            match=mtch
        )
        content = {
            'command': 'new_event',
            'event': self.event_to_json(event)
        }
        return self.send_live_event(content)

    def events_to_json(self, events):
        result = []
        for event in events:
            result.append(self.event_to_json(event))
        return result

    def event_to_json(self, event):
        return {
            'author': event.author.email,
            'type': event.type,
            'content': event.content,
            'timestamp': str(event.timestamp)
        }

    commands = {
        'fetch_event': fetch_event,
        'new_event': new_event
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_live_event(self, event):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'line_event',
                'event': event
            }
        )

    def send_event(self, mtch_event):
        self.send(text_data=json.dumps(mtch_event))

    def line_event(self, event):
        mtch_event = event['event']
        self.send(text_data=json.dumps(mtch_event))
