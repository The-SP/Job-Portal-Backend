import pandas as pd
import pickle

from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from hiring.models import Job
from recommender.utils import (
    clean_job_title,
    clean_job_description,
    clean_skill,
)


class Command(BaseCommand):
    help = "Update recommendations and save vectorizer and matrices in a pickle file"

    def handle(self, *args, **options):
        # Get all the jobs as a queryset from the database
        jobs_qs = Job.objects.all()
        # Convert the queryset to a list
        jobs_list = list(jobs_qs.values())

        df_jobs = pd.DataFrame()  # Initialize empty dataframe first
        if jobs_list:
            # Convert the list of jobs to a pandas dataframe
            df_jobs = pd.DataFrame.from_records(jobs_list)

            # Clean jobtitle, jobdescription, and skills
            self.stdout.write(
                self.style.SUCCESS(
                    "Cleaning job titles, job descriptions, and skills..."
                )
            )
            df_clean_title = df_jobs["title"].apply(clean_job_title)
            df_clean_description = df_jobs["description"].apply(clean_job_description)
            df_clean_skills = df_jobs["skill_required"].apply(clean_skill)

            # Initialize the TfidfVectorizer
            title_vectorizer = CountVectorizer()
            description_vectorizer = TfidfVectorizer(stop_words="english", min_df=0.01)
            skills_vectorizer = CountVectorizer(ngram_range=(1, 3))

            self.stdout.write(self.style.SUCCESS("Creating vector representations..."))

            # Fit_transform the vectorizers and create matrices
            title_matrix = title_vectorizer.fit_transform(df_clean_title)
            description_matrix = description_vectorizer.fit_transform(
                df_clean_description
            )
            skills_matrix = skills_vectorizer.fit_transform(df_clean_skills)

            self.stdout.write(
                self.style.SUCCESS("Vector representations successfully created.")
            )

            # Save vectorizer and matrices to a pickle file
            with open("recommender/recommendation_data.pkl", "wb") as f:
                pickle.dump(
                    {
                        "title_vectorizer": title_vectorizer,
                        "description_vectorizer": description_vectorizer,
                        "skills_vectorizer": skills_vectorizer,
                        "title_matrix": title_matrix,
                        "description_matrix": description_matrix,
                        "skills_matrix": skills_matrix,
                        "df_jobs": df_jobs,
                    },
                    f,
                )

            self.stdout.write(
                self.style.SUCCESS(
                    "Vectorizer and matrices saved to recommendation_data.pkl"
                )
            )
