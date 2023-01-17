from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from user_system.models import SeekerProfile,EmployerProfile

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "is_employer", "password")


class SeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeekerProfile
        exclude = ('user', 'created')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return SeekerProfile.objects.create(**validated_data)

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        exclude = ('user', 'created')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return EmployerProfile.objects.create(**validated_data)