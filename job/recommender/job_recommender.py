import pandas as pd
import numpy as np
import pickle

from hiring.models import Job
from user_system.models import EmployerProfile

from recommender.utils import (
    clean_text,
    compute_vectorizer_similarity,
    compute_weighted_similarity_score,
)


def get_recommendations(title, description, skills):
    # Load vectorizer and matrices from pickle file
    try:
        with open("recommender/recommendation_data.pkl", "rb") as f:
            data = pickle.load(f)
            title_vectorizer = data["title_vectorizer"]
            description_vectorizer = data["description_vectorizer"]
            skills_vectorizer = data["skills_vectorizer"]
            title_matrix = data["title_matrix"]
            description_matrix = data["description_matrix"]
            skills_matrix = data["skills_matrix"]
            df_jobs = data.get("df_jobs", pd.DataFrame())

        print("Vectorizer and matrices loaded from recommendation_data.pkl.")
    except FileNotFoundError:
        print(
            "Pickle file not found. Run the update_recommendations management command first."
        )
        exit()

    # If no records don't do processing
    if df_jobs.empty:
        return df_jobs

    title, description, skills = clean_text(title, description, skills)

    # Compute vectorizer and cosine similarity scores for job title, job description and skills
    cosine_sim_title = compute_vectorizer_similarity(
        title, title_vectorizer, title_matrix
    )
    cosine_sim_description = compute_vectorizer_similarity(
        description, description_vectorizer, description_matrix
    )
    cosine_sim_skills = compute_vectorizer_similarity(
        skills, skills_vectorizer, skills_matrix
    )

    # Combine the cosine similarity scores
    cosine_sim_input = compute_weighted_similarity_score(
        cosine_sim_title, cosine_sim_description, cosine_sim_skills
    )

    # Find the indices of the top N jobs with the highest cosine similarity scores
    N = 20
    top_n_indices = np.argsort(-cosine_sim_input[0])[:N]

    # Return the top N jobs with the highest cosine similarity scores
    results = df_jobs.iloc[top_n_indices]

    # Add the similarity percentage scores to the results dataframe
    results = results.copy()
    # Get the similarity scores of the recommended jobs
    similarity_scores = cosine_sim_input[0][top_n_indices]
    similarity_scores *= 100
    similarity_scores = [round(score, 2) for score in similarity_scores]
    results["similarity_scores"] = similarity_scores
    results["company"] = results.apply(
        lambda x: EmployerProfile.objects.get(user=x["posted_by_id"]).company_name,
        axis=1,
    )

    # Get the job IDs from the top N indices
    top_n_job_ids = results["id"].tolist()

    # Filter the top_n_job_ids to only include IDs that exist in Job.objects
    # This is needed because the pickle file may contain some deleted jobs
    existing_job_ids = Job.objects.values_list("id", flat=True)
    valid_top_n_job_ids = [
        job_id for job_id in top_n_job_ids if job_id in existing_job_ids
    ]

    # Filter the results to only include rows with job IDs that exist in Job.objects
    results = results[results["id"].isin(valid_top_n_job_ids)]

    return results
