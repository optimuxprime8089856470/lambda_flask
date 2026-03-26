from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

import serverless_wsgi
import os
import re


# Load env


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# ---------------- CONFIG ----------------

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/db.sqlite"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mail config
app.config["MAIL_SERVER"] = "sandbox.smtp.mailtrap.io"
app.config["MAIL_PORT"] = 2525
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

if not app.config["SECRET_KEY"]:
    raise Exception("SECRET_KEY not set")

if not app.config["MAIL_USERNAME"]:
    raise Exception("MAIL_USERNAME not set")

if not app.config["MAIL_PASSWORD"]:
    raise Exception("MAIL_PASSWORD not set")

BASE_URL=os.getenv("BASE_URL")
if not BASE_URL:
     raise Exception("BASE_URL not set")

# Cookies
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True
    

# ---------------- INIT ----------------

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# ---------------- MODEL ----------------

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# ---------------- LOGIN ----------------

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                return render_template("index.html", error="Verify your email first.")
            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("index.html", error="Invalid username or password")

    return render_template("index.html")

# PASSWORD VALIDATION
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def username_sec_check(username):
    return re.fullmatch(r"[A-Za-z0-9_]+", username)

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not is_strong_password(password):
            return render_template("register.html", error="Weak password")

        if not username_sec_check(username):
            return render_template("register.html", error="Invalid username")

        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            if not existing_user.is_verified:
                send_verification_email(email)
                return "Verification email resent."
            return render_template("register.html", error="Email already exists")

        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username taken")

        hashed_password = generate_password_hash(password)

        new_user = Users(
            username=username,
            email=email,
            password=hashed_password,
            is_verified=False
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)

        return "Check your email to verify."

    return render_template("register.html")

# SEND EMAIL FUNCTION
def send_verification_email(email):
  try:
    token = serializer.dumps(email, salt="email-verify")
    
    verify_url = f"{BASE_URL}/verify/{token}"

    msg = Message(
        subject="Verify your email",
        
        recipients=[email],
        body=f"Click the link to verify your account:\n{verify_url}"
    )

    mail.send(msg)
    print("Email sent to: , email")
  except Exception as e : 
      print("Email failed to send", str(e))


# RESEND VERIFICATION
@app.route("/resend-verification", methods=["POST"])
def resend_verification():
    email = request.form.get("email")

    user = Users.query.filter_by(email=email).first()

    if not user:
        return render_template("index.html", error="Account not found.")

    if user.is_verified:
        return render_template("index.html", error="Email already verified.")

    send_verification_email(email)

    return "Verification email resent. Check your inbox."

# VERIFY EMAIL
@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-verify", max_age=3600)
    except:
        return "Invalid or expired link"

    user = Users.query.filter_by(email=email).first()

    if user.is_verified:
        return "Already verified"

    user.is_verified = True
    db.session.commit()

    return redirect(url_for("index"))

# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- HEADERS ----------------

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response

# ---------------- LAMBDA ----------------

def handler(event, context):
    path = event.get("rawPath", "")

    # remove /default prefix
    if path.startswith("/default"):
        event["rawPath"] = path[len("/default"):] or "/"
        event["path"] = event["rawPath"]

    return serverless_wsgi.handle_request(app, event, context)


# if __name__ == "__main__":
#     app.run(debug=True)