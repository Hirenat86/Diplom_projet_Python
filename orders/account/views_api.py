from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer

# Регистрация
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Профиль пользователя
class ProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Логин
class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"status": "logged_in"}, status=status.HTTP_200_OK)
        return Response({"error": "Неверный логин или пароль"}, status=status.HTTP_400_BAD_REQUEST)

# Логаут
class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"status": "logged_out"}, status=status.HTTP_200_OK)

# Смена пароля
class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # Проверка старого пароля
        if not self.object.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Неверный пароль"}, status=status.HTTP_400_BAD_REQUEST)
        # Установка нового пароля
        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response({"status": "password_changed"}, status=status.HTTP_200_OK)
