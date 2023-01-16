from rest_framework import generics

from user_system.permissions import IsSeeker, IsOwner
from .models import *
from .serializers import *


class ResumeDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSeeker, IsOwner]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_object(self):
        return Resume.objects.get(user=self.request.user)


class EducationListCreateView(generics.ListCreateAPIView):
    """
    A view for handling the List and Create operations for Education model.
    """

    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class ExperienceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SkillListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class InterestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


class AwardListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeeker]
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
    permission_classes = [IsSeeker, IsOwner]
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
