from django.core.management.base import BaseCommand
import os
from user_system.models import SeekerProfile
from hiring.models import Job
from job_applications.models import JobApplication


class Command(BaseCommand):
    help = "Populate the Job Applications"

    def handle(self, *args, **options):
        # Choose job to populate its job_applications
        JOB_ID = 39434
        job = Job.objects.get(pk=JOB_ID)

        # Delete all job applications for the selected job
        # job.applications.all().delete()
        # self.stdout.write(f"Deleted job applications for job_id {JOB_ID}.")
        # return

        seekers = SeekerProfile.objects.all()

        resume_inputs_path = "media/job_39434_resumes"
        resume_files = [f for f in os.listdir(resume_inputs_path) if f.endswith(".pdf")]

        self.stdout.write(f"Creating job applications for job_id {JOB_ID}.\n")

        for seeker in seekers:
            phone_number = seeker.phone_number if seeker.phone_number else ""

            # Ensure there are resume files available
            if resume_files:
                # Assign resumes sequentially to seekers
                resume_file = resume_files.pop(0)
                resume_path = os.path.join(resume_inputs_path, resume_file)

                resume_path = os.path.join("job_39434_resumes", resume_file)

                JobApplication.objects.create(
                    user=seeker.user,
                    job=job,
                    name=seeker.name,
                    email=seeker.email,
                    phone_number=phone_number,
                    resume=resume_path,
                )

                self.stdout.write(
                    f"{seeker.name} applied with resume {resume_file}"
                )
            else:
                self.stdout.write(
                    f"No resume found for {seeker.name}. Skipped job application for job_id {JOB_ID}"
                )
