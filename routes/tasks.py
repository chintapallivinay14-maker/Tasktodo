from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.task import Task

tasks_bp = Blueprint("tasks", __name__)

VALID_PRIORITIES = {"Low", "Medium", "High"}
VALID_CATEGORIES = {"College", "Personal", "Work", "Other"}
VALID_STATUSES = {"Pending", "In Progress", "Completed"}

def parse_due_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid due date.")

def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "category": task.category,
        "status": task.status,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "overdue": task.is_overdue,
    }

def get_owned_task(task_id):
    return Task.query.filter_by(id=task_id, user_id=current_user.id).first()

@tasks_bp.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        data = request.form if request.form else (request.get_json(silent=True) or {})
        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        priority = data.get("priority", "Medium")
        category = data.get("category", "Other")
        status = data.get("status", "Pending")

        if not title:
            flash("Task title cannot be empty.", "error")
            return redirect(url_for("tasks.tasks"))
        if len(title) > 150:
            flash("Task title must be 150 characters or fewer.", "error")
            return redirect(url_for("tasks.tasks"))
        if priority not in VALID_PRIORITIES or category not in VALID_CATEGORIES or status not in VALID_STATUSES:
            flash("Invalid task option.", "error")
            return redirect(url_for("tasks.tasks"))

        try:
            due_date = parse_due_date(data.get("due_date", ""))
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("tasks.tasks"))

        task = Task(
            user_id=current_user.id,
            title=title,
            description=description,
            priority=priority,
            category=category,
            status=status,
            due_date=due_date,
        )
        db.session.add(task)
        db.session.commit()

        if request.is_json:
            return jsonify(task_to_dict(task)), 201

        flash("Task added successfully.", "success")
        return redirect(url_for("tasks.tasks"))

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    category = request.args.get("category", "")
    due_filter = request.args.get("due", "")
    sort = request.args.get("sort", "newest")

    query = Task.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    if status in VALID_STATUSES:
        query = query.filter_by(status=status)
    if priority in VALID_PRIORITIES:
        query = query.filter_by(priority=priority)
    if category in VALID_CATEGORIES:
        query = query.filter_by(category=category)

    tasks_list = query.all()

    if due_filter == "overdue":
        tasks_list = [t for t in tasks_list if t.is_overdue]
    elif due_filter == "today":
        tasks_list = [t for t in tasks_list if t.due_date == date.today()]
    elif due_filter == "upcoming":
        tasks_list = [t for t in tasks_list if t.due_date and t.due_date >= date.today()]

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    if sort == "oldest":
        tasks_list.sort(key=lambda t: t.created_at)
    elif sort == "priority":
        tasks_list.sort(key=lambda t: priority_order.get(t.priority, 9))
    elif sort == "due":
        tasks_list.sort(key=lambda t: t.due_date or date.max)
    else:
        tasks_list.sort(key=lambda t: t.created_at, reverse=True)

    return render_template(
        "tasks.html",
        tasks=tasks_list,
        filters={
            "search": search,
            "status": status,
            "priority": priority,
            "category": category,
            "due": due_filter,
            "sort": sort,
        },
    )

@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
@login_required
def task_detail(task_id):
    task = get_owned_task(task_id)
    if not task:
        if request.is_json:
            return jsonify({"error": "Task not found or unauthorized."}), 404
        flash("Task not found.", "error")
        return redirect(url_for("tasks.tasks"))

    if request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully."})

    data = request.get_json(silent=True) or {}
    title = str(data.get("title", task.title)).strip()
    if not title:
        return jsonify({"error": "Task title cannot be empty."}), 400

    priority = data.get("priority", task.priority)
    category = data.get("category", task.category)
    status = data.get("status", task.status)

    if priority not in VALID_PRIORITIES or category not in VALID_CATEGORIES or status not in VALID_STATUSES:
        return jsonify({"error": "Invalid task option."}), 400

    try:
        due_date = parse_due_date(data.get("due_date", task.due_date.isoformat() if task.due_date else ""))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    task.title = title
    task.description = str(data.get("description", task.description)).strip()
    task.priority = priority
    task.category = category
    task.status = status
    task.due_date = due_date
    db.session.commit()

    return jsonify(task_to_dict(task))

@tasks_bp.route("/tasks/<int:task_id>/status", methods=["PATCH"])
@login_required
def update_status(task_id):
    task = get_owned_task(task_id)
    if not task:
        return jsonify({"error": "Task not found or unauthorized."}), 404

    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status."}), 400

    task.status = status
    db.session.commit()
    return jsonify(task_to_dict(task))

@tasks_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = get_owned_task(task_id)
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("tasks.tasks"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Task title cannot be empty.", "error")
            return redirect(url_for("tasks.edit_task", task_id=task.id))

        try:
            due_date = parse_due_date(request.form.get("due_date", ""))
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("tasks.edit_task", task_id=task.id))

        priority = request.form.get("priority", "Medium")
        category = request.form.get("category", "Other")
        status = request.form.get("status", "Pending")

        if priority not in VALID_PRIORITIES or category not in VALID_CATEGORIES or status not in VALID_STATUSES:
            flash("Invalid task option.", "error")
            return redirect(url_for("tasks.edit_task", task_id=task.id))

        task.title = title
        task.description = request.form.get("description", "").strip()
        task.priority = priority
        task.category = category
        task.status = status
        task.due_date = due_date
        db.session.commit()

        flash("Task updated successfully.", "success")
        return redirect(url_for("tasks.tasks"))

    return render_template("edit_task.html", task=task)
