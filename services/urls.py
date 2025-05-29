from django.urls import path
from .views import (
    ServiceListCreateAPIView,
    ServiceRetrieveUpdateDestroyAPIView,
    ServiceImageListCreateAPIView,
    ServiceImageDestroyAPIView,
    BookingCreateAPIView,
    BookingListAPIView,
    BookingUpdateDestroyAPIView,
    ReviewRetrieveUpdateDestroyAPIView,
    ReviewListCreateAPIView,
    ReplyListCreateAPIView,
    ReplyRetrieveUpdateDestroyAPIView,
    CustomTokenObtainPairView,
    UserProfileAPIView,
)

urlpatterns = [
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
    path('services/<int:service_id>/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
    path('reviews/<int:review_id>/replies/', ReplyListCreateAPIView.as_view(), name='reply-list-create'),
    path('replies/<int:pk>/', ReplyRetrieveUpdateDestroyAPIView.as_view(), name='reply-detail'),
    path('service-images/', ServiceImageListCreateAPIView.as_view(), name='service-image-list-create'),
    path('service-images/<int:pk>/', ServiceImageDestroyAPIView.as_view(), name='service-image-delete'),
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/my/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingUpdateDestroyAPIView.as_view(), name='booking-update-delete'),
    path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('users/me/', UserProfileAPIView.as_view(), name='user-profile'),
]