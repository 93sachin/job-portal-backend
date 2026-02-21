# 🧑‍💼 Job Portal Backend (Django + DRF + JWT)

A Role-Based Job Portal Backend built using Django REST Framework with JWT Authentication.

## 🚀 Features

- 🔐 JWT Authentication (Login/Register)
- 👥 Role-Based Access Control (Student / Recruiter)
- 📝 Recruiter can create jobs
- 📩 Student can apply for jobs
- 📊 Student Dashboard (View applied jobs)
- 👀 Recruiter Dashboard (View applicants)
- 🔄 Recruiter can update application status
- 🚫 Duplicate application prevention
- ✅ Proper validation and secure endpoints

---

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- JWT Authentication
- SQLite (Development)
- Git & GitHub

---

## 📌 API Endpoints

### Authentication
- POST `/api/register/`
- POST `/api/token/`

### Jobs
- POST `/api/create-job/`
- GET `/api/jobs/`

### Applications
- POST `/api/apply-job/`
- GET `/api/my-applications/`
- GET `/api/my-applicants/`
- PATCH `/api/update-application/<id>/`

---

## ⚙ Setup Instructions

```bash
git clone <your-repo-link>
cd job-portal-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🎯 Project Purpose

This project demonstrates:

- Backend architecture design
- JWT-based authentication
- Role-based authorization
- REST API development
- Relational database handling
- Secure and validated endpoints

---

## 🌍 Live Demo
https://job-portal-backend-p580.onrender.com

## 🔑 How to Test

1. Register: POST /api/register/
2. Login: POST /api/token/
3. Use access token as Bearer Token

## 👨‍💻 Developed By

Sachin Kumar
