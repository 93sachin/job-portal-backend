from django.urls import path
from .views import ApplyJobView, MyApplicationsView

urlpatterns = [
    path("apply/", ApplyJobView.as_view(), name="apply"),
    path("my-applications/", MyApplicationsView.as_view(), name="my-applications"),
]