from rest_framework import serializers
from datetime import datetime

from .models import *
from user_system.models import EmployerProfile
from user_system.serializers import EmployerProfileSerializer


class JobSerializer(serializers.ModelSerializer):
    company = EmployerProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    # Get the details of Company
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Get the profile from posted_by then add it to the JobSerializer data
        representation["company"] = EmployerProfileSerializer(
            EmployerProfile.objects.get(user=instance.posted_by)
        ).data
        return representation


class ShortJobSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    deadline_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "location",
            "job_level",
            "salary_range",
            "deadline",
            "posted_by",
            "company",
            "deadline_remaining",
        )

    # Get the name of Company
    def get_company(self, job_obj):
        company = EmployerProfile.objects.get(user=job_obj.posted_by)
        return company.company_name

    # Get deadline in terms of 'x week, y days'
    def get_deadline_remaining(self, obj):
        today = datetime.now().date()
        delta = obj.deadline - today
        remaining = ""
        if delta.days <= 0:
            remaining = "Expired"
        else:
            months = delta.days // 30
            weeks = (delta.days % 30) // 7
            days = (delta.days % 30) % 7
            if months > 0:
                remaining += f"{months} month{'s' if months > 1 else ''}, "
            if weeks > 0:
                remaining += f"{weeks} week{'s' if weeks > 1 else ''}, "
            if days > 0:
                remaining += f"{days} day{'s' if days > 1 else ''}, "
            remaining = remaining[:-2]  # remove ', ' at end
        return remaining.strip()


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


class GetApplicationsForJobSerializer(serializers.ModelSerializer):
    seeker_id = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    class Meta:
        model = JobApplication
        fields = "__all__"

    def get_seeker_id(self, application_obj):
        return application_obj.user.id

    def get_job_title(self, application_obj):
        return application_obj.job.title


class CreateJobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = JobApplication
        fields = "__all__"
