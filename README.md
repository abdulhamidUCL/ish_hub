# ISH Hub

A Django-based job portal that connects job seekers with employers. The platform allows users to browse available jobs, view detailed job information, and apply through a clean and user-friendly interface.

## Features

- 🔐 User authentication
- 💼 Browse available job listings
- 📄 View detailed job descriptions
- 🔍 Search and filter jobs
- 👤 Employer job management
- 🛠 Django Admin panel
- 📱 Responsive user interface

## Tech Stack

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite (Development)

## Project Structure

```
ish_hub/
├── manage.py
├── jobs/
├── users/
├── templates/
├── static/
├── media/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/abdulhamidUCL/ish_hub.git
```

### 2. Navigate to the project

```bash
cd ish_hub
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

## Future Improvements

- Email notifications
- Resume uploads
- Company profiles
- Advanced job filtering
- Saved jobs
- REST API
- Deployment

## Author

**Abdulhamid**

GitHub: https://github.com/abdulhamidUCL

---

⭐ If you found this project useful, consider giving it a star on GitHub!