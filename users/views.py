from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, PasswordResetToken
from .serializers import UserSerializer, UserUpdateSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import timedelta

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful!",
                "username": user.username,
                "email": user.email,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

class UserLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!", "user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"error": "No user is associated with this email address."}, status=status.HTTP_400_BAD_REQUEST)

            token = str(uuid.uuid4())
            
            try:
                PasswordResetToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=timezone.now() + timedelta(hours=1)
                )
            except Exception as e:
                return Response({"error": "Failed to generate reset token."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            reset_link = f"https://home-service-uk6z.vercel.app/reset-password?token={token}&email={email}"
            
            try:
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {reset_link}\nThis link will expire in 1 hour.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"error": "Invalid email."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                reset_token = PasswordResetToken.objects.get(user=user, token=token)
                if not reset_token.is_valid():
                    return Response({"error": "This reset token is expired."}, status=status.HTTP_400_BAD_REQUEST)
            except PasswordResetToken.DoesNotExist:
                return Response({"error": "Invalid reset token."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user.set_password(password)
                user.save()
                reset_token.delete()
                return Response({"message": "Password reset successfully. You can now log in with your new password."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to update password: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)