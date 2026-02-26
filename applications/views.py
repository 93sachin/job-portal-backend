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
        resume = request.FILES.get("resume")

        if not job_id:
            return Response({"error": "Job ID required"}, status=400)

        job = get_object_or_404(Job, id=job_id)

    # Correct field name: applicant
        if Application.objects.filter(applicant=request.user, job=job).exists():
            return Response({"message": "Already applied"}, status=400)

        Application.objects.create(applicant=request.user, job=job, resume=resume)

        return Response({"message": "Applied successfully"}, status=201)

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.generics import UpdateAPIView
from .permissions import IsRecruiter

# Student : MyApplications                                                            
class MyApplicationsView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

# Recruiter: Update Status
class UpdateApplicationStatusView(UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        application = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["SHORTLISTED", "REJECTED"]:
            return Response({"error": "Invalid status"}, status=400)

        application.status = new_status
        application.save()

        return Response({"message": "Status updated"})

# Recruiter: See All Applications
class AllApplicationsView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.all()