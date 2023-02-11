from django.core.management.base import BaseCommand
import random, datetime

from user_system.models import EmployerProfile
from hiring.models import (
    Job,
    JOB_LEVEL_CHOICES,
    JOB_NATURE_CHOICES,
    EMPLOYMENT_TYPE_CHOICES,
)

education_levels = [
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "High School Diploma",
]
job_titles = [
    "Software Engineer",
    "Full Stack Developer",
    "Data Scientist",
    "DevOps Engineer",
    "Product Manager",
    "UX Designer",
    "Machine Learning Engineer",
    "Mobile Developer",
    "Front-End Developer",
    "Back-End Developer",
]
skills = [
    "C",
    "Python",
    "JavaScript",
    "SQL",
    "React",
    "Node.js",
    "Django",
    "Angular",
    "JS",
    "Java",
    "C++",
    "Go",
]
job_descriptions = [
    "We're seeking a highly motivated software engineer to join our team. The successful candidate will be responsible for designing and developing innovative solutions for our clients. Strong coding skills and experience with Python and/or JavaScript are a must. This is a great opportunity for someone looking to grow their career in the tech industry.",
    "We're looking for a talented marketing manager to lead our marketing efforts. The ideal candidate will have experience creating and executing successful marketing campaigns, as well as a passion for storytelling and brand building. Strong analytical and project management skills are a must. This is a chance to make a real impact at a rapidly growing company.",
    "We're hiring a customer service representative to join our team. The successful candidate will have excellent communication skills and the ability to provide top-notch customer service to our clients. Experience in a customer service role is preferred, but not required. This is a great opportunity for someone looking to start a career in customer service.",
    "We're seeking a graphic designer to join our creative team. The ideal candidate will have a strong portfolio showcasing their skills in design, typography, and branding. Knowledge of Adobe Creative Suite is a must. This is a great opportunity for a designer to work on exciting projects and help bring our clients' visions to life.",
    "We're looking for a financial analyst to join our finance team. The successful candidate will have experience working with financial data and creating financial models. Strong analytical skills and a passion for problem solving are a must. This is a great opportunity for someone looking to grow their career in finance.",
]


class Command(BaseCommand):
    help = "Populate the Job model with sample data"

    def handle(self, *args, **options):
        N = 25
        employer = EmployerProfile.objects.all()
        today_date = datetime.datetime.now().date()

        for i in range(N):
            company = random.choice(employer)

            """Basic Information"""
            title = random.choice(job_titles)
            location = company.company_location
            no_of_vacancy = random.randint(1, 10)
            salary_range = f"Rs. {random.randint(1, 40) * 10000}"

            deadline = today_date + datetime.timedelta(days=random.randint(14, 150))
            # Replace 150 with 30 * 5 or 30 * 4 to set the maximum range to 4 or 5 months, respectively.

            """Choice Fields"""
            job_level = random.choice(JOB_LEVEL_CHOICES)[0]
            employment_type = random.choice(EMPLOYMENT_TYPE_CHOICES)[0]
            job_nature = random.choice(JOB_NATURE_CHOICES)[0]

            """Specification"""
            education_level = random.choice(education_levels)
            experience_required = random.randint(0, 4)
            random_skills = random.sample(skills, 3)
            skill_required = ", ".join(random_skills)

            """Additional Description"""
            description = random.choice(job_descriptions)

            """Company"""
            posted_by = company.user

            Job.objects.create(
                title=title,
                location=location,
                no_of_vacancy=no_of_vacancy,
                salary_range=salary_range,
                deadline=deadline,
                job_level=job_level,
                employment_type=employment_type,
                job_nature=job_nature,
                education_level=education_level,
                experience_required=experience_required,
                skill_required=skill_required,
                description=description,
                posted_by=posted_by,
            )

            self.stdout.write(
                f"Job '{title}' for company '{company.company_name}' created."
            )
