from wtforms import Form, StringField, RadioField, validators

class PlaylistForm(Form):
    name = StringField('Name', [
            validators.Length(min=4, max=49),
            validators.DataRequired("Please, enter playlist name.")
        ],
        render_kw={
            "placeholder": "Playlist Name",
            "class": "form-control"
        }
                       )
    privacy = RadioField('Privacy', choices=[('Public','Public'),('Private','Private')])