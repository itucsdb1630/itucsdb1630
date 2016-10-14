from wtforms import Form, validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class UserForm(Form):
    """CSRF Protected User Form."""
    username = StringField('Username', [
        validators.Length(min=4, max=49),
        validators.DataRequired("Please, enter your username.")
    ])
    email = EmailField('Email', [
        validators.Email("Please, enter correct email address."),
        validators.DataRequired("Please, enter your email address.")
    ])
    password = PasswordField('Password', [
        validators.DataRequired("Please, enter your password"),
        validators.EqualTo('confirm', message='Passwords must match!')
    ])
    confirm = PasswordField('Repeat Password')
    name = StringField('FullName')
