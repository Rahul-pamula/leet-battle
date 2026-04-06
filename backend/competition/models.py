from django.db import models
from users.models import User

class Week(models.Model):
    user_a = models.ForeignKey(User, related_name='weeks_as_a', on_delete=models.CASCADE)
    user_b = models.ForeignKey(User, related_name='weeks_as_b', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    user_a_points = models.IntegerField(default=0)
    user_b_points = models.IntegerField(default=0)
    winner = models.ForeignKey(User, null=True, blank=True, related_name='weeks_won', on_delete=models.SET_NULL)
    payment_amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=20, default='pending',
        choices=[('pending','Pending'),('paid','Paid'),('tie','Tie')])
    loser_unlocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, related_name='payments_made', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='payments_received', on_delete=models.CASCADE)
    amount = models.IntegerField()
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='created',
        choices=[('created','Created'),('paid','Paid'),('failed','Failed')])
    paid_at = models.DateTimeField(null=True, blank=True)
