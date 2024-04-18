from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, Length


    
class RegisterForm(FlaskForm):
    """Form for registering a user"""
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=4)])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=8)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    first_name = StringField("First Name",
                       validators=[DataRequired()])
    last_name = StringField("Last Name",
                          validators=[DataRequired()])
    image_url = StringField("(Optional) Profile Image URL")
    
class EditUserForm(FlaskForm):
    """Edit user form"""
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=8)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    first_name = StringField("First Name",
                       validators=[DataRequired()])
    last_name = StringField("Last Name",
                          validators=[DataRequired()])
    image_url = StringField("(Optional) Profile Image URL")

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=4)])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=8)])