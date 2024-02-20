from django.urls import path

from accounts.views import RegisterAPIView, UserInfoAPIView, LogoutAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView,
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('user-info/<int:pk>', UserInfoAPIView.as_view(), name='user_info'),
]
