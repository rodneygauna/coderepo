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
class ICD10(db.Model):
    """ICD-10 model"""

    __tablename__ = "icd10"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # ICD-10 Information
    library_year = db.Column(db.String(4), nullable=False)
    library_type = db.Column(db.String(3), nullable=False)
    diagnosis_code = db.Column(db.String(10), nullable=False)
    diagnosis_description = db.Column(db.String(255), nullable=False)


# Model - SNOMED CT Library
class SNOMEDCT(db.Model):
    """SNOMED CT model"""

    __tablename__ = "snomedct"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # SNOMED CT Information
    library_year = db.Column(db.DateTime, nullable=False)
    snomed_code = db.Column(db.String(10), nullable=False)
    snomed_description = db.Column(db.String(255), nullable=False)


# Model - ICD-10 to SNOMED CT Mapping
class ICD10_SNOMEDCT(db.Model):
    """ICD-10 to SNOMED CT Mapping model"""

    __tablename__ = "icd10_snomedct"

    # IDs
    id = db.Column(db.Integer, primary_key=True)
    # Timestamps
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    # ICD-10 to SNOMED CT Mapping Information
    icd10_id = db.Column(db.Integer, db.ForeignKey("icd10.id"))
    snomedct_id = db.Column(db.Integer, db.ForeignKey("snomedct.id"))
