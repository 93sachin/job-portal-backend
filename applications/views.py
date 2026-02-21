from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer


class ApplyJobView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]