from django.urls import path
from .views import *

urlpatterns = [
    path("", JobListView.as_view(), name="job-list"),
    path("<int:pk>/", JobRetrieveView.as_view(), name="job-detail"),
    path("employer/", EmployerJobListView.as_view(), name="employer-job-list"),
    path("create/", JobCreateView.as_view(), name="job-create"),
    path(
        "<int:pk>/update/",
        JobUpdateDestroyView.as_view(),
        name="job-update-destroy",
    ),
    # Scraped jobs
    path("scraped/", ScrapedJobListView.as_view(), name="scraped-job-list"),
]
