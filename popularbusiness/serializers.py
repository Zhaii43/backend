from rest_framework import serializers
from .models import PopularBusiness, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name"]

class PopularBusinessSerializer(serializers.ModelSerializer):
    service_category = serializers.StringRelatedField()
    class Meta:
        model = PopularBusiness
        fields = ["id", "service_category", "service_name", "location", "image"]
