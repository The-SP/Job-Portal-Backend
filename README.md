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