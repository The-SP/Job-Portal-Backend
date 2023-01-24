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


# Web Scraping
class ScrapedJobSerializer(serializers.Serializer):
    logo_url = serializers.URLField()
    url = serializers.URLField()
    title = serializers.CharField()
    company = serializers.CharField()
    location = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    salary = serializers.CharField()
    deadline = serializers.CharField()


""" Serializer for Job Application """


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"


class CreateJobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobApplication
        fields = "__all__"
