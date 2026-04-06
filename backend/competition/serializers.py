from rest_framework import serializers
from .models import Week, Payment
from users.serializers import UserSerializer

class WeekSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user_a = UserSerializer(read_only=True)
    user_b = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    
    class Meta:
        model = Week
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
