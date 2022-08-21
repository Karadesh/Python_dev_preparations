from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username:',
        validators=[
            DataRequired(),
        Length(min=2, max=20)
        ]
    )
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
        Email()
        ]
    )
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        'Confirm password:',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That name is already exists. Please choose another'
            )
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Someone with that E-mail is already registered. Please choose another'
            )

class LoginForm(FlaskForm):
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
        Email()
        ]
    )
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired()
        ]
    )
    remember = BooleanField('remember me my password')
    submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username:',
        validators=[
            DataRequired(),
        Length(min=2, max=20)
        ]
    )
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
        Email()
        ]
    )
    picture = FileField(
        'Change profile photo',
        validators=[
            FileAllowed(['jpg', 'png'])
        ]
    )
    submit = SubmitField('Save changes')

    def validate_username(self,  username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Someone with that user name is already registered. Please choose other User name'
                    )
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'Someone with that e-mail is already registered. Please choose another one'
                    )
    
class RequestResetForm(FlaskForm):
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
        Email()
        ]
    )
    submit = SubmitField('Change password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that e-mail. You can register new account'
                )
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        'Confirm password:',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Change password')