from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Week, Payment
from users.models import User
from .serializers import WeekSerializer, PaymentSerializer
from problems.models import DailyAssignment
from datetime import date, timedelta

def calculate_payment(points_a, points_b):
    diff = abs(points_a - points_b)
    if diff == 0:
        return 0, "tie"
    amount = max(10, min(210, diff * 10))
    winner = "a" if points_a > points_b else "b"
    return amount, winner


def get_active_week(user, on_date=None):
    today = on_date or date.today()
    return Week.objects.filter(
        (models.Q(user_a=user) | models.Q(user_b=user)) &
        models.Q(start_date__lte=today, end_date__gte=today)
    ).first()

class CurrentWeekView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        week = get_active_week(request.user)
        if not week:
            return Response(status=status.HTTP_404_NOT_FOUND)
        me = request.user
        opp = week.user_a if week.user_b == me else week.user_b

        my_assignments = DailyAssignment.objects.filter(
            user=me, assigned_date__gte=week.start_date, assigned_date__lte=week.end_date
        )
        opp_assignments = DailyAssignment.objects.filter(
            user=opp, assigned_date__gte=week.start_date, assigned_date__lte=week.end_date
        )

        def slim(assignments):
            return [
                {
                    "id": str(a.id),
                    "assigned_date": a.assigned_date,
                    "solved": a.solved,
                    "points": a.points_awarded,
                    "problem": {
                        "title": a.problem.title,
                        "difficulty": a.problem.difficulty,
                        "slug": a.problem.slug,
                        "order_in_step": a.problem.order_in_step,
                    }
                } for a in assignments
            ]

        return Response({
            "week_start": week.start_date,
            "week_end": week.end_date,
            "my_score": week.user_a_points if week.user_a == me else week.user_b_points,
            "opponent_score": week.user_b_points if week.user_a == me else week.user_a_points,
            "my_assignments": slim(my_assignments),
            "opponent_assignments": [
                {
                    "solved": a.solved,
                    "assigned_date": a.assigned_date,
                    "problem": {
                        "title": a.problem.title,
                        "slug": a.problem.slug,
                        "leetcode_url": a.problem.leetcode_url,
                        "difficulty": a.problem.difficulty,
                        "order_in_step": a.problem.order_in_step,
                    }
                }
                for a in opp_assignments
            ],
        })

class LeaderboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        week = get_active_week(request.user)
        if not week:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "user_a": {"id": week.user_a.id, "username": week.user_a.username, "points": week.user_a_points},
            "user_b": {"id": week.user_b.id, "username": week.user_b.username, "points": week.user_b_points},
            "end_date": week.end_date
        })

class EndWeekView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        week = get_active_week(request.user)
        if not week:
            return Response({"error": "No active week"}, status=status.HTTP_404_NOT_FOUND)

        amount, winner_key = calculate_payment(week.user_a_points, week.user_b_points)
        if winner_key == "tie":
            week.payment_status = "tie"
            week.loser_unlocked = True
        else:
            week.winner = week.user_a if winner_key == "a" else week.user_b
            week.payment_amount = amount
            week.payment_status = "pending"
            loser = week.user_b if winner_key == "a" else week.user_a
            loser.is_locked = True
            loser.save()
        week.save()
        return Response(WeekSerializer(week).data)

class UnlockSimulationView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        week = get_active_week(request.user)
        if not week:
            return Response({"error": "No active week"}, status=status.HTTP_404_NOT_FOUND)

        week.payment_status = "paid"
        week.loser_unlocked = True
        week.save()

        payer = request.user
        receiver = week.user_a if week.user_b == request.user else week.user_b
        Payment.objects.create(
            week=week,
            payer=payer,
            receiver=receiver,
            amount=week.payment_amount or 0,
            status='paid'
        )

        # Unlock loser
        if week.winner:
            loser = week.user_b if week.winner == week.user_a else week.user_a
            loser.is_locked = False
            loser.save()

        # Auto-create next week starting next Monday
        next_start = week.end_date + timedelta(days=(7 - week.end_date.weekday()) % 7 or 7)
        next_end = next_start + timedelta(days=6)
        Week.objects.create(
            user_a=week.user_a,
            user_b=week.user_b,
            start_date=next_start,
            end_date=next_end
        )

        return Response({"status": "unlocked"})

class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "leetcode_username": request.user.leetcode_username,
            "language": request.user.language,
            "problems_solved_this_week": 0,
            "points_this_week": 0,
            "wins": 0
        })
