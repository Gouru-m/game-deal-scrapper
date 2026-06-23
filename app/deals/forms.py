from wtforms import SelectField, DecimalField, BooleanField, SubmitField
from wtforms.validators import Optional, NumberRange
from flask_wtf import FlaskForm

class FilterForm(FlaskForm):
    genre = SelectField(
        "Genre",
        choices=[],
        validators=[Optional()]
    )

    max_price = DecimalField(
        "Maximum Price",
        places= 2,
        validators=[
            Optional(),
            NumberRange(min=0, message="Prices cannot be negative.")
        ]
    )

    best_only = BooleanField("Best deals only")

    submit = SubmitField("Apply filters")

    class Meta:
        csrf = False
        #Do not need csrf as they do not modify server-side data.

    def __init__(self, *args, genres=None,**kwargs):
        super().__init__(*args, **kwargs)

        genre_choices = [("", "All genres")]

        if genres:
            genre_choices.extend((genre,genre) for genre in genres)

        self.genre.choices = genre_choices

class RefreshDealsForm(FlaskForm):
    submit = SubmitField("Refresh scraped deals")