from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.database import db


# ==========================================================
# USER MODEL
# ==========================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    analyses = db.relationship(
        "AnalysisHistory",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ===================================
    # PASSWORD FUNCTIONS
    # ===================================

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(
            self.password,
            password
        )

    def __repr__(self):
        return f"<User {self.email}>"


# ==========================================================
# ANALYSIS HISTORY
# ==========================================================

class AnalysisHistory(db.Model):
    __tablename__ = "analysis_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    mother_file = db.Column(
        db.String(255)
    )

    father_file = db.Column(
        db.String(255)
    )

    health_score = db.Column(
        db.Float
    )

    risk_level = db.Column(
        db.String(50)
    )

    predicted_disease = db.Column(
        db.String(255)
    )

    recommendations = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ===================================
    # HELPER
    # ===================================

    def to_dict(self):

        return {

            "id": self.id,

            "mother_file": self.mother_file,

            "father_file": self.father_file,

            "health_score": self.health_score,

            "risk_level": self.risk_level,

            "predicted_disease": self.predicted_disease,

            "recommendations": self.recommendations,

            "created_at": self.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )

        }

    def __repr__(self):
        return f"<Analysis {self.id}>"