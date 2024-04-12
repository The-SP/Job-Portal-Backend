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

### Running migrations

```bash
py manage.py makemigrations
py manage.py migrate
```

### Running the server and frontend

```bash
py manage.py runserver
npm start
```

```bash
cd frontend
npm install
```
