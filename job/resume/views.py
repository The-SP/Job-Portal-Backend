from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import *
from .serializers import *


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Safe=GET
            return True
        # Check if the obj has any resume set and Allow write permission to owner only
        if not obj.resume_set.exists() or obj.resume_set.first().user != request.user:
            raise PermissionDenied(
                detail="You are not the owner of this resume object."
            )
        return True


class ResumeDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_object(self):
        return Resume.objects.get(user=self.request.user)


class EducationListCreateView(generics.ListCreateAPIView):
    """
    A view for handling the List and Create operations for Education model.
    """

    permission_classes = [IsAuthenticated]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def perform_create(self, serializer):
        education_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        # Add this education instance to the resume
        resume.education.add(education_instance)

    def get_queryset(self):
        """
        Overriding the get_queryset method to return only Education related to owner of the resume
        """
        resume = Resume.objects.get(user=self.request.user)
        return resume.education.all()


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class ExperienceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def perform_create(self, serializer):
        experience_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        resume.experience.add(experience_instance)

    def get_queryset(self):
        resume = Resume.objects.get(user=self.request.user)
        return resume.experience.all()


class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        project_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        resume.projects.add(project_instance)

    def get_queryset(self):
        resume = Resume.objects.get(user=self.request.user)
        return resume.projects.all()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SkillListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def perform_create(self, serializer):
        skill_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        resume.skills.add(skill_instance)

    def get_queryset(self):
        resume = Resume.objects.get(user=self.request.user)
        return resume.skills.all()


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class InterestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def perform_create(self, serializer):
        interest_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        resume.interests.add(interest_instance)

    def get_queryset(self):
        resume = Resume.objects.get(user=self.request.user)
        return resume.interests.all()


class InterestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


class AwardListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

    def perform_create(self, serializer):
        award_instance = serializer.save()
        resume = Resume.objects.get(user=self.request.user)
        resume.awards.add(award_instance)

    def get_queryset(self):
        resume = Resume.objects.get(user=self.request.user)
        return resume.awards.all()


class AwardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
