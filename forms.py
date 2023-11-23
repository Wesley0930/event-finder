from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for registering a user"""
    username = StringField("Username",
                           validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    email = StringField("Email",
                        validators=[Email()])
    first_name = StringField("First Name",
                       validators=[DataRequired()])
    last_name = StringField("Last Name",
                          validators=[DataRequired()])
    
class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username",
                           validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    

class Delete(FlaskForm):
    """Used to delete feedback"""