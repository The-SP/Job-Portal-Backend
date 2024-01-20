import pandas as pd
import ast
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView


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


""" Views for Bookmark feature """


class BookmarkCreateView(generics.CreateAPIView):
    serializer_class = BookmarkSerializer

    def create(self, request, *args, **kwargs):
        job_id = self.kwargs["job_id"]
        job = Job.objects.get(pk=job_id)
        bookmark = Bookmark.objects.create(user=request.user, job=job)
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarkDestroyView(APIView):
    serializer_class = BookmarkSerializer

    def delete(self, request, *args, **kwargs):
        job_id = self.kwargs["job_id"]
        try:
            bookmark = Bookmark.objects.filter(user=request.user, job__id=job_id)
            bookmark.delete()
            # Return a successful response with status code 204 (No Content)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Bookmark.DoesNotExist:
            return Response(
                {"detail": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND
            )


class BookmarkListView(generics.ListAPIView):
    serializer_class = ShortJobSerializer

    def get_queryset(self):
        # Get a list of job IDs bookmarked by the user
        bookmarked_job_ids = Bookmark.objects.filter(
            user=self.request.user
        ).values_list("job", flat=True)

        # Retrieve the corresponding Job objects
        jobs = Job.objects.filter(id__in=bookmarked_job_ids)

        return jobs
