"""
icd10 > views.py
"""

# Imports
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
                # Create a new ICD-10 record
                icd10 = ICD10(
                    library_year=form.library_year.data,
                    library_type=form.library_type.data,
                    diagnosis_code=diagnosis_code,
                    diagnosis_description=diagnosis_description,
                )
                db.session.add(icd10)
            # Commit the changes to the database
            db.session.commit()
            flash("ICD-10 upload successful!", "success")
            return redirect(url_for("icd10.icd10_landing"))
        else:
            flash("Invalid file type!", "danger")

    return render_template("icd10/icd10_upload_parse.html", form=form)
