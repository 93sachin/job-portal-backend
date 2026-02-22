from django.urls import path
from .views import ApplyJobView, MyApplicationsView
from .views import UpdateApplicationStatusView
from .views import AllApplicationsView

urlpatterns = [
    path('apply/', ApplyJobView.as_view(), name='apply'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('<int:pk>/update-status/', UpdateApplicationStatusView.as_view()),
    path('', AllApplicationsView.as_view(), name='all-applications'),
]