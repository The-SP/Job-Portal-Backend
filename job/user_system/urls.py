from django.urls import path

from user_system.views import *

urlpatterns = [
    path("profile/seeker/", SeekerProfileView.as_view(), name="seeker-profile"),
    path(
        "profile/employer/",
        EmployerProfileView.as_view(),
        name="employer-profile",
    ),
    path(
        "profile/employer/<int:pk>/",
        CompanyProfileView.as_view(),
        name="company-profile",
    ),
    path(
        "profile/seeker/<int:pk>/",
        ApplicantProfileView.as_view(),
        name="applicant-profile",
    ),
]
