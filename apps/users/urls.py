from django.urls import path


#local imports 
from .views import (
    LoginAPIView,
    PasswordChangeView,
    UserAPIView,
    UserDetailAPIView
    )

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("users/", UserAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="users_detail"),
]