from django.urls import path
from .views import BusinessRegisterView, BusinessDetailView, PopularBusinessListView

urlpatterns = [
    # Other URLs
    path('business/register/', BusinessRegisterView.as_view(), name='business-register'),
    path('business/list/', PopularBusinessListView.as_view(), name='business-list'),
    path('business/<int:business_id>/', BusinessDetailView.as_view(), name='business-detail'),
]
