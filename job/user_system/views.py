from rest_framework import generics

from user_system.models import Profile
from user_system.serializers import ProfileSerializer
from user_system.permissions import IsSeeker


"""
Profile Create (for Seeker only) is handled automatically on user signup using signals.
"""
# class ProfileCreate(generics.CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsSeeker]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
