from django.urls import path

from .views import UserRegisterView, SetTelegramChatIdView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "telegram-chat-id/",
        SetTelegramChatIdView.as_view(),
        name="set-telegram-chat-id"
    ),
]
