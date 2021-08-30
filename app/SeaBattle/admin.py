from django.contrib import admin
from django.apps import apps

RoomModels = apps.get_model('SeaBattle', 'RoomModels')
MessageModels = apps.get_model('SeaBattle', 'MessageModels')
RoomFieldDataModels = apps.get_model('SeaBattle', 'RoomFieldDataModels')

admin.site.register(RoomModels)
admin.site.register(MessageModels)
admin.site.register(RoomFieldDataModels)
