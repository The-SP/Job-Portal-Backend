import pandas as pd
import ast
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from user_system.permissions import IsEmployer, IsJobOwner
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
