from wtforms.fields.core import *
from wtforms.fields.simple import *
from wtforms.fields.simple import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp, Optional,NumberRange
from wtforms import ValidationError
from server_pkg.models import User


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    # Placeholder labels to enable form rendering
    username = StringField(
        validators=[Optional()]
    )


class register_form(FlaskForm):
    
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_. ]*$",
                0,
                "Usernames must have only letters, " "numbers, dots, underscores or spaces",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        if User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")


class Tour_form(FlaskForm):
    name =              StringField("Name for the Tour",validators=[InputRequired(), Length(1, 64)])
    longitude =          FloatField("longitude",validators=[InputRequired()])
    latitude =           FloatField("latitude",validators=[InputRequired()])
    photos =      MultipleFileField("photos", validators=[FileAllowed(['xls', 'xlsx'], 'Excel Document only!')])
    site =              StringField("Link for the Site",validators=[Length(0, 64)])
    landmarks =         StringField("Names of Landmarks",validators=[Length(0, 64)])
    opening_timing =    StringField("Opening timings",validators=[Length(0, 64)])
    description =       StringField("description of the Tour",validators=[InputRequired(), Length(1, 64)])
    submit=             SubmitField("Submit")
    
    # Placeholder labels to enable form rendering

class Location_form(FlaskForm):
    name =              StringField("Name for the Location",validators=[InputRequired(), Length(1, 64)])
    type =              SelectField("Type ofLocation",validators=[InputRequired()], choices=[(1,""),(2,""),(3,""),(4,"")])
    site =              StringField("Link for the Site",validators=[Length(0, 64)])
    longitude =          FloatField("longitude",validators=[InputRequired()])
    latitude =           FloatField("latitude",validators=[InputRequired()])
    opening_timing =    StringField("Opening timings",validators=[Length(0, 64)])
    photos =      MultipleFileField("photos", validators=[FileAllowed(['xls', 'xlsx'], 'Excel Document only!')])
    description =       StringField("description of the Tour",validators=[InputRequired(), Length(1, 64)])
    other_type =        StringField("Describe the type of location",validators=[Length(0, 64)])
    submit=             SubmitField("Submit")
    
