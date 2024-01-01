from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime, timedelta
import random

from hiring.models import Job


class Command(BaseCommand):
    help = "Update the deadline field for existing Job objects using bulk update"

    def handle(self, *args, **options):
        today_date = datetime.now().date()

        self.stdout.write("Fetching all existing jobs from database")

        # Fetch all existing jobs
        jobs = Job.objects.all()
        jobs_count = len(jobs)

        self.stdout.write("Generating random deadline for each job")

        # Prepare a dictionary with updated deadlines for each job
        updated_jobs = [
            Job(id=job.id, deadline=today_date + timedelta(days=random.randint(14, 150)))
            for job in jobs
        ]

        self.stdout.write(f"Updating {jobs_count} job instances to database...")
        # Perform the bulk update within a transaction
        with transaction.atomic():
            Job.objects.bulk_update(updated_jobs, ["deadline"])

        self.stdout.write(f"Successfully updated deadline for {jobs_count} jobs.")
