from django.shortcuts import render
from rest_framework import generics, status
from .models import Service, ServiceImage, Booking, WorkSpecification, Review, Reply
from .serializers import ServiceSerializer, ServiceImageSerializer, BookingSerializer, ReviewSerializer, ReplySerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        response.data["username"] = user.username
        return response

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Fetching profile for user: {request.user.username}")
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username
        })

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return Review.objects.filter(service_id=service_id).prefetch_related('replies')

    def perform_create(self, serializer):
        service_id = self.kwargs.get('service_id')
        serializer.save(user=self.request.user, service_id=service_id)
        logger.info(f"Review created by {self.request.user.username} for service {service_id}")

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).prefetch_related('replies')

    def perform_update(self, serializer):
        logger.info(f"Review updated by {self.request.user.username} for service {self.kwargs.get('pk')}")
        serializer.save()

    def perform_destroy(self, instance):
        logger.info(f"Review deleted by {self.request.user.username} for service {instance.service.id}")
        instance.delete()

class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Reply.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(user=self.request.user, review_id=review_id)
        logger.info(f"Reply created by {self.request.user.username} for review {review_id}")

class ReplyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reply.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        logger.info(f"Reply updated by {self.request.user.username} for review {self.kwargs.get('pk')}")
        serializer.save()

    def perform_destroy(self, instance):
        logger.info(f"Reply deleted by {self.request.user.username} for review {instance.review.id}")
        instance.delete()

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category and category != 'all':
            return self.queryset.filter(category=category).prefetch_related('reviews__replies')
        return self.queryset.prefetch_related('reviews__replies')

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('images', 'reviews__replies')

class ServiceImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ServiceImageDestroyAPIView(generics.DestroyAPIView):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            logger.info(f"Creating booking with data: {serializer.validated_data}")
            serializer.save(user=self.request.user, is_editable=True)
            logger.info("Booking created successfully")
        except Exception as e:
            logger.error(f"Failed to create booking: {str(e)}")
            raise

class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class BookingUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_editable=True, status='scheduled')

    def perform_update(self, serializer):
        logger.info(f"Booking updated by {self.request.user.username} for booking {self.kwargs.get('pk')}")
        serializer.save()

    def perform_destroy(self, instance):
        logger.info(f"Booking deleted by {self.request.user.username} for booking {instance.id}")
        instance.delete()