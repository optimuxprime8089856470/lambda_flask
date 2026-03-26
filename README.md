# lambda_flask
# 🚀 Flask Auth System

A **secure Flask web application** built to handle real-world authentication flows — not just login forms, but **verified users, protected routes, and attack resistance**.

This project focuses on doing the basics **correctly**, not just making them work.

---

## ⚡ Features

* 🔐 User Registration & Login
* 📧 Email Verification System
* 🔑 Secure Password Hashing
* 🚫 Rate Limiting (anti brute-force)
* 👤 Session Management (Flask-Login)
* 🛡️ Protected Dashboard
* 🧼 Input Validation

---

## 🧱 Tech Stack

**Backend**

* Python
* Flask
* Flask-Login
* Flask-SQLAlchemy
* Flask-Mail
* Flask-Limiter
* itsdangerous

**Database**

* SQLite

**Frontend**

* HTML / CSS / JavaScript

---

## ⚙️ Setup

### 1. Clone the repository

```bash id="cln01"
git clone https://github.com/optimuxprime8089856470/flask-auth-system.git
cd flask-auth-system
```

### 2. Create virtual environment

```bash id="venv01"
python -m venv venv
```

Activate it:

**Windows**

```bash id="win01"
venv\Scripts\activate
```

**Linux / macOS**

```bash id="mac01"
source venv/bin/activate
```

---

### 3. Install dependencies

```bash id="dep01"
pip install -r requirements.txt
or install the packages manually
```

---

### 4. Configure environment variables

Create a `.env` file  in the lambda configration env variables :

```env id="env01"
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

if the gmail doesnt work 
use trapmail (only for testing)
repalce the gmail credentials with trapmail credentials
```

> ⚠️ Never upload `.env` to GitHub

---

### 5. Run the application

```bash id="run01"
python app.py
```

Open:

```id="url01"
http://127.0.0.1:5000/
```

---

## 🧪 Workflow

1. Register account
2. Receive verification email
3. Activate account
4. Login
5. Access dashboard

---

## 🔐 Security

* Password hashing (Werkzeug)
* Token-based email verification
* Rate limiting on login
* Session protection
* Environment variable handling

---

## 📸 Preview



---

## 🚧 Future Improvements

* Password reset system
* OAuth (Google login)
* Deployment (Render / VPS)
* Better UI/UX

---

## 👨‍💻 Author

**Muhammed Darwish**
🔗 https://github.com/optimuxprime8089856470

---

## ⭐ Note

This project proves you understand **how authentication actually works**.

If you extend this → you’re improving.
If you stop here → you’re still basic.

HOME PAGE
<img width="1906" height="920" alt="Screenshot 2026-03-20 163051" src="https://github.com/user-attachments/assets/977780c1-5be8-4fdb-a2a9-739f99eaa18c" />

LOGIN PAGE


<img width="1915" height="950" alt="Screenshot 2026-03-20 163144" src="https://github.com/user-attachments/assets/90ba82cb-02f1-45f3-894e-a8c7340a9832" />


DASHBOARD PAGE

<img width="1916" height="997" alt="image" src="https://github.com/user-attachments/assets/d1995840-4f96-4ca2-b02e-4665d584659b" />

Register pagge

<img width="1909" height="925" alt="image" src="https://github.com/user-attachments/assets/0126486b-b437-4b0e-9105-f9734f969067" />

