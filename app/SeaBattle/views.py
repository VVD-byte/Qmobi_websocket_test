from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.apps import apps
from app.SeaBattle import forms

RoomModels = apps.get_model('SeaBattle', 'RoomModels')
MessageModels = apps.get_model('SeaBattle', 'MessageModels')
RoomFieldDataModels = apps.get_model('SeaBattle', 'RoomFieldDataModels')


def check_anon(func):
    def wrap(*args, **kwargs):
        if args[-1].user.is_anonymous:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect("/")

    return wrap


def check_not_anon(func):
    def wrap(*args, **kwargs):
        if not args[-1].user.is_anonymous:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect("/")

    return wrap


class ConnectGameView(View):
    @check_not_anon
    def get(self, request, room_name):
        room = RoomModels.objects.filter(
            Q(FirstUser=request.user) | Q(SecondUser=request.user),
            id=room_name,
            Active=True
        ).first()
        if room:
            if room.FirstUser == request.user:
                you_field = room.FieldData.FirstUserField
                you_ready = room.FieldData.ReadyFirstUser
                rival_field = room.FieldData.SecondUserField
            else:
                you_field = room.FieldData.SecondUserField
                you_ready = room.FieldData.ReadySecondUser
                rival_field = room.FieldData.FirstUserField
            rival_field = [[j if j != 3 else 0 for j in i] for i in rival_field]
            message = MessageModels.objects.filter(Room=room)
            return render(request, 'SeaBattle/game_field.html', {'room_name': room_name, 'room': room,
                                                                 'you_field': you_field,
                                                                 'you_ready': you_ready,
                                                                 'rival_field': rival_field,
                                                                 'message': message,
                                                                 'color': ["#FFFFFF", "#000000", "#FF0000", "#f3bd48"]})
        return HttpResponseRedirect("/")


class CreateGameView(View):
    @check_not_anon
    def get(self, request):
        form = forms.CreateGameForm()
        return render(request, 'SeaBattle/create_game.html', {'form': form})

    @check_not_anon
    def post(self, request):
        form = forms.CreateGameForm(request.POST or None)
        if form.is_valid():
            RF = RoomFieldDataModels(
                FirstUserField=[[0 for i in range(10)] for j in range(10)],
                SecondUserField=[[0 for i in range(10)] for j in range(10)]
            )
            RF.save()
            room = RoomModels(
                NameRoom=form.cleaned_data['NameRoom'],
                FirstUser=request.user,
                SecondUser=form.cleaned_data['SecondUser'],
                FieldData=RF
            )
            room.save()
            return HttpResponseRedirect("/")
        return render(request, 'SeaBattle/create_game.html', {'form': form})


class MainPageView(View):
    def get(self, request):
        context = {}
        if not request.user.is_anonymous:
            context['user_room'] = RoomModels.objects.filter(
                Q(FirstUser=request.user) | Q(SecondUser=request.user),
                Active=True
            )
        return render(request, 'SeaBattle/main.html', context=context)


class RegisterUserVies(View):
    @check_anon
    def get(self, request):
        form = forms.UserRegisterForm()
        return render(request, 'SeaBattle/register.html', {'form': form})

    @check_anon
    def post(self, request):
        form = forms.UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        return render(request, 'SeaBattle/register.html', {'form': form})


class LoginUserView(View):
    @check_anon
    def get(self, request):
        form = forms.UserLoginForm()
        return render(request, 'SeaBattle/login.html', {'form': form})

    @check_anon
    def post(self, request):
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        return render(request, 'SeaBattle/login.html', {'form': form})


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
