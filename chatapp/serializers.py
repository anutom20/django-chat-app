from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
import re
from datetime import datetime


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        # Check if the username matches the regex pattern (letters and digits only)
        if not re.match(r"^\w+$", value):
            raise serializers.ValidationError(
                "Username must contain only letters, digits, and underscores."
            )
        # Check if the username already exists in the database
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username address already exists.")
        return value

    def validate_email(self, value):
        # Check if the email matches the regex pattern for a valid email address
        if not re.match(r"^[\w\.-]+@[\w\.-]+$", value):
            raise serializers.ValidationError("Invalid email address.")
        # Check if the email already exists in the database
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exists.")
        return value

    def validate_password(self, value):
        # Check if the password meets your desired length criteria (e.g., at least 8 characters)
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    def create(self, validated_data):
        # Create the User instance
        user = User.objects.create_user(**validated_data)

        # Create the associated UserProfile
        UserProfile.objects.create(
            user=user, is_online=False
        )  # Adjust fields as needed

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                print("login superuser", user.is_superuser)

                if user.is_active and not user.is_superuser:
                    data["user"] = user
                    user.userprofile.is_online = True
                    user.userprofile.last_activity = datetime.now()
                    user.userprofile.save()
                else:
                    raise serializers.ValidationError("User account is not active.")
            else:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError(
                "Both username and password are required."
            )

        return data


class OnlineUserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ["username", "is_online", "last_activity"]


class ChatStartSerializer(serializers.Serializer):
    recipient_username = serializers.CharField(max_length=150)
