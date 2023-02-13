from django.core.management.base import BaseCommand
from django.db import transaction
import random, datetime
import pandas as pd

from user_system.models import EmployerProfile
from hiring.models import (
    Job,
    JOB_LEVEL_CHOICES,
    JOB_NATURE_CHOICES,
    EMPLOYMENT_TYPE_CHOICES,
)

education_levels = [
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "High School Diploma",
]


class Command(BaseCommand):
    help = "Populate the Job model with 20K datasets from csv"

    def handle(self, *args, **options):
        employer = EmployerProfile.objects.all()
        today_date = datetime.datetime.now().date()

        self.stdout.write("Reading around 20K jobs from csv")

        df_jobs = pd.read_csv("../Recommendation System/jobs_data.csv")

        # List to hold all the django job objects
        jobs = []

        for index, row in df_jobs.iterrows():
            company = random.choice(employer)

            """ Fields from df_jobs (csv dataset) """
            title = row["title"]
            description = row["description"]
            skill_required = row["skills"]
            # location = row['location']

            """Basic Information"""
            # title = random.choice(job_titles)
            location = company.company_location
            no_of_vacancy = random.randint(1, 10)
            salary_range = f"Rs. {random.randint(1, 40) * 10000}"

            deadline = today_date + datetime.timedelta(days=random.randint(14, 150))
            # Replace 150 with 30 * 5 or 30 * 4 to set the maximum range to 4 or 5 months, respectively.

            """Choice Fields"""
            job_level = random.choice(JOB_LEVEL_CHOICES)[0]
            employment_type = random.choice(EMPLOYMENT_TYPE_CHOICES)[0]
            job_nature = random.choice(JOB_NATURE_CHOICES)[0]

            """Specification"""
            education_level = random.choice(education_levels)
            experience_required = random.randint(0, 4)
            # random_skills = random.sample(skills, 3)
            # skill_required = ", ".join(random_skills)

            """Additional Description"""
            # description = random.choice(job_descriptions)

            """Company"""
            posted_by = company.user

            job = Job(
                title=title,
                location=location,
                no_of_vacancy=no_of_vacancy,
                salary_range=salary_range,
                deadline=deadline,
                job_level=job_level,
                employment_type=employment_type,
                job_nature=job_nature,
                education_level=education_level,
                experience_required=experience_required,
                skill_required=skill_required,
                description=description,
                posted_by=posted_by,
            )
            jobs.append(job)

        jobs_count = len(jobs)
        self.stdout.write(f'Saving {jobs_count} instances to database')
        # Use bulk_create to insert all the jobs in a single call
        with transaction.atomic():
            Job.objects.bulk_create(jobs)
        self.stdout.write(f'Successfully saved {jobs_count} instances to database')

        # bulk_create is used to insert all the jobs in the list in a single database call. The use of the transaction.atomic context manager ensures that the bulk insertion is treated as a single transaction, which can be rolled back if there is an error, ensuring that the database remains in a consistent state.
