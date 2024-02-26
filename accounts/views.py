from django.shortcuts import render
from django.contrib.auth.views import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import UserSerializer, UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if User.objects.filter(email=email).exists():
            return Response({'success': False, 'error': 'Email already used!'}, status=400)

        if password1 != password2:
            return Response({'success': False, 'error': 'Passwords do not match!'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'error': 'Username already exists!'}, status=400)

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password1
        )
        user_serializer = UserSerializer(user)
        return Response({'success': True, 'data': user_serializer.data})


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)


class UserInfoAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({'success': True, 'data': user_serializer.data})


class UserListAPiView(GenericAPIView):
    permission_classes = ()

    def get(self):
        pass
