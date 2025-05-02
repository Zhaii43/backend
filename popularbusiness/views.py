from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PopularBusiness
from .serializers import PopularBusinessSerializer

class BusinessRegisterView(APIView):
    def post(self, request):
        serializer = PopularBusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Business registered successfully!", "business": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessDetailView(APIView):
    def get(self, request, business_id):
        try:
            business = PopularBusiness.objects.get(id=business_id)
            serializer = PopularBusinessSerializer(business)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PopularBusiness.DoesNotExist:
            return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)



class PopularBusinessListView(generics.ListAPIView):
    queryset = PopularBusiness.objects.all()
    serializer_class = PopularBusinessSerializer