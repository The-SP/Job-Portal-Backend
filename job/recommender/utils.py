import re
from sklearn.metrics.pairwise import cosine_similarity


# Title should contain only characters, spaces and '+' (for C++)
def clean_job_title(title):
    # Include only characters and '+'
    text = re.sub("[^a-zA-Z\+]", " ", title)
    # Remove extra blank spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def clean_job_description(text):
    # Remove punctuation and numbers
    text = re.sub("[^a-zA-Z]", " ", text)
    # Remove extra blank spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Convert to lowercase
    text = text.lower()
    return text


def clean_skill(skill):
    return skill.replace(",", "").lower()


def clean_text(title, description, skills):
    # Clean title
    title = clean_job_title(title)
    # Clean description
    if skills:
        description = skills + " " + description
    if title:
        description = f"{title} {description}"
    description = clean_job_description(description)
    # Clean skills
    skills = clean_skill(skills)
    return title, description, skills


def compute_vectorizer_similarity(query, vectorizer, matrix):
    query_vec = vectorizer.transform([query])
    cosine_sim = cosine_similarity(query_vec, matrix)
    return cosine_sim


def compute_weighted_similarity_score(title_scores, description_scores, skills_scores):
    WEIGHT_TITLE = 0.4
    WEIGHT_DESCRIPTION = 0.2
    WEIGHT_SKILLS = 0.4
    cosine_sim_input = (
        WEIGHT_TITLE * title_scores
        + WEIGHT_DESCRIPTION * description_scores
        + WEIGHT_SKILLS * skills_scores
    )
    return cosine_sim_input
