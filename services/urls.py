from django.urls import path
from .views import (
    ServiceListCreateAPIView,
    ServiceRetrieveUpdateDestroyAPIView,
    ServiceImageListCreateAPIView,
    ServiceImageDestroyAPIView,
)

urlpatterns = [
    path('services/', ServiceListCreateAPIView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
    path('service-images/', ServiceImageListCreateAPIView.as_view(), name='service-image-list-create'),
    path('service-images/<int:pk>/', ServiceImageDestroyAPIView.as_view(), name='service-image-delete'),
]
