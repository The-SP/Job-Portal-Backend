# Project Setup

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
