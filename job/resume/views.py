from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import *
from .serializers import *


class EducationCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def perform_create(self, serializer):
        education_instance = serializer.save()
        resume, created = Resume.objects.get_or_create(user=self.request.user)
        resume.education.add(education_instance)
        print(education_instance, resume.education.all())


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def perform_update(self, serializer):
        if self.get_object().resume_set.first().user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You are not the owner of this resume")

    def perform_destroy(self, instance):
        if instance.resume_set.first().user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You are not the owner of this resume")
