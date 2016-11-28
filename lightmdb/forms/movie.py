from wtforms import Form, StringField,validators

class MovieForm(Form):
	title = StringField('Title',
					render_kw={
						"placeholder": "Title",
						"class": "form-control"
					}
					)
	year = StringField('year', [
		validators.Length(min=4, max=4),
		validators.DataRequired("Enter the year of the film.")
		],
		render_kw={
			"placeholder": "Phone number",
			"class": "form-control"	
		}
		)

