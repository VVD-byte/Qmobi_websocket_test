from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.apps import apps

import json

RoomModels = apps.get_model('SeaBattle', 'RoomModels')
MessageModels = apps.get_model('SeaBattle', 'MessageModels')
RoomFieldDataModels = apps.get_model('SeaBattle', 'RoomFieldDataModels')


class ConsumerLogic:
    room_name = None
    # 0 - пустая ячейка, 1 - мимо, 2 - попадание, 3 - ячейка с кораблем
    color = {
        0: 1,
        3: 2
    }

    @database_sync_to_async
    def add_message(self, message, scope):
        if message is None:
            return
        message = MessageModels(
            Sender=scope.get('user', None),
            Room=RoomModels.objects.filter(id=int(self.room_name)).first(),
            Message=message,
        )
        message.save()

    @database_sync_to_async
    def add_move(self, move, scope):
        if move is None:
            return
        room = RoomModels.objects.filter(id=int(self.room_name)).first()
        fields = room.FieldData
        if fields.UserTurn != scope.get('user', None):
            return
        if room.SecondUser == scope.get('user', None):
            fields.FirstUserField[move[0]][move[1]] = self.color[fields.FirstUserField[move[0]][move[1]]]
            fields.UserTurn = room.FirstUser
            fields.save()
            move.append(fields.FirstUserField[move[0]][move[1]])
        elif room.FirstUser == scope.get('user', None):
            fields.SecondUserField[move[0]][move[1]] = self.color[fields.SecondUserField[move[0]][move[1]]]
            fields.UserTurn = room.SecondUser
            fields.save()
            move.append(fields.SecondUserField[move[0]][move[1]])
        move.append(scope.get('user', None).id)
        return move

    @database_sync_to_async
    def update_field(self, field, scope):
        if field is None:
            return
        room = RoomModels.objects.filter(id=int(self.room_name)).first()
        fields = room.FieldData
        if room.FirstUser == scope.get('user', None):
            fields.FirstUserField = field
            fields.ReadyFirstUser = True
        elif room.SecondUser == scope.get('user', None):
            fields.SecondUserField = field
            fields.ReadySecondUser = True
        fields.save()
        return [fields.ReadyFirstUser, fields.ReadySecondUser]


class GameConsumers(AsyncWebsocketConsumer, ConsumerLogic):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        you_field = text_data_json.get('you_field', None)
        message = text_data_json.get('message', None)
        move = text_data_json.get('move', None)

        await self.add_message(message, self.scope)
        move = await self.add_move(move, self.scope)
        you_field = await self.update_field(you_field, self.scope)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_event',
                'you_field': you_field,
                'message': message,
                'move': move,
            }
        )

    async def game_event(self, event):
        you_field = event.get('you_field', None)
        message = event.get('message', None)
        move = event.get('move', None)

        await self.send(text_data=json.dumps({
            'event': 'Send',
            'you_field': you_field,
            'message': message,
            'move': move,
        }))
