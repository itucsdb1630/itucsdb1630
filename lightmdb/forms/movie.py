from wtforms import Form, StringField, IntegerField, validators


class MovieForm(Form):
    title = StringField('Title', [
            validators.Length(min=4, max=49),
            validators.DataRequired("Please, enter movie title.")
        ],
        render_kw={
            "placeholder": "Movie Title",
            "class": "form-control"
        }
    )
    year = IntegerField('Year', [
            validators.NumberRange(min=1600, max=2200, message="Only movies between 1600-2200 can be added"),
            validators.DataRequired("Please, Enter movie release year.")
        ],
        render_kw={
           "placeholder": "Release Year",
           "class": "form-control"
        }
    )
