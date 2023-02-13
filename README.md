# Hire Nepal
A Job Portal website for finding your dream job in Nepal.

## Features
- Job Listings: Browse through the latest job postings from top companies in Nepal.
- Job Recommendations: Get personalized job recommendations based on your profile and preferences.
- Easy Apply: Apply for a job with just a few clicks.
- Employer Dashboard: Manage your job postings and applicants from a single platform.

## Project Setup

### Backend

```bash
# Create a virtual environment to isolate our package dependencies locally
python -m venv env
env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run project

```bash
py manage.py runserver
npm start
```

## Setup .env inside job/
```bash
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DOMAIN=localhost:3000
SITE_NAME=Frontend
```

## Recommendation System Setup
- Download the original dataset from 'https://www.kaggle.com/datasets/PromptCloudHQ/us-technology-jobs-on-dicecom'. (Save it inside 'Recommendation System' folder)

- Then run `filter_csv.ipynb`
    - This creates `jobs_data.csv` file which is used by the backed.

- Also, You can experiment with the recommender by running 'job_recommender.ipynb'

## Populating Database

### Django Management Commands
Django Management Commands are custom scripts that can be used to automate tasks related to your Django application. These commands can be run through the `python manage.py <command>` in the terminal.  

The available commands are:
1. ### create_users 
    This command creates 10 instances of UserAccount model with email addresses in the format "user0@gmail.com" to "user9@gmail.com" and sets their password to "testing321". It also creates 10 instances of SeekerProfile model linked to the respective UserAccount instances.

2. ### create_employer
    Creates 10 instances of UserAccount model with email addresses in the format "company0@gmail.com" to "company9@gmail.com" and sets their password to "testing321".
    Also creates corresponding EmployerProfile model.

3. ### create_jobs
    Creates instances of Job model with random meaningful values.

4. ### create_applications
    Creates instances of JobApplication model for a particular job. (Change JOB_ID to choose job)

### Run above commands
```bash
python manage.py create_users
python manage.py create_employer
python manage.py create_jobs
python manage.py create_applications
```