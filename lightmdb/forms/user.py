from wtforms import Form, validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class UserForm(Form):
    """CSRF Protected User Form."""
    username = StringField('Username', [
            validators.Length(min=4, max=49),
            validators.DataRequired("Please, enter your username.")
        ],
        render_kw={
            "placeholder": "Username",
            "class": "form-control"
        }
    )
    email = EmailField('Email', [
            validators.Email("Please, enter correct email address."),
            validators.DataRequired("Please, enter your email address.")
        ],
        render_kw={
            "placeholder": "E-mail",
            "class": "form-control"
        }
    )
    password = PasswordField('Password', [
            validators.DataRequired("Please, enter your password"),
            validators.EqualTo('confirm', message='Passwords must match!')
        ],
        render_kw={
            "placeholder": "Password",
            "class": "form-control"
        }
    )
    confirm = PasswordField('Repeat Password',
        render_kw={
            "placeholder": "Confirm Password",
            "class": "form-control"
        }
    )
    name = StringField('FullName',
        render_kw={
            "placeholder": "FullName",
            "class": "form-control"
        }
    )


class LoginForm(Form):
    """Form to be used in login page."""
    username = StringField('Username', [
            validators.Length(min=4, max=49),
            validators.DataRequired("Please, enter your username.")
        ],
        render_kw={
            "placeholder": "Username",
            "class": "form-control"
        }
    )
    password = PasswordField('Password', [
            validators.DataRequired("Please, enter your password")
        ],
        render_kw={
            "placeholder": "Password",
            "class": "form-control"
        }
    )
