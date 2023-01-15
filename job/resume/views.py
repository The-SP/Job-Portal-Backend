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
        # Allow write permission to owner only
        if obj.resume_set.first().user != request.user:
            raise PermissionDenied(
                detail="You are not the owner of this resume object."
            )
        return True


class EducationCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def perform_create(self, serializer):
        education_instance = serializer.save()
        resume, created = Resume.objects.get_or_create(user=self.request.user)
        resume.education.add(education_instance)
        print(education_instance, resume.education.all(), created)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
