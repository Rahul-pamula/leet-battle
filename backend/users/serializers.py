import os

from rest_framework import serializers
from .models import User, Friendship
from leetcode.client import validate_username, get_total_solved

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'leetcode_username', 'language', 'baseline_solved', 'created_at', 'is_locked']

class FriendshipSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'leetcode_username', 'language']

    def validate_leetcode_username(self, value):
        """
        Keep LeetCode validation soft so local/dev signups don't break when the
        public API is unreachable or a fake username is used.
        Set ENFORCE_LEETCODE_VALIDATION=true to make the check strict again.
        """
        if not value:
            return value

        enforce = os.getenv('ENFORCE_LEETCODE_VALIDATION', '').lower() == 'true'
        is_valid = validate_username(value)
        if is_valid or not enforce:
            return value

        raise serializers.ValidationError("Invalid LeetCode username.")

    def create(self, validated_data):
        leetcode_username = validated_data.get('leetcode_username', '')
        baseline = get_total_solved(leetcode_username) if leetcode_username else 0
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            leetcode_username=leetcode_username,
            language=validated_data.get('language', 'python'),
            baseline_solved=baseline
        )
        return user
