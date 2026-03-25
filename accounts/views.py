from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from accounts.models import User

# 🔐 Current User (JWT required)
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "role": request.user.role
        })


# 🔐 Profile API (JWT required)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "id": user.id
    })


# 🧠 IMPORTANT: USER CREATE API (TEMP FIX)
@api_view(['GET'])
def create_user(request):
    if not User.objects.filter(username="admin").exists():
        user = User.objects.create_user(
            username="admin",
            password="admin123"
        )
        user.role = "recruiter"  # 👈 agar role field hai
        user.save()
        return Response({"msg": "User created"})
    return Response({"msg": "User already exists"})

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer