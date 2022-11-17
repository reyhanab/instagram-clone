from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User
from sqlalchemy import or_


def user_exists(form, field):
    # Checking if user exists
    credential = field.data
    user = User.query.filter(or_(User.email == credential, User.username == credential)).first()
    if not user:
        raise ValidationError('Email provided not found.')


def password_matches(form, field):
    # Checking if password matches
    password = field.data
    credential = form.data['credential']
    user = User.query.filter(or_(User.email == credential, User.username == credential)).first()
    # if not user:

    #     raise ValidationError('No such user exists.')
    if user and not user.check_password(password):
        raise ValidationError('Password was incorrect.')


class LoginForm(FlaskForm):
    credential = StringField('Email or Username', validators=[DataRequired(), user_exists])
    password = StringField('Password', validators=[
                           DataRequired(), password_matches])