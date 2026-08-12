import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(username) < 3:
            flash("Username must contain at least 3 characters.", "error")
            return render_template("register.html")
        if not EMAIL_RE.match(email):
            flash("Please enter a valid email address.", "error")
            return render_template("register.html")
        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "error")
            return render_template("register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == identity) | (User.email == identity.lower())
        ).first()

        if not user or not user.check_password(password):
            flash("Invalid username/email or password.", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("dashboard.index"))

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
