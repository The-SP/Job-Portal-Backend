import pandas as pd
import ast
from rest_framework import generics

from user_system.permissions import IsEmployer, IsJobOwner, IsSeeker, IsApplicationOwner
from .models import *
from .serializers import *

# List all jobs with few info to all users (no login required)
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = ShortJobSerializer


# This view will handle retrieving a single job based on the primary key passed in the URL.
class JobRetrieveView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# List all jobs (with few info) posted by logged_in Employer
class EmployerJobListView(generics.ListAPIView):
    serializer_class = ShortJobSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).order_by('-created_at')


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
        jobs1 = pd.read_csv("scrapper/jobs_csv/jobs1.csv")
        jobs2 = pd.read_csv("scrapper/jobs_csv/jobs2.csv")
        # tags is stored as string so, convert back to list of string
        jobs1["tags"] = jobs1["tags"].apply(lambda x: ast.literal_eval(x))
        jobs2["tags"] = jobs2["tags"].apply(lambda x: ast.literal_eval(x))
        # Convert pandas dataframe to list of dictionaries
        jobs_list = jobs1.to_dict(orient="records") + jobs2.to_dict(orient="records")
        return jobs_list


""" Views for Job Applications """


class ApplicationCreateView(generics.CreateAPIView):
    permission_classes = [IsSeeker]
    queryset = JobApplication.objects.all()
    serializer_class = CreateJobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Allow owner of the job-application to update and delete
class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSeeker, IsApplicationOwner]
    queryset = JobApplication.objects.all()
    serializer_class = CreateJobApplicationSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserApplicationListView(generics.ListAPIView):
    permission_classes = [IsSeeker]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        return self.request.user.applications.all().order_by('-created_at')


class GetApplicationsForJob(generics.ListAPIView):
    permission_classes = [IsEmployer]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return JobApplication.objects.filter(job_id=job_id, job__posted_by=self.request.user)