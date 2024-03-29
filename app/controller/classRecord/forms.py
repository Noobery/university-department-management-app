from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, DecimalField

class classRecordForm(FlaskForm):
    studentID = StringField('studentID', validators=[validators.DataRequired(), validators.Regexp(regex=r'^\d{4}-\d{4}$', message="ID Should be in (XXXX-XXXX) Format")])

    firstname = StringField('firstname', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="First Name should only contain letters, spaces, or hyphens")
    ])

    lastname = StringField('lastname', validators=[
        validators.InputRequired(),
        validators.Regexp(regex=r'^[A-Za-z\s\-]+$', message="Last Name should only contain letters, spaces, or hyphens")
    ])

    coursecode = StringField("coursecode", [validators.DataRequired()])

    email = StringField('email', validators=[validators.Email(), validators.Regexp(regex=r'.*@g\.msuiit\.edu\.ph$', message="Only Accepts MSU-IIT Email")])

    submit = SubmitField("Submit")

class gradeDistributionForm(FlaskForm):
    name = StringField("name", [validators.DataRequired()])
    percentage = DecimalField("Percentage", [
        validators.DataRequired(),
        validators.NumberRange(min=0, max=100, message="Please enter a valid percentage (0-100).")
    ])
    submit = SubmitField("Submit")

class activityForm(FlaskForm):
    Assessment = StringField("Assessment", [validators.DataRequired()])
    activityname = StringField("activityname", [validators.DataRequired()])
    scorelimit = DecimalField("scorelimit", [
        validators.DataRequired(),
        validators.NumberRange(min=0)
    ])
    submit = SubmitField("Submit")
