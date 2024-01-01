import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from hiring.models import Job
from user_system.models import EmployerProfile

from recommender.utils import (
    clean_job_title,
    clean_job_description,
    clean_skill,
    clean_text,
    compute_vectorizer_similarity,
    compute_weighted_similarity_score,
)


# df_jobs = pd.read_csv("../Recommendation System/jobs_data.csv")

# get all the jobs as a queryset from the database
jobs_qs = Job.objects.all()
# convert the queryset to a list
jobs_list = list(jobs_qs.values())

df_jobs = pd.DataFrame()  # Initialize empty dataframe first
if jobs_list:
    # convert the list of jobs to a pandas dataframe
    df_jobs = pd.DataFrame.from_records(jobs_list)

    # Clean jobtitle, jobdescription and skills
    print("Cleaning job titles, job descriptions, and skills...")

    df_clean_title = df_jobs["title"].apply(clean_job_title)
    df_clean_description = df_jobs["description"].apply(clean_job_description)
    df_clean_skills = df_jobs["skill_required"].apply(clean_skill)

    # Initialize the TfidfVectorizer
    title_vectorizer = CountVectorizer()
    description_vectorizer = TfidfVectorizer(stop_words="english", min_df=0.01)
    skills_vectorizer = CountVectorizer(ngram_range=(1, 3))

    print("Creating vector representations for job titles, descriptions, and skills...")

    # fit_transform the vectorizers and create tfidf matrix
    title_matrix = title_vectorizer.fit_transform(df_clean_title)
    description_matrix = description_vectorizer.fit_transform(df_clean_description)
    skills_matrix = skills_vectorizer.fit_transform(df_clean_skills)

    print(
        "Vector representations successfully created for job titles, descriptions, and skills."
    )


def get_recommendations(title, description, skills):
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

    return results
