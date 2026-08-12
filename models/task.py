from datetime import datetime, timezone
from . import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    priority = db.Column(db.String(20), default="Medium", nullable=False)
    category = db.Column(db.String(30), default="Other", nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    @property
    def is_overdue(self):
        from datetime import date
        return bool(self.due_date and self.due_date < date.today() and self.status != "Completed")
