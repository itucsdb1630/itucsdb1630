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
            "class": "form-control",
            "type": "number",
            "min": 1600,
            "max": 2200
        }
    )
    synopsis = StringField('Synopsis', [
            validators.Length(min=5, max=254),
            validators.DataRequired("Please, enter short plot synopsis.")
        ],
        render_kw={
            "placeholder": "Plot Synopsis",
            "class": "form-control",
            "type": "textarea",
        }
    )


class UpdateMovieForm(MovieForm):
    pk = IntegerField(
        'Identifier',
        render_kw={
            "class": "hidden"
        }
    )
