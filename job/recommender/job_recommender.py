import pandas as pd
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Title should contain only characters, spaces and '+' (for C++)
def clean_job_title(title):
    return re.sub(r"[^a-zA-Z\s\+]", " ", title).lower()


def clean_job_description(text):
    # Remove punctuation and numbers
    text = re.sub("[^a-zA-Z]", " ", text)
    # Convert to lowercase
    text = text.lower()
    return text


# Remove ',' and convert to lowercase
def clean_skill(skill):
    return skill.replace(",", "").lower()


df_jobs = pd.read_csv("../Recommendation System/jobs_data.csv")

# Clean jobtitle, jobdescription and skills
df_clean_title = df_jobs["jobtitle"].apply(clean_job_title)
df_clean_description = df_jobs["jobdescription"].apply(clean_job_description)
df_clean_skills = df_jobs["skills"].apply(clean_skill)

# Initialize the TfidfVectorizer
title_vectorizer = CountVectorizer()
description_vectorizer = TfidfVectorizer(stop_words="english")
skills_vectorizer = CountVectorizer(ngram_range=(1, 3))


# fit_transform the vectorizers and create tfidf matrix
title_matrix = title_vectorizer.fit_transform(df_clean_title)
description_matrix = description_vectorizer.fit_transform(df_clean_description)
skills_matrix = skills_vectorizer.fit_transform(df_clean_skills)


def get_recommendations(title, description, skills):
    # Clean input title
    title = clean_job_title(title)
    # Clean input description
    if skills:
        description = " ".join(skills) + " " + description
    if title:
        description = f"{title} {description}"
    description = clean_job_description(description)
    # Clean input skills
    skills = clean_skill(skills)

    # Compute vectorizer
    query_title_vec = title_vectorizer.transform([title])
    query_description_vec = description_vectorizer.transform([description])
    query_skills_vec = skills_vectorizer.transform([skills])

    # Compute cosine similarity
    cosine_sim_title = cosine_similarity(query_title_vec, title_matrix)
    cosine_sim_description = cosine_similarity(
        query_description_vec, description_matrix
    )
    cosine_sim_skills = cosine_similarity(query_skills_vec, skills_matrix)

    # Combine the cosine similarity scores for job title and job description
    weight_title = 0.4
    weight_description = 0.2
    weight_skills = 0.4
    cosine_sim_input = (
        weight_title * cosine_sim_title
        + weight_description * cosine_sim_description
        + weight_skills * cosine_sim_skills
    )

    # Find the indices of the top N jobs with the highest cosine similarity scores
    N = 20
    top_n_indices = np.argsort(-cosine_sim_input[0])[:N]

    # Get the similarity scores of the recommended jobs
    similarity_scores = cosine_sim_input[0][top_n_indices]
    # print("Similarity Scores:", similarity_scores)

    # Return the top N jobs with the highest cosine similarity scores
    results = df_jobs.iloc[top_n_indices]

    # Add the similarity percentage scores to the results dataframe
    results = results.copy()
    similarity_scores *= 100
    similarity_scores = [round(score, 2) for score in similarity_scores]
    results["similarity_scores"] = similarity_scores

    return results
