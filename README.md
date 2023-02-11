# Django REST + React

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

## DJOSER API Endpoints

This project uses Djoser package to handle authentication in backend.

- auth/users/ => create user
- auth/jwt/create/ => login user
- auth/jwt/refresh/ => get new access token
- auth/users/reset_password/
- auth/users/reset_password_confirm/


## Setup .env inside job/
```bash
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DOMAIN=localhost:3000
SITE_NAME=Frontend
```

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