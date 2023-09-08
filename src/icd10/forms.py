"""
icd10 > forms.py
"""

# Imports
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    FileField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
)


# Form - ICD-10 Upload
class ICD10UploadForm(FlaskForm):
    """ICD-10 upload form"""

    library_year = StringField(
        "Library Year",
        validators=[
            DataRequired(),
        ],
    )
    library_type = SelectField(
        "Library Type",
        choices=[
            ("CM", "ICD-10-CM"),
            ("PCS", "ICD-10-PCS"),
        ],
        validators=[
            DataRequired(),
        ],
    )
    file = FileField(
        "Upload File",
        validators=[
            DataRequired(),
        ],
    )
    submit = SubmitField("Upload")
