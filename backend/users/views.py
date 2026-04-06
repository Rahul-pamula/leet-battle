from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Friendship
from .serializers import UserSerializer, SignupSerializer, FriendshipSerializer
from competition.models import Week
from datetime import date, timedelta
from django.utils import timezone

def _debug(msg, extra=None):
    """Lightweight dev logger."""
    if extra is not None:
        print(msg, extra)
    else:
        print(msg)

class SignupView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # Log errors to help diagnose signup failures (temporary debug)
        _debug("Signup validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class InviteFriendView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            _debug("InviteFriendView missing username", request.data)
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            _debug("InviteFriendView user not found", username)
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == friend:
            return Response({"error": "Cannot invite yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(from_user=request.user, to_user=friend).exists() or \
           Friendship.objects.filter(from_user=friend, to_user=request.user).exists():
           _debug("InviteFriendView duplicate request", {'from': request.user.username, 'to': friend.username})
           return Response({"error": "Friendship or request already exists"}, status=status.HTTP_400_BAD_REQUEST)

        friendship = Friendship.objects.create(from_user=request.user, to_user=friend, status='pending')
        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)

class AcceptFriendView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            _debug("AcceptFriendView missing username", request.data)
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            req_user = User.objects.get(username=username)
            friendship = Friendship.objects.get(from_user=req_user, to_user=request.user, status='pending')
        except (User.DoesNotExist, Friendship.DoesNotExist):
            _debug("AcceptFriendView pending request not found", {'from': username, 'to': request.user.username})
            return Response({"error": "Pending request not found"}, status=status.HTTP_404_NOT_FOUND)
        
        friendship.status = 'accepted'
        friendship.save()

        # Create Week 1 starting next Monday 00:00
        today = date.today()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        start_date = today + timedelta(days=days_until_monday)
        end_date = start_date + timedelta(days=6)
        Week.objects.create(
            user_a=friendship.from_user,
            user_b=friendship.to_user,
            start_date=start_date,
            end_date=end_date
        )

        return Response(FriendshipSerializer(friendship).data)

class MyFriendView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendship = Friendship.objects.filter(
            from_user=request.user, status='accepted'
        ).first()
        if not friendship:
            friendship = Friendship.objects.filter(
                to_user=request.user, status='accepted'
            ).first()

        if not friendship:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        friend = friendship.to_user if friendship.from_user == request.user else friendship.from_user
        return Response(UserSerializer(friend).data)
