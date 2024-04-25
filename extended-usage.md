# Usage

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

4. ### create_jobs_from_csv

   Populate the Job model with 20K datasets from csv (https://www.kaggle.com/datasets/PromptCloudHQ/us-technology-jobs-on-dicecom)

5. ### update_jobs_deadline

   Update the deadline field for existing Job objects using bulk update

6. ### create_applications

   Creates instances of JobApplication model for a particular job. (Change JOB_ID to choose job and specify the resume_path)

7. ### update_recommendations
  -  Update recommendations and save vectorizer, matrices and df_jobs in a pickle file
  - This creates `recommendation_data.pkl` inside `job/recommender`

### Run above commands

```bash
python manage.py create_users
python manage.py create_employer
python manage.py create_jobs
python manage.py create_applications
python manage.py create_jobs_from_csv
python manage.py update_jobs_deadline
python manage.py update_recommendations
```

## Migrating to PostgreSQL

```bash
# Dump / Backup existing database
py manage.py dumpdata > datadump.json

# Install PostgreSQL and pgAdmin
pip install psycopg2

py manage.py migrate

py manage.py loaddata datadump.json
```

## Running scrapper/scrapper.py

```bash
# Run below command from backend/job
py scrapper/scrapper.py
```

- It scrapes IT related jobs from merojob.com website and stores in csv file.
