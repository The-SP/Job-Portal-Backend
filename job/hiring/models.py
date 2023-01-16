from django.db import models

from user_system.models import UserAccount


JOB_LEVEL_CHOICES = (
    ("entry", "Entry"),
    ("intern", "Intern"),
    ("mid", "Mid"),
    ("senior", "Senior"),
)

EMPLOYMENT_TYPE_CHOICES = (
    ("full-time", "Full-time"),
    ("part-time", "Part-time"),
    ("contract", "Contract"),
    ("intern", "Intern"),
    ("freelance", "Freelance"),
)

JOB_LOCATION_CHOICES = (
    ("remote", "Remote"),
    ("work-from-home", "Work-from-home"),
    ("office", "Office"),
)


class BasicInformation(models.Model):
    category = models.CharField(max_length=255)
    job_level = models.CharField(max_length=255, choices=JOB_LEVEL_CHOICES)
    no_of_vacancy = models.IntegerField()
    employment_type = models.CharField(max_length=255, choices=EMPLOYMENT_TYPE_CHOICES)
    job_location = models.CharField(max_length=255, choices=JOB_LOCATION_CHOICES)
    salary_range = models.CharField(max_length=255)
    deadline = models.DateField()


class Specification(models.Model):
    education_level = models.CharField(max_length=255, null=True, blank=True)
    experience_required = models.IntegerField(null=True, blank=True)
    skill_required = models.TextField(null=True, blank=True)


class Description(models.Model):
    tasks = models.TextField(null=True, blank=True)
    perks_and_benefits = models.TextField(null=True, blank=True)


class Job(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="jobs_posted"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    basic_info = models.OneToOneField(BasicInformation, on_delete=models.CASCADE)
    specification = models.OneToOneField(
        Specification, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.OneToOneField(
        Description, on_delete=models.CASCADE, null=True, blank=True
    )
