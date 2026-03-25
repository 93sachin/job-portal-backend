from django.urls import path
from .views import CurrentUserView
from .views import profile_view
from .views import create_user

urlpatterns = [
    path("user/", CurrentUserView.as_view()),
    path('profile/', profile_view),
    path('create-user/', create_user),
]