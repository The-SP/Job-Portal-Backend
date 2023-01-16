from django.urls import path

from user_system.views import ProfileDetailView

urlpatterns = [
    path("profile/", ProfileDetailView.as_view(), name='profile-detail'),
]
