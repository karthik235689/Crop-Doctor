from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , FileField
from wtforms.validators import Length , EqualTo , Email , DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)

class RegistrationForm_ID(FlaskForm):
    firstname = StringField(label="Enter your First Name" , validators=[Length(min=2,max=30), DataRequired()])
    lastname = StringField(label="Enter your Last Name" , validators=[Length(min=2,max=30), DataRequired()])
    mobile_number = StringField(label="Enter your Mobile Number" , validators=[Length(min=10,max=10), DataRequired()])
    email_address=StringField(label="Enter your Email Address" , validators=[Email(),DataRequired()])
    password1=PasswordField(label="Enter a Unique Password" , validators=[Length(min=6,max=30), DataRequired()])
    password2=PasswordField(label="Confirm Password" , validators=[EqualTo('password1'), DataRequired()])
    city = StringField(label="Please provide a city" , validators=[Length(min=2,max=30), DataRequired()])
    state = StringField(label="Please provide a state" , validators=[Length(min=2,max=30), DataRequired()])
    zip = StringField(label="Please provide a zip" , validators=[Length(min=2,max=30), DataRequired()])
    submit=SubmitField(label="Create Account")

class UploadForm(FlaskForm):
    photo = FileField('image',validators=[FileRequired('File was empty!')])
    submit = SubmitField('Upload')

class LoginForm_ID(FlaskForm):
    email_address=StringField(label="Enter your Email Address" , validators=[Email(),DataRequired()])
    password=PasswordField(label="Enter a Unique Password" , validators=[Length(min=6,max=30), DataRequired()])
    submit=SubmitField(label="Create Account")
