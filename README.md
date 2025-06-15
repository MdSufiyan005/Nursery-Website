# 🌱 Nursery Website - Backend (IN DEVELOPMENT)

This repository contains the backend of the **Nursery Website**, developed using Django. The project is currently in active development. It handles all server-side logic including routing, database management, and administrative operations.

---

## 🚀 Getting Started

Follow the steps below to set up the project locally on your system.
also for the AUTH part you need to use .exp.env -> .env file and add the environment variables to it
follow this YT Video for getting google credentials ``` https://www.youtube.com/watch?v=LyDdfO6o_G4  ```

### 1. Clone the Repository

Fork or clone the repository from GitHub:

```bash
git clone https://github.com/MdSufiyan005/Nursery-Website.git
````

Navigate into the project directory:

```bash
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

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the Server

Navigate to the backend directory:

```bash
cd backend
```

Run Django commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit the server in your browser:

```
http://127.0.0.1:8000/
```

---

## 🗂️ Accessing the Admin Panel

To manage database content via Django Admin:

1. Create a superuser:

```bash
python manage.py createsuperuser
```

> ⚠️ Remember the username and password you set.

2. Access the admin interface:

```
http://127.0.0.1:8000/admin
```

---

## 📌 Notes

* Activate your virtual environment before running commands.
* Run migrations after modifying models.

---

## 🤝 Contributing

fork the project, work on features or bugs, and create a pull request.

