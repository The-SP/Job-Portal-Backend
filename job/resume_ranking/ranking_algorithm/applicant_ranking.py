import pandas as pd

from .description_score import get_description_score
from .skill_score import get_skills_score, get_projects_score
from .education_score import get_education_score
from .experience_score import get_experience_score
from .total_score import calculate_total_score, convert_to_percentage


def ranking_algorithm(target_job, weights):
    df_resume = pd.read_csv("media/resume_sections.csv")
    df_resume.fillna("", inplace=True)

    print()
    print("Calculating description score...")
    get_description_score(df_resume, target_job)

    print("Calculating skills score...")
    get_skills_score(df_resume, target_job)

    print("Calculating projects score...")
    get_projects_score(df_resume, target_job)

    print("Calculating education score...")
    get_education_score(df_resume, target_job)

    print("Calculating experience score...")
    get_experience_score(df_resume, target_job)

    print("Calculating Total score...")
    df_resume = calculate_total_score(df_resume, weights)

    print("\nEvaluation complete.")

    df_resume = df_resume[
        [
            "Filename",
            "description_score",
            "skills_score",
            "projects_score",
            "education_score",
            "experience_score",
            "total_score",
        ]
    ]

    df_resume = convert_to_percentage(df_resume)

    return df_resume
