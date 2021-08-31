from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view()),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserVies.as_view(), name='register'),
    path('create_game/', views.CreateGameView.as_view(), name='create_game'),
    path('game/<int:room_name>', views.ConnectGameView.as_view()),
]
