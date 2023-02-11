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

JOB_NATURE_CHOICES = (
    ("remote", "Remote"),
    ("work-from-home", "Work-from-home"),
    ("office", "Office"),
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


class JobApplication(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    # resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application for {self.job.title} by {self.user.name}"
