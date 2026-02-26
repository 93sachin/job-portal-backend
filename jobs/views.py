from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Job
from applications.models import Application
from rest_framework import status
from .serializers import JobSerializer

class CreateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "recruiter":
            return Response({"error": "Only recruiters can post jobs"})

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class MyJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.filter(created_by=request.user)

        data = []

        for job in jobs:
            new_apps = Application.objects.filter(
                job=job,
                is_viewed=False
            ).count()

            total_apps = Application.objects.filter(job=job).count()


            data.append({
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "company": job.company,
                "new_applications": new_apps,
                "total_applications": total_apps
            })

        return Response(data)

class DeleteJobView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            job = Job.objects.get(id=pk)

            # Optional: sirf jisne banaya wahi delete kare
            if job.created_by != request.user:
                return Response({"error": "Not allowed"}, status=403)

            job.delete()
            return Response({"message": "Job deleted"}, status=200)

        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

class UpdateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            job = Job.objects.get(id=pk)

            # Security check
            if job.created_by != request.user:
                return Response({"error": "Not allowed"}, status=403)

            job.title = request.data.get("title", job.title)
            job.description = request.data.get("description", job.description)
            job.company = request.data.get("company", job.company)
            job.save()

            return Response({"message": "Job updated"}, status=200)

        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

class JobApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        job = Job.objects.get(id=pk)

        # Sirf jisne job banayi wahi dekh sake
        if job.created_by != request.user:
            return Response({"error": "Not allowed"}, status=403)

        applications = Application.objects.filter(job=job)
        applications.update(is_viewed=True)

        data = []
        for app in applications:
            data.append({
                "id": app.id,
                "username": app.applicant.username,
                "applied_at": app.applied_at,
                "status": app.status,
                "resume": app.resume.url if app.resume else None,
            })

        return Response(data)
    
class NewApplicationsCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.filter(created_by=request.user)

        new_count = Application.objects.filter(
            job__in=jobs,
            is_viewed=False
        ).count()

        return Response({"new_applications": new_count})

class UpdateApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            application = Application.objects.get(id=pk)

            # Security check – sirf job ka recruiter hi update kare
            if application.job.created_by != request.user:
                return Response({"error": "Not allowed"}, status=403)

            status_value = request.data.get("status")
            application.status = status_value
            application.save()

            return Response({"message": "Status updated"})

        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)
        
class RecruiterAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "recruiter":
            return Response({"error": "Not allowed"}, status=403)

        jobs = Job.objects.filter(created_by=request.user)
        total_jobs = jobs.count()

        applications = Application.objects.filter(job__in=jobs)
        total_applications = applications.count()

        shortlisted = applications.filter(status="SHORTLISTED").count()
        rejected = applications.filter(status="REJECTED").count()
        pending = applications.filter(status="PENDING").count()

        return Response({
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "rejected": rejected,
            "pending": pending
        })