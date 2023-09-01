"""
Database models for the application.
"""

# Imports
from datetime import datetime
from flask import redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from src import db, login_manager


# Login Manager - User Loader
@login_manager.user_loader
def load_user(user_id):
    """Loads the user from the database"""
    return User.query.get(int(user_id))


# Login Manager - Unauthorized Handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirects unauthorized users to the login page"""
    return redirect(url_for("users.login"))


# Model - User
class User(db.Model, UserMixin):
    """User model"""

    __tablename__ = "users"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Login Information
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
    # Role
    role = db.Column(db.String(100), default="user")
    # Status
    status = db.Column(db.String(10), default="ACTIVE")
    # Profile Picture
    profile_image = db.Column(
        db.String(255), nullable=False, default="default_profile.jpg"
    )

    def check_password(self, password):
        """Checks if the password is correct"""
        return check_password_hash(self.password_hash, password)


# Model - ICD-10 Library
class ICD10CM(db.Model):
    """ICD-10-CM model"""

    __tablename__ = "icd10cm"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # ICD-10-CM Library Year
    library_year = db.Column(db.DateTime, nullable=False)
    # ICD-10-CM Code
    diagnosis_code = db.Column(db.String(10), nullable=False)
    # ICD-10-CM Description
    diagnosis_description = db.Column(db.String(255), nullable=False)
    # ICD-10-CM Inclusion Terms
    inclusion_term_1 = db.Column(db.String(255))
    inclusion_term_2 = db.Column(db.String(255))
    inclusion_term_3 = db.Column(db.String(255))
    inclusion_term_4 = db.Column(db.String(255))
    inclusion_term_5 = db.Column(db.String(255))
