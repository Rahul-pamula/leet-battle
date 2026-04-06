from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import Case, When, IntegerField
from .models import Problem, DailyAssignment
from .serializers import DailyAssignmentSerializer
from ai.client import generate_problem_content
from competition.models import Week
from datetime import date
from django.utils import timezone
from leetcode.client import check_problem_solved

class TodayProblemsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        user = request.user

        week = Week.objects.filter(
            (models.Q(user_a=user) | models.Q(user_b=user)) &
            models.Q(start_date__lte=today, end_date__gte=today)
        ).first()

        if not week:
            return Response([], status=status.HTTP_200_OK)

        assignments = DailyAssignment.objects.filter(user=user, assigned_date=today)
        if not assignments.exists():
            # Basic-first ordering: easy → medium → hard, preserving seed order
            difficulty_order = Case(
                When(difficulty='easy', then=0),
                When(difficulty='medium', then=1),
                When(difficulty='hard', then=2),
                default=3,
                output_field=IntegerField()
            )

            already_assigned_ids = set(
                DailyAssignment.objects.filter(
                    user=user,
                    assigned_date__gte=week.start_date,
                    assigned_date__lte=week.end_date
                ).values_list('problem_id', flat=True)
            )

            candidates = Problem.objects.annotate(diff_order=difficulty_order).order_by(
                'diff_order', 'step_number', 'order_in_step'
            )

            selected = []
            for p in candidates:
                if p.id in already_assigned_ids:
                    continue
                selected.append(p)
                if len(selected) == 3:
                    break

            # If fewer than 3 remain (end of list), still create what we have
            for p in selected:
                DailyAssignment.objects.create(
                    user=user,
                    problem=p,
                    assigned_date=today
                )
            assignments = DailyAssignment.objects.filter(user=user, assigned_date=today)

        for assignment in assignments:
            p = assignment.problem
            if not p.ai_generated:
                content = generate_problem_content(p.title, p.topic_tag, p.difficulty)
                if content:
                    p.pattern_name = content.get('pattern_name', '')
                    p.pattern_explanation = content.get('pattern_explanation', '')
                    p.time_complexity = content.get('time_complexity', '')
                    p.space_complexity = content.get('space_complexity', '')
                    p.python_template = content.get('python_template', '')
                    p.java_template = content.get('java_template', '')
                    p.ai_generated = True
                    p.save()

        return Response(DailyAssignmentSerializer(assignments, many=True).data)

class MarkSolvedView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        assignment_id = request.data.get('assignment_id')
        if not assignment_id:
            return Response({"error": "assignment_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assignment = DailyAssignment.objects.get(id=assignment_id, user=request.user)
        except DailyAssignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)

        if assignment.solved:
            return Response({"verified": True, "points": assignment.points_awarded, "assignment": DailyAssignmentSerializer(assignment).data})

        if not request.user.leetcode_username:
            return Response({"error": "LeetCode username not set on profile"}, status=status.HTTP_400_BAD_REQUEST)

        verified, solved_at = check_problem_solved(request.user.leetcode_username, assignment.problem.slug, assignment.assigned_date)
        if not verified:
            return Response({"verified": False, "reason": "No verified Accepted submission found after assignment date"}, status=status.HTTP_400_BAD_REQUEST)

        # Points calculation
        on_time = solved_at.date() == assignment.assigned_date
        points = 10 if on_time else 5
        if assignment.problem.difficulty == 'hard':
            points += 2

        week = Week.objects.filter(
            (models.Q(user_a=request.user) | models.Q(user_b=request.user)) &
            models.Q(start_date__lte=assignment.assigned_date, end_date__gte=assignment.assigned_date)
        ).first()

        # If solved after the week ends, disallow
        if week and solved_at.date() > week.end_date:
            return Response({"verified": False, "reason": "Submission is after the competition week ended"}, status=status.HTTP_400_BAD_REQUEST)

        assignment.solved = True
        assignment.solved_at = solved_at
        assignment.is_late = not on_time
        assignment.points_awarded = points
        assignment.save()

        if week:
            if week.user_a == request.user:
                week.user_a_points += points
            else:
                week.user_b_points += points
            week.save()

        data = DailyAssignmentSerializer(assignment).data
        data.update({"verified": True, "points": points})
        return Response(data)

class WeekProblemsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        week = Week.objects.filter(
            (models.Q(user_a=request.user) | models.Q(user_b=request.user)) &
            models.Q(start_date__lte=today, end_date__gte=today)
        ).first()

        if not week:
            return Response([])

        assignments = DailyAssignment.objects.filter(
            user=request.user,
            assigned_date__gte=week.start_date,
            assigned_date__lte=week.end_date
        )
        return Response(DailyAssignmentSerializer(assignments, many=True).data)
