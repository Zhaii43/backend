from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
    PasswordResetRequestView,
    get_user_details,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("me/", get_user_details, name="user-details"),
]