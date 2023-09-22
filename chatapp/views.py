from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChatStartSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from .models import UserProfile
from .serializers import OnlineUserSerializer
from django.contrib.auth.models import User
from .friends.recommendation_algorithm import get_suggested_friends
from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer


class UserRegistrationView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        security=[],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success_message": "Registration successful."},
                template_name="chatapp/register.html",
            )
        return Response({"form": serializer}, template_name="chatapp/register.html")

    def get(self, request):
        return render(request, "chatapp/register.html")


class UserLoginView(APIView):
    authentication_classes = [
        TokenAuthentication
    ]  # Use TokenAuthentication for this view
    renderer_classes = [TemplateHTMLRenderer]

    @swagger_auto_schema(request_body=UserLoginSerializer, security=[])
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Create or retrieve an authentication token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "user_email": user.email,
                    "token": token.key,
                    "success_message": "login successful!",
                },
                template_name="chatapp/login.html",
            )
        return Response({"form": serializer}, template_name="chatapp/login.html")

    def get(self, request):
        return render(request, "chatapp/login.html")


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token associated with the user
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        print("logout superuser", user.is_superuser)
        if not user.is_superuser:
            user.userprofile.is_online = False
            user.userprofile.save()

        token.delete()

        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)


class OnlineUserListView(generics.ListAPIView):
    serializer_class = OnlineUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(is_online=True)


class ChatStartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChatStartSerializer)
    def post(self, request):
        serializer = ChatStartSerializer(data=request.data)

        if serializer.is_valid():
            recipient_username = serializer.validated_data["recipient_username"]

            try:
                recipient_user = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                return Response(
                    {"message": "Recipient user does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                recipient_profile = UserProfile.objects.get(user=recipient_user)

                if recipient_profile.is_online:
                    return Response(
                        {"message": "Chat started successfully."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Recipient user is offline or unavailable."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except UserProfile.DoesNotExist:
                return Response(
                    {"message": "Recipient user profile does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuggestedFriendsView(generics.ListAPIView):
    @swagger_auto_schema(security=[])
    def get(self, request, user_id):
        suggested_friends = get_suggested_friends(user_id)
        context = {"recommended_friends": suggested_friends}
        return render(request, "chatapp/recommended_friends.html", context)


class ChatLobby(APIView):
    def get(self, request, username):
        return render(request, "chatapp/chat_lobby.html")
