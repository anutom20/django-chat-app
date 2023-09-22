from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from .models import UserProfile
from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token


class UpdateLastActivityMiddleware:
    print("updatelastactivity")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if a token is provided in the request
        if "Authorization" in request.headers:
            try:
                # Extract the token string from the request
                token_string = request.headers["Authorization"].split()[1]
                # Get the user associated with the token
                token = Token.objects.get(key=token_string)
                user = token.user
                print("isAuth", user.is_authenticated, "isSuperUser", user.is_superuser)
                # Check if the user is authenticated and not a superuser
                if user.is_authenticated and not user.is_superuser:
                    print("Middleware inside")
                    user_profile = user.userprofile
                    user_profile.last_activity = timezone.now()
                    user_profile.save()
            except Token.DoesNotExist:
                pass

        response = self.get_response(request)
        return response


class UpdateTokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "Authorization" in request.headers:
            try:
                # Extract the token string from the request
                token_string = request.headers["Authorization"].split()[1]
                # Get the user associated with the token
                token = Token.objects.get(key=token_string)
                user = token.user

                if user.is_authenticated and not user.is_superuser:
                    now = timezone.now()

                # Iterate over all online users
                for user_profile in UserProfile.objects.filter(is_online=True):
                    last_activity = user_profile.last_activity
                    print(now, last_activity)
                    # Check if the user's last activity was more than 5 minutes ago
                    if last_activity and now - last_activity > timedelta(minutes=5):
                        # Expire the token for this user
                        Token.objects.filter(user=user_profile.user).delete()
                        user_profile.is_online = False
                        user_profile.save()

            except Token.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
