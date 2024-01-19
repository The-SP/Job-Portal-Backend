from django.urls import path
from .views import *

urlpatterns = [
    path(
        "applications/create/",
        ApplicationCreateView.as_view(),
        name="application-create",
    ),
    path(
        "applications/<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
    path(
        "user-applications/",
        SeekerApplicationListView.as_view(),
        name="user-application-list",
    ),
    path(
        "<int:job_id>/applications/",
        GetApplicationsForJob.as_view(),
        name="job-application-list",
    ),
    path(
        "<int:job_id>/applications/download/",
        DownloadJobApplicationsExcel.as_view(),
        name="download_job_applications_excel",
    ),
]
