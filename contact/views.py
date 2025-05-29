from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer
from .models import ContactMessage
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import os

class ContactMessageCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            contact_message = serializer.save()
            try:
                subject = serializer.validated_data.get('subject') or f"New Contact Form Submission from {serializer.validated_data['name']}"
                email_body = (
                    f"Name: {serializer.validated_data['name']}\n"
                    f"Email: {serializer.validated_data['email']}\n"
                    f"Subject: {subject}\n"
                    f"Message: {serializer.validated_data['message']}"
                )

                # Create email
                email = EmailMessage(
                    subject=subject,
                    body=email_body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=['hanzprahinog@gmail.com'],
                )

                # Attach image if provided
                if contact_message.image:
                    image_path = contact_message.image.path
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            email.attach(
                                os.path.basename(image_path),
                                f.read(),
                                'image/jpeg'  # Adjust MIME type as needed
                            )

                email.send(fail_silently=False)
                return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)