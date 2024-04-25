# Project Setup

### Backend

Create a virtual environment and install the required Python packages:

```bash
# Create a virtual environment to isolate our package dependencies locally
python -m venv env
env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Setup .env inside job/job/  
To enable sending email notifications to users (e.g., for account creation, password reset), you need to configure email settings. Create a .env file inside backend/job/job/ with the following content:

```bash
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=yourpassword
DOMAIN=localhost:3000
SITE_NAME=Job Portal
```

### Running migrations

```bash
py manage.py makemigrations
py manage.py migrate
```

### Running the server

```bash
py manage.py runserver
```
