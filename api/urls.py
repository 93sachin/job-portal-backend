from django.urls import path
from .views import RegisterView, CreateJobView, JobListView
from .views import ApplyJobView
from .views import StudentApplicationsView
from .views import UpdateApplicationStatusView
from .views import RecruiterApplicantsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('create-job/', CreateJobView.as_view(), name='create-job'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('apply-job/', ApplyJobView.as_view()),
    path('my-applications/', StudentApplicationsView.as_view()),
    path('update-application/<int:pk>/', UpdateApplicationStatusView.as_view()),
    path('my-applicants/', RecruiterApplicantsView.as_view()),
]

