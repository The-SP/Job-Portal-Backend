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

## Setup .env inside job/job/

```bash
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DOMAIN=localhost:3000
SITE_NAME=Frontend
```

## Running migrations

### Running migrations for the first time

1. First comment out these lines
   - inside job/job/settings.py
   ```py
       INSTALLED_APPS = [
           # ...
           "recommender", # Comment out this
           # ...
       ]
   ```
   - in job/job/urls.py
   ```py
       urlpatterns = [
       # ...
       path("api/jobs/", include("recommender.urls")), # Comment this
       # ...
   ```
2. Run migrations
```bash
py manage.py makemigrations
py manage.py migrate
```
3. Un-Comment above lines. Now you can run migrations again normally if needed.

### Running the server and frontend

```bash
py manage.py runserver
npm start
```
```bash
cd frontend
npm install
```

---

## Additional Features

For information on how to use the additional features of this API, see the [Extended Usage Guide](./extended-usage.md).

