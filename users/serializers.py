from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "id", "first_name", "middle_name", "last_name", "username",
            "contact", "address", "gender", "email", "password", "confirm_password"
        ]

    def validate(self, data):
        if CustomUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if CustomUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match!"})

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name", "middle_name", "last_name",
            "contact", "address", "gender", "email"
        ]

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value