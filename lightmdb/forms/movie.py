from wtforms import Form, StringField

class MovieForm(Form):
    year = StringField('Title',
                    render_kw={
                        "placeholder": "Title",
                        "class": "form-control"
                    }
                    )
    year = StringField('Year',
                   render_kw={
                       "placeholder": "Year",
                       "class": "form-control"
                   }
                   )