# Generated by Django 4.1.4 on 2023-01-26 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_system", "0006_rename_first_name_seekerprofile_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="seekerprofile",
            old_name="phone",
            new_name="phone_number",
        ),
    ]
