from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/register/", views.UserRegistrationView.as_view(), name="user-registration"
    ),
    path("api/login/", views.UserLoginView.as_view(), name="user-login"),
    path("api/logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "api/online-users/",
        views.OnlineUserListView.as_view(),
        name="online-users-list",
    ),
    path("api/chat/start/", views.ChatStartView.as_view(), name="chat-start"),
    path(
        "api/suggested-friends/<int:user_id>/",
        views.SuggestedFriendsView.as_view(),
        name="suggested-friends",
    ),
    path("api/chat/<str:username>/", views.ChatLobby.as_view()),
]
