# Generated by Django 4.1.4 on 2023-02-11 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_system", "0009_seekerprofile_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="seekerprofile",
            old_name="title",
            new_name="job_title",
        ),
    ]
