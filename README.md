# 🌱 Nursery Website - Backend (IN DEVELOPMENT)

This repository contains the **Nursery Website**, built using Django. The project is currently under active development. It handles all server-side logic including routing, database models, authentication, and administrative operations.

---

## 🚀 Getting Started

Follow the steps below to set up the project locally on your system.

> ⚠️ For the authentication system (Google OAuth), copy the variables from `.exp.env` to a new `.env` file and configure your credentials.
> Follow this YouTube tutorial to get Google credentials:
> 🎥 [`https://www.youtube.com/watch?v=LyDdfO6o_G4`](https://www.youtube.com/watch?v=LyDdfO6o_G4)

---

### 1. Clone the Repository

```bash
git clone https://github.com/MdSufiyan005/Nursery-Website.git
cd Nursery-Website
```

---

## 🛠️ Project Setup

### 2. Create a Virtual Environment

#### On Ubuntu/Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the Server

Navigate to the backend directory:

```bash
cd backend-website
```

Apply migrations and run the development server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Access the app at:

```
http://127.0.0.1:8000/
```

---

## 🐳 Running the Docker Container

1. Ensure Docker Desktop is installed and running.
2. Copy `.exp.env` → `.env` and update the environment variables.
3. Build and run the container:

```bash
cd backend-website
docker compose up -d --build
```

Open Docker Desktop to verify the container is running on port `8000`.

---

## 🗂️ Accessing the Admin Panel

1. Create a superuser:

```bash
python manage.py createsuperuser
```

> ⚠️ Remember the username and password.

2. Open your browser and go to:

```
http://127.0.0.1:8000/admin
```

---

## 📌 Notes

* Always activate the virtual environment before using Django commands.
* Apply migrations after making changes to models.
* All environment variables like `SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_API_KEY`, etc., must be in your `.env` file.

---

## 🤝 Contributing

Feel free to fork the project, work on features or bugs, and submit a pull request 🚀.
