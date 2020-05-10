from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField

class Register_Form(FlaskForm):
    """ Form for adding new user """
    username = StringField("Username", validators=[InputRequired(message='Username is required!')])
    password = PasswordField('Password',  validators=[InputRequired(message='Password is required!')])
    email = EmailField("Email", validators=[InputRequired(message='Email is required!')])
    first_name = StringField("First Name", validators=[InputRequired(message='First name is required!')])
    last_name = StringField("Last Name", validators=[InputRequired(message='Last name is required!')])

class Login_Form(FlaskForm):
    """ Form for logging in a user """
    username = StringField("Username", validators=[InputRequired(message='Username is required!')])
    password = PasswordField('Password',  validators=[InputRequired(message='Password is required!')])

class Feedback_Form(FlaskForm):
    """ Form for adding feedback to user """
    title = StringField("Title", validators=[InputRequired(message='Title is required!')])
    content = StringField('Content',  validators=[InputRequired(message='Content is required!')])