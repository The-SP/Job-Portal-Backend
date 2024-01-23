import pandas as pd
from rest_framework import generics
from rest_framework.response import Response

from hiring.models import Job
from user_system.permissions import IsEmployer

from .ranking_algorithm.resume_parse import parse_resume_files
from .ranking_algorithm.applicant_ranking import ranking_algorithm


class ApplicantRankingView(generics.GenericAPIView):
    permission_classes = [IsEmployer]

    def get(self, request, *args, **kwargs):
        job_id = self.kwargs.get("pk")
        job = Job.objects.get(pk=job_id)
        applicants = job.applications.all()

        weights = {
            "description": 0.15,
            "education": 0.2,
            "experience": 0.35,
            "skills": 0.2,
            "projects": 0.1,
        }

        target_job = {
            "title": job.title,
            "description": job.description,
            "skills": job.skill_required,
            "education": str(job.education_level)
            + " "
            + str(job.education_field_of_study),
            "experience": job.experience_required,
        }

        # Filter applicants who have resumes in pdf
        applicants_with_resume = [
            {
                "id": applicant.id,
                "name": applicant.name,
                "resume_url": applicant.resume.url.lstrip("/"),
                "status": applicant.status,
            }
            for applicant in applicants
            if applicant.resume and applicant.resume.url.endswith(".pdf")
        ]

        # Extract only resume_path list from filtered_applicants
        # resume.url gives '/media/job_19733_resumes/backend.pdf', so need to remove the starting '/' using lstrip('/')
        resume_paths = [applicant["resume_url"] for applicant in applicants_with_resume]

        print("\nProcessing uploaded resumes to extract relevant information...")
        parse_resume_files(resume_paths)

        print("\n\nEvaluating candidates...")
        df_resume = ranking_algorithm(target_job, weights)

        # Convert applicants_with_resume dictionary to a DataFrame
        df_applicants = pd.DataFrame(applicants_with_resume)
        # Concatenate df_applicants with df_resume
        df_resume_rankings = pd.concat([df_resume, df_applicants], axis=1)

        # Sort the DataFrame based on total_score in descending order
        df_resume_rankings_sorted = df_resume_rankings.sort_values(
            by="total_score", ascending=False
        )

        return Response(df_resume_rankings_sorted.to_dict(orient="records"))
