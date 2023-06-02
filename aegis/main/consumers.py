import datetime
import json

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import MatchEvent, Matches, TransMatch

Account = get_user_model()


class LiveConsumer(WebsocketConsumer):

    def fetch_event(self, data):
        events = MatchEvent.objects.filter(match_id=data['id']).order_by('data_time').all()
        content = {
            'command': 'events',
            'events': self.events_to_json(events)
        }
        self.send_event(content)

    def new_event(self, data):
        author = data['from']
        author_user = Account.objects.get(email=author)
        mtch = Matches.objects.get(pk=data['match'])
        goal = ' '
        goalsum = 0
        if data['type_event'] == 'goal-aeg':
            if mtch.home_team.q_we:
                num = mtch.home_goals
                mtch.home_goals = int(num) + 1
                goalsum = mtch.home_goals
                goal = 'home'
            else:
                num = mtch.away_goals
                mtch.away_goals = int(num) + 1
                goalsum = mtch.away_goals
                goal = 'away'
        if data['type_event'] == 'goal-eny':
            if mtch.home_team.q_we:
                num = mtch.away_goals
                mtch.away_goals = int(num) + 1
                goalsum = mtch.away_goals
                goal = 'away'
            else:
                num = mtch.home_goals
                mtch.home_goals = int(num) + 1
                goalsum = mtch.home_goals
                goal = 'home'
        mtch.save()
        event = MatchEvent.objects.create(
            author=author_user,
            content=data['event'],
            type=data['type_event'],
            timestamp=data['timestamp'],
            match=mtch
        )
        content = {
            'command': 'new_event',
            'event': self.event_to_json(event),
            'goal': goal,
            'goalsum': goalsum
        }
        return self.send_live_event(content)

    def start_trans(self, data):
        tr_mtch = TransMatch.objects.get(match_id=data['match'])
        if data['half-time'] == 1:
            tr_mtch.start_1 = str(data['start_time'])
            match = Matches.objects.get(pk=data['match'])
            match.home_goals = 0
            match.away_goals = 0
            match.save()
        else:
            tr_mtch.start_2 = str(data['start_time'])
        tr_mtch.save()
        content = {
            'command': 'change'
        }
        self.send_change_state(content)

    def pause(self, data):
        tr_mtch = TransMatch.objects.get(match_id=data['match'])
        tr_mtch.pause = str(data['pause_time'])
        tr_mtch.save()
        content = {
            'command': 'change'
        }
        self.send_change_state(content)

    def end_trans(self, data):
        tr_mtch = TransMatch.objects.get(match_id=data['match'])
        tr_mtch.end = str(data['end_time'])
        tr_mtch.save()
        content = {
            'command': 'change'
        }
        self.send_change_state(content)

    def refresh_time(self, data):
        tr_mtch = TransMatch.objects.get(match_id=data['match'])
        a = data['now'].split(':')
        b = []
        if tr_mtch.start_1:
            b = str(tr_mtch.start_1).split(':')
        if tr_mtch.start_2:
            b = str(tr_mtch.start_2).split(':')
        start = datetime.timedelta(hours=int(a[0]), minutes=int(a[1]), seconds=int(a[2]))
        now = datetime.timedelta(hours=int(b[0]), minutes=int(b[1]), seconds=int(b[2]))
        m_s = ''
        if tr_mtch.start_1:
            m_s = str(start - now).split(':')
        if tr_mtch.start_2:
            m_s = str(start - now + datetime.timedelta(minutes=25)).split(':')
        sub = m_s[1]
        content = {
            'command': 'refresh',
            'time': sub
        }
        self.send_refresh(content)

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
        'new_event': new_event,
        'start_trans': start_trans,
        'refresh_time': refresh_time,
        'pause': pause,
        'end_trans': end_trans
    }

    def connect(self):
        self.room_group_name = "live"

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
                'type': 'live_event',
                'event': event
            }
        )

    def live_event(self, event):
        mtch_event = event['event']
        self.send(text_data=json.dumps(mtch_event))

    def send_event(self, mtch_event):
        self.send(text_data=json.dumps(mtch_event))

    def send_refresh(self, time):
        self.send(text_data=json.dumps(time))

    def send_change_state(self, state):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'change_state_match',
                'state': state
            }
        )

    def change_state_match(self, state):
        mtch_state = state['state']
        self.send(text_data=json.dumps(mtch_state))
