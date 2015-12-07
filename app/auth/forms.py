from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    Email,
    DataRequired,
    ValidationError,
    Length,
    EqualTo,
)
from .models import User, School


def edu_email_validator(form, field):
    print(field.data[-4:])
    if not field.data[-4:] == '.edu':
        raise ValidationError('Email must be a .edu email')


def email_in_use_validator(form, field):
    if User.select().where(User.email == form.data).exists():
        raise ValidationError('Email already in use')


class SignUpForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    edu_email_validator,
                                    email_in_use_validator])
    school = SelectField('School', choices=[(str(school.school_id), school.name) for school in School.select()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                      message='Passwords must match')])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])