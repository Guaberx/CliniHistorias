from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2, max=20)], render_kw={"placeholder":"CoolUsername123"})
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"someone@domain.com"})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={"placeholder":"******"})
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo(password)], render_kw={"placeholder":"******"})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()], render_kw={"placeholder":"someone@domain.com"})
    password = PasswordField('Password',validators=[DataRequired()], render_kw={"placeholder":"******"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Secret key in order to protect against modified cookies and crosside attacks
