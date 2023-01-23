import pandas as pd
import ast
from rest_framework import generics

from user_system.permissions import IsEmployer, IsJobOwner
from .models import *
from .serializers import *

# List all jobs with few info to all users (no login required)
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
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
        return Job.objects.filter(posted_by=self.request.user)


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
        jobs1 = pd.read_csv('scrapper/jobs_csv/jobs1.csv')
        jobs2 = pd.read_csv('scrapper/jobs_csv/jobs2.csv')
        # tags is stored as string so, convert back to list of string
        jobs1['tags'] = jobs1['tags'].apply(lambda x: ast.literal_eval(x))
        jobs2['tags'] = jobs2['tags'].apply(lambda x: ast.literal_eval(x))
        # Convert pandas dataframe to list of dictionaries
        jobs_list = jobs1.to_dict(orient='records') + jobs2.to_dict(orient='records')
        return jobs_list
