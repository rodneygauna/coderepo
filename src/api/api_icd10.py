"""
api > api_icd10.py
This file contains the API for the ICD10 endpoint.
"""

# Imports
from datetime import datetime
from flask import Blueprint, jsonify, request
from src.models import ICD10


# Blueprint
api_icd10_bp = Blueprint("api_icd10", __name__)


# API - Search ICD-10
@api_icd10_bp.route("/api/icd10/search", methods=["GET"])
def search_icd10(date_of_service=None, code=None, description=None):
    """Search ICD-10 endpoint
    The user has the ability to search the endpoint using the following
    parameters:
    - date_of_service
    - code
    - description

    Based on the date_of_service, the user will be able to search for the
    ICD-10 for the appropriate year. For example, if the date_of_service
    is 2020-01-01, the ICD-10s for the library_year 2020 will be searched.

    The user can search for the ICD-10 using the code or description. The user
    can enter a partial code or description and the API will return all ICD-10s
    that match the partial code or description.

    The user will need to submit the date_of_service. The user can submit the
    code or description or both.

    The API will return the following information:
    - library_year
    - library_type
    - diagnosis_code
    - diagnosis_description

    URL Structure:
    /api/icd10/search?date_of_service=YYYY-MM-DD&code=CODE&description=DESCRIPTION
    Example:
    /api/icd10/search?date_of_service=2022-10-15&code=M5&description=pain
    """

    # Get the date_of_service
    date_of_service = request.args.get("date_of_service")
    # Get the code
    code = request.args.get("code")
    # Get the description
    description = request.args.get("description")

    # Check if the date_of_service is valid
    if date_of_service is None:
        return jsonify({"message": "Please enter a valid date_of_service."}),
    400

    # Convert the date_of_service string to a datetime object
    date_of_service = datetime.strptime(date_of_service, "%Y-%m-%d")

    # Calculate the ICD-10 library year based on the date_of_service
    if date_of_service.month >= 10 and date_of_service.month <= 12:
        # If the month is between October and December, it belongs to the
        # next year ICD-10 library
        library_year = date_of_service.year + 1
    else:
        # If the month is January and September, it belongs to the
        # current year ICD-10 library
        library_year = date_of_service.year

    # Query the ICD-10 table
    query = ICD10.query.filter(ICD10.library_year == library_year)

    if code:
        query = query.filter(ICD10.diagnosis_code.contains(code))
    if description:
        query = query.filter(
            ICD10.diagnosis_description.contains(description))

    # Get the results
    results = query.all()

    # Check if there are any results
    if not results:
        return jsonify({"message": "No results found."}), 200

    # Create the response
    response = []
    for result in results:
        response.append({
            "library_year": result.library_year,
            "library_type": result.library_type,
            "diagnosis_code": result.diagnosis_code,
            "diagnosis_description": result.diagnosis_description
        })

    return jsonify(response), 200
