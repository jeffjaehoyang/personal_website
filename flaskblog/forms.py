from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2,max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=8)])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Join')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Oops! This username seems to be taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Oops! This email is already registered. Please register with a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')

    login = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Your Name',
                       validators=[DataRequired()])

    email = StringField('Your Email',
                        validators=[DataRequired(), Email()])

    subject = StringField('Subject',
                          validators=[DataRequired()])

    message = TextAreaField('Message',
                            validators=[DataRequired()])

    security_question = StringField('Bots Aren\'t Welcome',
                                     validators=[DataRequired()])

    send = SubmitField('Send')

    def validate_security_question(self, security_question):
        answer = int(security_question.data)
        if answer != 8:
            raise ValidationError('Oops! Can you do simple arithmetics?')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2,max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    image = FileField('Upload Profile Picture',
                      validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data: 
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Oops! This username seems to be taken. Please choose another one.')

    def validate_email(self, email):
        if current_user.email != email.data:    
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Oops! This email is already registered. Please register with a different email.')
