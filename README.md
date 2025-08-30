# Job Board Application

A modern job board platform built with Django that combines social features with job posting capabilities. This project merges the functionality of a job portal with social interaction features.

---

## 🚀 Quick Start

### Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py collectstatic

python manage.py runserver


Quiz4/
├── accounts/           # User authentication & profiles
│   ├── models.py       # CustomUser and Profile models
│   └── views.py        # Authentication views
├── posts/              # Posts & social features
│   ├── models.py       # Post models
│   └── views.py        # Post related views
├── jobs/               # Job-related functionality
│   ├── models.py       # Job and Application models
│   └── views.py        # Job management views
├── static_my_project/  # Static assets
│   ├── css/            # Bootstrap and custom styles
│   └── js/             # JavaScript files
└── templates/          # HTML templates
    ├── auth/           # Authentication templates
    ├── jobs/           # Job-related templates
    └── posts/          # Post-related templates
# quiz4PURI
