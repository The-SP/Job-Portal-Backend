from django.core.management.base import BaseCommand
import random, datetime

from user_system.models import SeekerProfile
from hiring.models import Job, JobApplication

class Command(BaseCommand):
    help = "Populate the Job Applications"

    def handle(self, *args, **options):
        # Choose job to populate its job_applications
        JOB_ID = 50
        job = Job.objects.get(pk=JOB_ID)
        seekers = SeekerProfile.objects.all()

        for seeker in seekers:
            phone_number = seeker.phone_number if seeker.phone_number else ""

            JobApplication.objects.create(
                user=seeker.user,
                job=job,
                name=seeker.name,
                email=seeker.email,
                phone_number=phone_number
            )

            self.stdout.write(
                f"{seeker.name} sent job application for job_id {JOB_ID}"
            )
