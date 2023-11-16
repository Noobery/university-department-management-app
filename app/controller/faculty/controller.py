from os import name
from . import faculty
from flask import render_template, request, jsonify, redirect, url_for,flash
from app.controller.faculty.forms import FacultyForm, UpdateFacultyForm
from app.models.facultyModel import facultyModel
from app.controller.admin.controller import login_is_required

faculty_model = facultyModel()

@faculty.route("/faculty", methods=["GET", "POST"])
@login_is_required
def add_faculty():
    
    add_form = FacultyForm()
    update_form = UpdateFacultyForm()
    flash_message = None
    # single_faculty = None
    if request.method == "POST":
        if add_form.validate_on_submit():
            facultyID = add_form.facultyIDInput.data
            firstname = add_form.facultyfirstName.data
            lastname = add_form.facultylastName.data
            email = add_form.facultyEmail.data

            result = faculty_model.create_faculty(facultyID, firstname, lastname, email)
            # single_faculty = faculty_model.get_single_faculty(facultyID)
            if "success" in result:
                flash_message = {"type": "success", "message": "Faculty created successfully"}
                
            else:
                flash_message = {"type": "danger", "message": f"Failed to create faculty: {result}"}
        else:
            flash_message = {"type": "danger", "message": "Form validation failed. Please check your inputs."}

    faculties = faculty_model.get_faculty()
    
    return render_template("faculty.html", faculties=faculties, add_form=add_form, flash_message=flash_message, update_form=update_form)

@faculty.route("/faculty/delete/<string:facultyID>", methods=["DELETE"])
def delete_faculty(facultyID):
    try:
        result = faculty_model.delete_faculty(facultyID)
        return jsonify({'success': result == 'Faculty deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
# @faculty.route("/faculty/edit/<string:facultyID>", methods=["POST"])
# def edit_faculty(facultyID):
#     try:
#         new_firstname = request.form.get("editFacultyfirstName")
#         new_lastname = request.form.get("editFacultylastName")
#         new_email = request.form.get("editFacultyEmail")  # Corrected key
#         result = faculty_model.update_faculty(facultyID, new_firstname, new_lastname, new_email)
#         return jsonify({"success": result == "Faculty Information Updated Successfully"})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

@faculty.route("/faculty/edit/<string:facultyID>", methods=["POST"])
def edit_faculty(facultyID):
    try:
        form = UpdateFacultyForm(request.form)  # Create form instance and populate it with request data
        if form.validate_on_submit():  # Validate the form
            new_firstname = form.editFacultyfirstName.data
            new_lastname = form.editFacultylastName.data
            new_email = form.editFacultyEmail.data
            result = faculty_model.update_faculty(facultyID, new_firstname, new_lastname, new_email)
            return jsonify({"success": result == "Faculty Information Updated Successfully"})
        else:
            # Handle the case where form validation fails
            errors = {field: form.errors[field][0] for field in form.errors}
            return jsonify({"success": False, "errors": errors})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
