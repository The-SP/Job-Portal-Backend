# Generated by Django 4.1.4 on 2023-02-11 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hiring", "0005_alter_job_location"),
    ]

    operations = [
        migrations.RenameField(
            model_name="job",
            old_name="tasks",
            new_name="description",
        ),
        migrations.RemoveField(
            model_name="job",
            name="perks_and_benefits",
        ),
    ]
