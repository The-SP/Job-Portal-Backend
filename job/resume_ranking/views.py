from rest_framework import generics
from rest_framework.response import Response

from hiring.models import Job, JobApplication
from hiring.serializers import GetApplicationsForJobSerializer
from user_system.permissions import IsEmployer


class ApplicantRankingView(generics.GenericAPIView):
    permission_classes = [IsEmployer]

    def get(self, request, *args, **kwargs):
        job_id = self.kwargs.get("pk")
        job = Job.objects.get(pk=job_id)
        applicants = job.applications.all()

        serializer = GetApplicationsForJobSerializer(applicants, many=True)
        return Response(serializer.data)
