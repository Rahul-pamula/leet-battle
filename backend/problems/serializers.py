from rest_framework import serializers
from .models import Problem, DailyAssignment

class ProblemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Problem
        fields = '__all__'

class DailyAssignmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    # Cast FK ObjectId values to strings for JSON serialization
    user = serializers.CharField(source='user_id', read_only=True)
    problem = ProblemSerializer(read_only=True)
    class Meta:
        model = DailyAssignment
        fields = [
            'id',
            'user',
            'problem',
            'assigned_date',
            'solved',
            'solved_at',
            'is_late',
            'points_awarded',
        ]
