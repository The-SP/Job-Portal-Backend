from rest_framework import serializers

from .models import *


class BasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInformation
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = "__all__"


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    basic_info = BasicInformationSerializer()
    specification = SpecificationSerializer()
    description = DescriptionSerializer()
    posted_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "posted_by",
            "created_at",
            "basic_info",
            "specification",
            "description",
        )
