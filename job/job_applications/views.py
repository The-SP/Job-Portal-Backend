import pandas as pd
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from io import BytesIO
from django.http import FileResponse
from rest_framework.views import APIView

from user_system.permissions import IsEmployer, IsSeeker
from .models import *
from .serializers import *


class ApplicationCreateView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]  # for image/file upload
    permission_classes = [IsSeeker]
    queryset = JobApplication.objects.all()
    serializer_class = CreateJobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Allow owner of the job-application to update and delete
class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsSeeker, IsApplicationOwner]
    queryset = JobApplication.objects.all()
    serializer_class = CreateJobApplicationSerializer


# Get all jobs applied by the Seeker
class SeekerApplicationListView(generics.ListAPIView):
    permission_classes = [IsSeeker]
    serializer_class = SeekerApplicationsListSerializer

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


# Get all job applications for a particular job
class GetApplicationsForJob(generics.ListAPIView):
    permission_classes = [IsEmployer]
    serializer_class = GetApplicationsForJobSerializer

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return JobApplication.objects.filter(
            job_id=job_id, job__posted_by=self.request.user
        )


"""
    API view for downloading a structured Excel file containing job applications data.
    - This view fetches JobApplication objects for a specific job based on the job_id parameter.
    - It generates an Excel file with three sheets: "Interview", "Reject", and "Other".
    - The data includes applicant information such as name, email, phone number, and resume URL.
    - The resume URLs are constructed using the base URL and replacing backslashes with slashes.
    - The Excel file is returned as a downloadable attachment in the HTTP response.

    Usage:
    - Send a GET request to '/path/to/view/{job_id}/download/' to download the Excel file.
    - Replace {job_id} with the actual job ID for which you want to download the job applications.
"""


class DownloadJobApplicationsExcel(APIView):
    def get_excel(self, queryset):
        byte_buffer = BytesIO()
        df = pd.DataFrame(
            list(queryset.values("name", "email", "phone_number", "status", "resume"))
        )

        def get_resume_url(resume):
            if resume:
                resume_link = resume.replace("\\", "/")
                return "http://127.0.0.1:8000/media/" + resume_link
            else:
                return None

        df["resume"] = df["resume"].apply(get_resume_url)

        # Create three separate DataFrames based on status
        interview_df = df[df["status"] == "interview"]
        reject_df = df[df["status"] == "rejected"]
        other_df = df[~df["status"].isin(["interview", "rejected"])]

        # Create Excel writer and add sheets
        with pd.ExcelWriter(byte_buffer) as writer:
            interview_df.to_excel(writer, sheet_name="Interview", index=False)
            reject_df.to_excel(writer, sheet_name="Reject", index=False)
            other_df.to_excel(writer, sheet_name="Other", index=False)

        return byte_buffer

    def get(self, request, job_id, format=None):
        job_applications = JobApplication.objects.filter(job_id=job_id)

        byte_buffer = self.get_excel(job_applications)
        byte_buffer.seek(0)
        filename = f"job_applications_job_{job_id}.xlsx"

        return FileResponse(byte_buffer, filename, as_attachment=True)
