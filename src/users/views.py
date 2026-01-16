from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class TelegramChatIdSerializer(serializers.Serializer):
    telegram_chat_id = serializers.IntegerField()


class SetTelegramChatIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TelegramChatIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.telegram_chat_id = serializer.validated_data["telegram_chat_id"]
        request.user.save(update_fields=["telegram_chat_id"])
        return Response({"status": "ok"})
