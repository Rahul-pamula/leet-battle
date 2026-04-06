from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MongoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Store Mongo ObjectId as plain string so simplejwt can look up the user correctly
        token['user_id'] = str(user.pk)
        return token
