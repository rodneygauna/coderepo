"""
icd10 > views.py
"""

# Imports
from datetime import datetime
from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import (
    login_required,
    current_user,
)
from src.icd10.forms import (
    ICD10UploadForm,
)
from src import db
from src.models import (
    ICD10,
)
import xml.etree.ElementTree as ET


# Blueprint Configuration
icd10_bp = Blueprint("icd10", __name__)


# View - ICD-10 Landing Page
@icd10_bp.route("/icd10")
@login_required
def icd10_landing():
    """ICD-10 landing page"""
    return render_template("icd10/icd10_landing.html")


# View - ICD-10 Upload and Parse
@icd10_bp.route("/icd10/upload-parse", methods=["GET", "POST"])
@login_required
def icd10_upload_parse():
    """
    This page will do the following:
    1. Allow the user to upload the ICD-10 XML file
    2. Parse the XML content and store it in the database
    3. Display a banner indicating that the upload was successful
       or why the upload failed
    """

    form = ICD10UploadForm()

    # Record variables
    records_updated = 0
    records_skipped = 0
    new_records = 0

    if form.validate_on_submit():
        # Get the file from the form
        file = request.files["file"]

        # Get the file name
        filename = file.filename

        # Get the file extension
        file_extension = filename.split(".")[-1]

        # Check if the file extension is XML
        if file_extension == "xml":
            # Parse the XML file
            tree = ET.parse(file)
            root = tree.getroot()
            # Loop through the 'diag' elements
            for diag in root.findall(".//diag"):
                diagnosis_code = diag.find("name").text
                diagnosis_description = diag.find("desc").text
                # Check if the ICD-10 record already exists
                # (based on the
                # - library year,
                # - library type,
                # - diagnosis code,
                # - and diagnosis description)
                icd10_exists = ICD10.query.filter_by(
                    library_year=form.library_year.data,
                    library_type=form.library_type.data,
                    diagnosis_code=diagnosis_code,
                ).first()
                if icd10_exists:
                    # Check if the ICD-10 record's description has been updated
                    # if so, update the record
                    if icd10_exists.diagnosis_description != diagnosis_description:
                        icd10_exists.diagnosis_description = diagnosis_description
                        icd10_exists.updated_date = datetime.utcnow()
                        icd10_exists.updated_by = current_user.id
                        records_updated += 1
                    # If the ICD-10 record already exists, skip it
                    records_skipped += 1
                    continue
                else:
                    # Create a new ICD-10 record
                    icd10_new = ICD10(
                        library_year=form.library_year.data,
                        library_type=form.library_type.data,
                        diagnosis_code=diagnosis_code,
                        diagnosis_description=diagnosis_description,
                        created_date=datetime.utcnow(),
                        created_by=current_user.id,
                    )
                    db.session.add(icd10_new)
                    new_records += 1
            # Commit the changes to the database
            db.session.commit()
            flash(f"New: {new_records} | Updated: {records_updated} | Skipped: {records_skipped}",
                  "success")
            return redirect(url_for("icd10.icd10_landing"))
        else:
            flash("Invalid file type!", "danger")

    return render_template("icd10/icd10_upload_parse.html", form=form)
