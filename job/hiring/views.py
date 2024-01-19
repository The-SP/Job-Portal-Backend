import pandas as pd
import ast
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import LimitOffsetPagination
from io import BytesIO
from django.http import FileResponse
from rest_framework.views import APIView

from user_system.permissions import IsEmployer, IsJobOwner, IsSeeker, IsApplicationOwner
from .models import *
from .serializers import *


# List all jobs with few info to all users (no login required)
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by("-created_at")[:100]
    serializer_class = ShortJobSerializer

    # With this setup, you can specify the number of jobs you want to return in the API request by passing the limit parameter. For example, if you want to return the first 100 jobs, you would make a request to /jobs/?limit=100. If you don't specify the limit parameter, the default value of 100 will be used.
    # pagination_class = LimitOffsetPagination
    # pagination_class.default_limit = 100


# This view will handle retrieving a single job based on the primary key passed in the URL.
class JobRetrieveView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# List all jobs (with few info) posted by logged_in Employer
class EmployerJobListView(generics.ListAPIView):
    serializer_class = ShortJobSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).order_by("-created_at")[
            :50
        ]


# Allow only employer user to create new jobs
class JobCreateView(generics.CreateAPIView):
    permission_classes = [IsEmployer]
    queryset = Job.objects.all()
    serializer_class = CreateJobSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


# Allow owner of the job to update and delete the job
class JobUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsEmployer, IsJobOwner]
    queryset = Job.objects.all()
    serializer_class = CreateJobSerializer

    def perform_update(self, serializer):
        serializer.save(posted_by=self.request.user)


# Web Scraping
# List all jobs with few info
class ScrapedJobListView(generics.ListAPIView):
    serializer_class = ScrapedJobSerializer

    def get_queryset(self):
        jobs = pd.read_csv("scrapper/jobs_csv/jobs.csv")
        # tags is stored as string so, convert back to list of string
        jobs["tags"] = jobs["tags"].apply(lambda x: ast.literal_eval(x))
        # Convert pandas dataframe to list of dictionaries
        jobs_list = jobs.to_dict(orient="records")
        return jobs_list


""" Views for Job Applications """


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

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


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
