from django.urls import path
from .views import CreateJobView, JobListView, MyJobsView, DeleteJobView, UpdateJobView, JobApplicationsView, UpdateApplicationStatusView, RecruiterAnalyticsView, NewApplicationsCountView

urlpatterns = [
    path("create/", CreateJobView.as_view()),
    path("list/", JobListView.as_view()),
    path('my/', MyJobsView.as_view()),
    path('delete/<int:pk>/', DeleteJobView.as_view()),
    path('update/<int:pk>/',UpdateJobView.as_view()),
    path("applications/<int:pk>/", JobApplicationsView.as_view()),
    path("application/update/<int:pk>/", UpdateApplicationStatusView.as_view()),
    path('analytics/',RecruiterAnalyticsView.as_view()),
    path('new-applications-count/', NewApplicationsCountView.as_view()),
]
