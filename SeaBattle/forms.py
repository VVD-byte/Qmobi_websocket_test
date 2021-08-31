from django import forms
from django.contrib.auth.models import User

from django.apps import apps
RoomModels = apps.get_model('SeaBattle', 'RoomModels')


class CreateGameForm(forms.ModelForm):

    NameRoom = forms.CharField(label='Название комнаты', max_length=100, required=True)
    SecondUser = forms.IntegerField(label='id второго игрока', required=True)

    class Meta:
        model = RoomModels
        fields = ('NameRoom', 'SecondUser')

    def clean(self):
        NameRoom = self.cleaned_data['NameRoom']
        SecondUser = self.cleaned_data['SecondUser']
        self.cleaned_data['SecondUser'] = User.objects.filter(id=int(SecondUser)).first()
        if not self.cleaned_data['SecondUser']:
            raise forms.ValidationError(f'Пользователя с id {SecondUser} не существует')
        return self.cleaned_data


class UserLoginForm(forms.ModelForm):

    username = forms.CharField(label='Логин', max_length=100, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь {username} не зарегестрирован')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный логин или пароль')
        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):

    username = forms.CharField(label='Логин', max_length=100, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Повторение пароля', widget=forms.PasswordInput, required=True)
    email = forms.CharField(label='Почта', widget=forms.EmailInput, required=True)

    class Meta:
        model = User
        fields = ('username',  'email', 'password', 'confirm_password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь {username} уже существует')
        if confirm_password != password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data
