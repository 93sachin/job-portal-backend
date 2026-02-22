from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Application
from jobs.models import Job

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        job_id = request.data.get("job")

        if not job_id:
            return Response({"error": "Job ID required"}, status=400)

        job = get_object_or_404(Job, id=job_id)

    # Correct field name: applicant
        if Application.objects.filter(applicant=request.user, job=job).exists():
            return Response({"message": "Already applied"}, status=400)

        Application.objects.create(applicant=request.user, job=job)

        return Response({"message": "Applied successfully"}, status=201)

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
                                                                
class MyApplicationsView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)