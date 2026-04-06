from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    leetcode_username = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, choices=[('python','Python'),('java','Java')])
    baseline_solved = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending','Pending'),('accepted','Accepted')])
    created_at = models.DateTimeField(auto_now_add=True)
