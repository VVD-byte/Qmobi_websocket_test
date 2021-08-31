from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class BaseModel(models.Model):

    class Meta:
        abstract = True
        app_label = 'SeaBattle'


class RoomFieldDataModels(BaseModel):
    FirstUserField = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=10,
        ),
        size=10,
    )
    SecondUserField = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=10,
        ),
        size=10,
    )
    ReadyFirstUser = models.BooleanField(default=False)
    ReadySecondUser = models.BooleanField(default=False)
    UserTurn = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_turn')


class RoomModels(BaseModel):
    NameRoom = models.CharField(max_length=100)
    FirstUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')  # первый игрок
    SecondUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user', blank=True, null=True)  # второй игрок
    FieldData = models.ForeignKey(RoomFieldDataModels, on_delete=models.CASCADE, related_name='field_data')
    Active = models.BooleanField(default=True)  # активна ли комната
    CreateData = models.DateTimeField(auto_now=True)


class MessageModels(BaseModel):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE)
    Room = models.ForeignKey(RoomModels, on_delete=models.CASCADE)  # ссылка комнаты
    Date = models.DateTimeField(auto_now=True)  # время сообщение
    Message = models.CharField(max_length=200)  # текст сообщения
