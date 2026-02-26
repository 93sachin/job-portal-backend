from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add role inside token
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Send role in response also
        data['role'] = self.user.role
        return data