from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Job
from applications.models import Application
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
# from rest_framework import status
from .serializers import JobSerializer

class CreateJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

    # 🔐 role check
        if request.user.role != "recruiter":
            return Response({"error": "Only recruiters can post jobs"}, status=403)

    # 🔥 validation yaha add karni hai 👇
        if not request.data.get("title"):
            return Response({"error": "Title is required"}, status=400)

        if not request.data.get("description"):
            return Response({"error": "Description is required"}, status=400)

        if not request.data.get("company"):
            return Response({"error": "Company is required"}, status=400)

    # 👇 serializer yaha se start hoga
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class JobListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    

class MyJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.filter(created_by=request.user).annotate(
            total_applications=Count('application'),
            new_applications=Count(
                'application',
                filter=Q(application__is_viewed=False)
            )
        )

        data = []

        for job in jobs:
            data.append({
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "company": job.company,
                "new_applications": job.new_applications,
                "total_applications": job.total_applications
            })

        return Response(data)

class DeleteJobView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            job = get_object_or_404(Job, id=pk)

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
            job = get_object_or_404(Job, id=pk)

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
        job = get_object_or_404(Job, id=pk)

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

        # 🔹 safe way (no crash)
        application = get_object_or_404(Application, id=pk)

        # 🔐 security check
        if application.job.created_by != request.user:
            return Response({"error": "Not allowed"}, status=403)

        # 🔥 status value le
        status_value = request.data.get("status")

        # ❌ agar status hi nahi bheja
        if not status_value:
            return Response({"error": "Status is required"}, status=400)

        # 🔥 valid status list
        valid_status = ["PENDING", "SHORTLISTED", "REJECTED"]

        # ❌ invalid value
        if status_value not in valid_status:
            return Response({
                "error": "Invalid status",
                "allowed": valid_status
            }, status=400)

        # ✅ save
        application.status = status_value
        application.save()

        return Response({
            "success": True,
            "message": "Status updated successfully",
            "status": application.status
        })
        
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