from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, MultipleFileField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=20)])
    remember = BooleanField('Remember me')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=15)])


class CreationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email format'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=15)])
    active = BooleanField('Activate user')
    admin = BooleanField('Admin user')


class DeleteForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])


class ModelForm(FlaskForm):
    files = MultipleFileField('Upload your images', validators=[InputRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    sentence = TextAreaField('Copy your texts / 1 description = 1 line', validators=[InputRequired(), Length(min=5, max=5000)])
