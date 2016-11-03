from wtforms import Form, validators, StringField, TextAreaField
from wtforms.fields.html5 import EmailField


class ContactForm(Form):
    """Form to be used in contactus page."""
    title = StringField('title', [
            validators.Length(min=5, max=100),
            validators.DataRequired("Please, enter title.")
        ],
        render_kw={
            "placeholder": "Title",
            "class": "form-control"
        }
    )
    content = TextAreaField('Content', [
            validators.Length(min=10, max=255),
            validators.DataRequired("Please, enter content.")
        ],
        render_kw={
            "placeholder": "Content",
            "type" : "textarea",
            "class": "form-control",
            "rows": "10",
            "cols": "50"
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
    phone = StringField('phone', [
        validators.Length(min=5, max=50),
        validators.DataRequired("Please, enter phone number.")
        ],
        render_kw={
          "placeholder": "Phone number",
          "class": "form-control"
        }
    )
