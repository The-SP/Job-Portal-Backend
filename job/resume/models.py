from django.db import models
from user_system.models import UserAccount


class Education(models.Model):
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    # level = models.CharField(max_length=100, blank=True, null=True)


class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    duties = models.TextField(blank=True, null=True)


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)


class Interest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class Award(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Resume(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    education = models.ManyToManyField(Education)
    skills = models.ManyToManyField(Skill)
    experience = models.ManyToManyField(Experience)
    projects = models.ManyToManyField(Project)
    interests = models.ManyToManyField(Interest)
    awards = models.ManyToManyField(Award)
