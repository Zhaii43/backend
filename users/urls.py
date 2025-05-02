from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView, UserUpdateView, get_user_details

urlpatterns = [
    path('user/register/', UserRegisterView.as_view(), name='register'),
    path('user/login/', UserLoginView.as_view(), name='login'),
    path('user/logout/', UserLogoutView.as_view(), name='logout'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
    path('me/', get_user_details, name='user-details'),
]