# Generated by Django 4.1.4 on 2023-01-14 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Award",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("date", models.DateField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("degree", models.CharField(max_length=100)),
                ("university", models.CharField(max_length=100)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("current", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("company", models.CharField(max_length=100)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("current", models.BooleanField(default=False)),
                ("duties", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Interest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("current", models.BooleanField(default=False)),
                ("url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True)),
                ("awards", models.ManyToManyField(to="resume.award")),
                ("education", models.ManyToManyField(to="resume.education")),
                ("experience", models.ManyToManyField(to="resume.experience")),
                ("interests", models.ManyToManyField(to="resume.interest")),
                ("projects", models.ManyToManyField(to="resume.project")),
                ("skills", models.ManyToManyField(to="resume.skill")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
