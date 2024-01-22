from rest_framework import serializers

from .models import *


class GetApplicationsForJobSerializer(serializers.ModelSerializer):
    seeker_id = serializers.PrimaryKeyRelatedField(source="user.id", read_only=True)
    job_title = serializers.CharField(source="job.title")

    class Meta:
        model = JobApplication
        fields = "__all__"


class CreateJobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobApplication
        fields = "__all__"


class SeekerApplicationsListSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(source="job.id", read_only=True)
    job_title = serializers.CharField(source="job.title")
    posted_by = serializers.PrimaryKeyRelatedField(
        source="job.posted_by", read_only=True
    )
    company = serializers.CharField(source="job.posted_by.company.company_name")

    class Meta:
        model = JobApplication
        fields = [
            "job_id",
            "job_title",
            "posted_by",
            "company",
            "id",
            "created_at",
            "resume",
            "status"
        ]
