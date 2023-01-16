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
