from rest_framework_simplejwt.views import TokenObtainPairView

from .token import MongoTokenObtainPairSerializer


class MongoTokenObtainPairView(TokenObtainPairView):
    serializer_class = MongoTokenObtainPairSerializer
