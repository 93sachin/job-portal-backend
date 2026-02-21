from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer


class ApplyJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        job_id = request.data.get("job")

        if Application.objects.filter(
            applicant=request.user,
            job_id=job_id
        ).exists():
            return Response(
                {"message": "Already applied"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(applicant=request.user)

        return Response(
            {"message": "Application submitted successfully"},
            status=status.HTTP_201_CREATED
        )