# Social Media Platform

Mini social media application built with HTML, CSS, JavaScript and Django.

Built as a task for the **CodeAlpha** internship.

## Tech Stack
- Backend: Python, Django 5
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (Django templates)
- Image uploads: Pillow

## Features
- User registration, login and logout
- User profiles and bio
- Create, edit and delete posts
- Optional post images
- Comments
- Like / unlike posts
- Follow / unfollow users
- Followers and following counts
- User profile pages
- Django admin
- SQLite database

## Setup

### 1. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install packages
```bash
pip install -r requirements.txt
```

### 3. Create database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create admin account
```bash
python manage.py createsuperuser
```

### 5. Run
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Project Structure
```
manage.py
requirements.txt
social_media/   # project settings and root URLs
social/         # app: models, views, forms, urls, admin
templates/social/
static/social/  # style.css, script.js
```

## Screenshots
Add screenshots of the home feed and a profile page here.

## Notes
Uploaded media is stored in the `media/` folder. The SQLite database is `db.sqlite3` after migration.
