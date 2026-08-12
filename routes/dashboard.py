from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.task import Task

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def home():
    from flask_login import current_user
    if current_user.is_authenticated:
        return __import__("flask").redirect(__import__("flask").url_for("dashboard.index"))
    return __import__("flask").redirect(__import__("flask").url_for("auth.login"))

@dashboard_bp.route("/dashboard")
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    total = len(tasks)
    completed = sum(t.status == "Completed" for t in tasks)
    pending = sum(t.status != "Completed" for t in tasks)
    overdue = sum(t.is_overdue for t in tasks)
    completion = round((completed / total) * 100) if total else 0

    priority_counts = {
        "High": sum(t.priority == "High" for t in tasks),
        "Medium": sum(t.priority == "Medium" for t in tasks),
        "Low": sum(t.priority == "Low" for t in tasks),
    }

    recent_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:5]

    return render_template(
        "dashboard.html",
        total=total,
        completed=completed,
        pending=pending,
        overdue=overdue,
        completion=completion,
        priority_counts=priority_counts,
        recent_tasks=recent_tasks,
        today=date.today(),
    )

@dashboard_bp.route("/profile")
@login_required
def profile():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    completed = sum(t.status == "Completed" for t in tasks)
    pending = len(tasks) - completed
    return render_template(
        "profile.html",
        total=len(tasks),
        completed=completed,
        pending=pending,
    )
