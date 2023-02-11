from rest_framework import generics
from rest_framework.response import Response

from .job_recommender import get_recommendations
from user_system.models import SeekerProfile
from user_system.permissions import IsSeeker


class JobRecommendationsList(generics.GenericAPIView):
    permission_classes = [IsSeeker]

    def get(self, request, *args, **kwargs):
        seeker = SeekerProfile.objects.get(user=request.user)

        input_title = seeker.job_title if seeker.job_title else ""
        input_description = seeker.bio if seeker.bio else ""
        input_skills = seeker.skills if seeker.skills else ""
        recommended_jobs = get_recommendations(
            input_title, input_description, input_skills
        )

        return Response(recommended_jobs.to_dict(orient="records"))
