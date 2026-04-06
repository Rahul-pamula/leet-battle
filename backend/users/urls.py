from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, MeView, InviteFriendView, AcceptFriendView, MyFriendView
from .token_view import MongoTokenObtainPairView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', MongoTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('friends/invite/', InviteFriendView.as_view(), name='invite'),
    path('friends/accept/', AcceptFriendView.as_view(), name='accept'),
    path('friends/my-friend/', MyFriendView.as_view(), name='my-friend'),
]
