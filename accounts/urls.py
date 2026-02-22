from django.urls import path
from .views import CurrentUserView
from .views import profile_view

urlpatterns = [
    path("user/", CurrentUserView.as_view()),
    path('profile/', profile_view),
]