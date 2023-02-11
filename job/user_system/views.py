from rest_framework import generics

from user_system.models import SeekerProfile, EmployerProfile
from user_system.serializers import SeekerProfileSerializer, EmployerProfileSerializer
from user_system.permissions import IsSeeker, IsEmployer


"""
Profile Create is handled automatically on user signup using signals.
"""
# class ProfileCreate(generics.CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class SeekerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSeeker]
    queryset = SeekerProfile.objects.all()
    serializer_class = SeekerProfileSerializer

    def get_object(self):
        return SeekerProfile.objects.get(user=self.request.user)


class EmployerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsEmployer]
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)


# Allow all users to view company details
class CompanyProfileView(generics.RetrieveAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer


# Allow employers to view seeker(applicant) details
class ApplicantProfileView(generics.RetrieveAPIView):
    queryset = SeekerProfile.objects.all()
    serializer_class = SeekerProfileSerializer
