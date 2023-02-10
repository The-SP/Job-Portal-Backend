from rest_framework import generics
from rest_framework.response import Response

from .job_recommender import get_recommendations
from user_system.models import SeekerProfile
from user_system.permissions import IsSeeker

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class JobRecommendationsList(generics.GenericAPIView):
    permission_classes = [IsSeeker]

    def get(self, request, *args, **kwargs):
        seeker = SeekerProfile.objects.get(user=request.user)

        input_title = "backend"
        input_description = seeker.bio
        input_skills = ["python"]

        recommended_jobs = get_recommendations(input_title, input_description, input_skills)
        print(recommended_jobs.info())
        print(recommended_jobs.head(5))

        return Response(recommended_jobs.to_dict(orient='records'))

