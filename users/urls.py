from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
    get_user_details,
    PasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("me/", get_user_details, name="user-details"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]