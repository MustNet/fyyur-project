from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL

# Choices für States und Genres
state_choices = [
    ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
    # ... (weitere States hier auffüllen)
    ('WY', 'WY'),
]

genre_choices = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Swing', 'Swing'),
    ('Other', 'Other'),
]

class ShowForm(FlaskForm):
    artist_id = StringField('artist_id', validators=[DataRequired()])
    venue_id = StringField('venue_id', validators=[DataRequired()])
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],
                        choices=state_choices)
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone')
    image_link = StringField('image_link', validators=[URL()])
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genre_choices
    )
    facebook_link = StringField('facebook_link', validators=[URL()])
    website_link = StringField('website_link')
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')

class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],
                        choices=state_choices)
    phone = StringField('phone')
    image_link = StringField('image_link', validators=[URL()])
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=genre_choices
    )
    facebook_link = StringField('facebook_link', validators=[URL()])
    website_link = StringField('website_link')
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
