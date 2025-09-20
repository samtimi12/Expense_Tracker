from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User  # Assuming models.py defines your User model and db

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

serializer = URLSafeTimedSerializer("SECRET_KEY")  # Replace with app.config["SECRET_KEY"]

# Create Blueprint
auth = Blueprint("auth", __name__)

# -----------------------------
# LOGIN ROUTE
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("index"))  # make sure 'index' route exists
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


# -----------------------------
# SIGNUP ROUTE
# -----------------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password").strip()

        # Email check
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in or use another email.", "danger")
            return redirect(url_for("auth.signup"))

        # Username check
        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose another one.", "danger")
            return redirect(url_for("auth.signup"))

        # Hash password (safe default with pbkdf2:sha256)
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)

        # Create and commit new user
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Error creating account. Please try again.", "danger")
            return redirect(url_for("auth.signup"))

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# -----------------------------
# LOGOUT ROUTE
# -----------------------------
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

# -----------------------------
# FORGOT PASSWORD ROUTE
# -----------------------------
@auth.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for("auth.forgot_password"))

        token = serializer.dumps(user.email, salt="password-reset-salt")
        reset_url = url_for("auth.reset_password", token=token, _external=True)
        print(f"[RESET LINK] {reset_url}")  # Replace with actual email sending
        flash("Password reset link has been sent (check console for now).", "success")
        return redirect(url_for("auth.login"))

    return render_template("forgot.html")

# ------------------------------
# RESET PASSWORD ROUTE
# ------------------------------
@auth.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=3600)  # 1 hour
    except Exception:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        new_password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()
        flash("Password reset successfully. You can log in now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset.html")

