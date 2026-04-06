from django.urls import path
from .views import TodayProblemsView, MarkSolvedView, WeekProblemsView

urlpatterns = [
    path('today/', TodayProblemsView.as_view(), name='today'),
    path('mark-solved/', MarkSolvedView.as_view(), name='mark-solved'),
    path('week/', WeekProblemsView.as_view(), name='week'),
]
