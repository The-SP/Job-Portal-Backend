from rest_framework import serializers
from .models import Resume, Education, Skill, Experience, Project, Interest, Award


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    skills = SkillSerializer(many=True)
    experience = ExperienceSerializer(many=True)
    projects = ProjectSerializer(many=True)
    interests = InterestSerializer(many=True)
    awards = AwardSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Resume
        fields = (
            "bio",
            "education",
            "skills",
            "experience",
            "projects",
            "interests",
            "awards",
            "user",
        )
