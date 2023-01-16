from rest_framework import serializers

from .models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class ShortJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "category",
            "job_level",
            "salary_range",
            "deadline",
            "posted_by",
        )

# HiddenField is used to hide the posted_by field in the serializer while still setting the current user as the default value.It will still be passed to the serializer and saved to the database, but it will not be displayed to the user.
class CreateJobSerializer(serializers.ModelSerializer):
    posted_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = "__all__"
