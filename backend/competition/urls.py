from django.urls import path
from .views import CurrentWeekView, LeaderboardView, EndWeekView, UnlockSimulationView, ProfileView

urlpatterns = [
    path('week/current/', CurrentWeekView.as_view(), name='current_week'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('week/end/', EndWeekView.as_view(), name='end_week'),
    path('unlock/', UnlockSimulationView.as_view(), name='unlock'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
