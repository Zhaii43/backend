from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
import re

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
        password = data["password"]
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            "first_name", "middle_name", "last_name",
            "contact", "address", "gender", "email",
            "current_password", "password", "confirm_password"
        ]

    def validate(self, data):
        email = data.get("email")
        user = self.context['request'].user
        if email and CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        current_password = data.get("current_password")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password or confirm_password or current_password:
            if not current_password:
                raise serializers.ValidationError({"current_password": "Current password is required to update password."})
            if not user.check_password(current_password):
                raise serializers.ValidationError({"current_password": "Current password is incorrect."})
            if password != confirm_password:
                raise serializers.ValidationError({"password": "New passwords do not match."})
            if not password:
                raise serializers.ValidationError({"password": "New password is required."})
            if not confirm_password:
                raise serializers.ValidationError({"confirm_password": "Confirm password is required."})
            if password:
                if len(password) < 8:
                    raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
                if not re.search(r"[A-Z]", password):
                    raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    raise serializers.ValidationError({"password": "Password must contain at least one special character."})
        return data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.middle_name = validated_data.get("middle_name", instance.middle_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.contact = validated_data.get("contact", instance.contact)
        instance.address = validated_data.get("address", instance.address)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.email = validated_data.get("email", instance.email)
        if validated_data.get("password"):
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value