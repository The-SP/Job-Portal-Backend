from django.urls import path
from .views import *

urlpatterns = [
    path("", JobListView.as_view(), name="job-list"),
    path("<int:pk>/", JobRetrieveView.as_view(), name="job-detail"),
    path("employee/", EmployerJobListView.as_view(), name="employer-job-list"),
    path("create/", JobCreateView.as_view(), name="job-create"),
    path(
        "<int:pk>/update/",
        JobUpdateDestroyView.as_view(),
        name="job-update-destroy",
    ),
]
