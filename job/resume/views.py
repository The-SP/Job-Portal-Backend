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
