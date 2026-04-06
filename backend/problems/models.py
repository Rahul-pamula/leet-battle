from django.db import models
from users.models import User

class Problem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    leetcode_url = models.URLField()
    difficulty = models.CharField(max_length=10, choices=[('easy','Easy'),('medium','Medium'),('hard','Hard')])
    topic_tag = models.CharField(max_length=100)
    step_number = models.IntegerField()
    order_in_step = models.IntegerField()
    module = models.CharField(max_length=20, default='striver')
    pattern_name = models.CharField(max_length=100, blank=True)
    pattern_explanation = models.TextField(blank=True)
    python_template = models.TextField(blank=True)
    java_template = models.TextField(blank=True)
    time_complexity = models.CharField(max_length=50, blank=True)
    space_complexity = models.CharField(max_length=50, blank=True)
    ai_generated = models.BooleanField(default=False)

class DailyAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    solved = models.BooleanField(default=False)
    solved_at = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    points_awarded = models.IntegerField(default=0)
