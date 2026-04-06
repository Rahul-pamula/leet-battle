from django.contrib.auth.backends import ModelBackend
from .models import User

class MongoAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Debug logging to help trace login failures in dev
            print(f"MongoAuthBackend: user '{username}' not found")
            return None
        if not user.check_password(password):
            print(f"MongoAuthBackend: bad password for '{username}'")
            return None
        if not self.user_can_authenticate(user):
            print(f"MongoAuthBackend: user '{username}' cannot authenticate (inactive?)")
            return None
        print(f"MongoAuthBackend: authentication success for '{username}'")
        return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
