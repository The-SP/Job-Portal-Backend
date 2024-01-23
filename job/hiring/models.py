from django.db import models

from user_system.models import UserAccount


JOB_LEVEL_CHOICES = (
    ("Entry", "Entry"),
    ("Intern", "Intern"),
    ("Mid", "Mid"),
    ("Senior", "Senior"),
)

EMPLOYMENT_TYPE_CHOICES = (
    ("Full-time", "Full-time"),
    ("Part-time", "Part-time"),
    ("Contract", "Contract"),
    ("Intern", "Intern"),
    ("Freelance", "Freelance"),
)

JOB_NATURE_CHOICES = (
    ("Remote", "Remote"),
    ("Work-from-home", "Work-from-home"),
    ("Office", "Office"),
)


class Job(models.Model):

    """Basic Information"""

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    no_of_vacancy = models.IntegerField()
    salary_range = models.CharField(max_length=255)
    deadline = models.DateField()

    """ Choice Fields """
    job_level = models.CharField(max_length=255, choices=JOB_LEVEL_CHOICES)
    employment_type = models.CharField(max_length=255, choices=EMPLOYMENT_TYPE_CHOICES)
    job_nature = models.CharField(max_length=255, choices=JOB_NATURE_CHOICES)

    """ Specification """
    education_level = models.CharField(max_length=255, null=True, blank=True)
    education_field_of_study = models.CharField(max_length=255, null=True, blank=True)
    experience_required = models.IntegerField(null=True, blank=True)
    skill_required = models.TextField(null=True, blank=True)

    """ Additional Description """
    description = models.TextField(null=True, blank=True)

    """ Company """
    posted_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="jobs_posted"
    )

    """ Dates """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bookmark(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="bookmarks"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
