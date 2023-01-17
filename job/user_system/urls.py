from django.urls import path

from user_system.views import SeekerProfileView, EmployerProfileView

urlpatterns = [
    path("profile/seeker/", SeekerProfileView.as_view(), name="seeker-profile"),
    path(
        "profile/employer/",
        EmployerProfileView.as_view(),
        name="employer-profile",
    ),
]
