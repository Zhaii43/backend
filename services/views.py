from rest_framework import generics
from .models import Service, ServiceImage
from .serializers import ServiceSerializer, ServiceImageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

# List and Create Services
class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category and category != 'all':
            return self.queryset.filter(category=category)
        return self.queryset

# Retrieve, Update, Delete individual services
class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# List and Create Service Images
class ServiceImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Delete a single service image
class ServiceImageDestroyAPIView(generics.DestroyAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
