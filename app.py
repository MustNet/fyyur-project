# app.py
from datetime import datetime
from sqlalchemy import asc
from sqlalchemy.dialects.postgresql import ARRAY

from flask import (
    Flask, render_template, request, flash, redirect, url_for, abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# WTForms (liegen in forms.py)
from forms import VenueForm, ArtistForm, ShowForm

# -------------------------------------------------
# App / Config
# -------------------------------------------------
app = Flask(__name__)
app.config.from_object("config.Config")  # stellt u.a. SECRET_KEY & SQLALCHEMY_DATABASE_URI bereit

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# -------------------------------------------------
# Models
# -------------------------------------------------
class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    phone = db.Column(db.String(50))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))

    # Mehrfachauswahl (Postgres ARRAY)
    genres = db.Column(ARRAY(db.String()), nullable=False, default=[])

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Beziehung zu Show
    shows = db.relationship(
        "Show",
        back_populates="venue",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return f"<Venue id={self.id} name={self.name!r}>"


class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)

    phone = db.Column(db.String(50))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))

    genres = db.Column(ARRAY(db.String()), nullable=False, default=[])

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    shows = db.relationship(
        "Show",
        back_populates="artist",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self):
        return f"<Artist id={self.id} name={self.name!r}>"


class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)

    # FKs
    artist_id = db.Column(
        db.Integer, db.ForeignKey("artists.id", ondelete="CASCADE"), nullable=False
    )
    venue_id = db.Column(
        db.Integer, db.ForeignKey("venues.id", ondelete="CASCADE"), nullable=False
    )

    # Backrefs
    artist = db.relationship("Artist", back_populates="shows", lazy="joined")
    venue = db.relationship("Venue", back_populates="shows", lazy="joined")

    def __repr__(self):
        return f"<Show id={self.id} artist_id={self.artist_id} venue_id={self.venue_id} start={self.start_time}>"


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def split_shows(shows):
    """Teilt Shows in 'past' und 'upcoming' anhand aktueller Zeit."""
    now = datetime.utcnow()
    past = [s for s in shows if s.start_time < now]
    upcoming = [s for s in shows if s.start_time >= now]
    return past, upcoming


# -------------------------------------------------
# Routes: Home
# -------------------------------------------------
# Home
@app.route("/")
def index():
    latest_venues  = Venue.query.order_by(Venue.created_at.desc()).limit(5).all()
    latest_artists = Artist.query.order_by(Artist.created_at.desc()).limit(5).all()
    upcoming_shows = Show.query.order_by(Show.start_time.asc()).limit(10).all()
    return render_template(
        "pages/home.html",
        latest_venues=latest_venues,
        latest_artists=latest_artists,
        upcoming_shows=upcoming_shows,
    )

@app.get("/health")
def health():
    return {"ok": True}


# -------------------------------------------------
# Routes: Venues
# -------------------------------------------------
@app.get("/venues")
def list_venues():
    venues = Venue.query.order_by(
        asc(Venue.city), asc(Venue.state), asc(Venue.name)
    ).all()
    return render_template("pages/venues.html", venues=venues)


@app.get("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    past, upcoming = split_shows(venue.shows)
    return render_template(
        "pages/venue_detail.html",
        venue=venue,
        past_shows=past,
        upcoming_shows=upcoming,
    )


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        try:
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website_link=form.website_link.data,
                genres=form.genres.data,
                seeking_talent=form.seeking_talent.data or False,
                seeking_description=form.seeking_description.data,
            )
            db.session.add(venue)
            db.session.commit()
            flash(f"Venue '{venue.name}' was successfully listed!", "success")
            return redirect(url_for("show_venue", venue_id=venue.id))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred. Venue could not be listed. {e}", "danger")
        finally:
            db.session.close()
    else:
        flash("Form validation failed. Please check your input.", "danger")
    return render_template("forms/new_venue.html", form=form)


# -------------------------------------------------
# Routes: Artists
# -------------------------------------------------
@app.get("/artists")
def list_artists():
    artists = Artist.query.order_by(asc(Artist.name)).all()
    return render_template("pages/artists.html", artists=artists)


@app.get("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    past, upcoming = split_shows(artist.shows)
    return render_template(
        "pages/artist_detail.html",
        artist=artist,
        past_shows=past,
        upcoming_shows=upcoming,
    )


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm()
    if form.validate_on_submit():
        try:
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                facebook_link=form.facebook_link.data,
                website_link=form.website_link.data,
                genres=form.genres.data,
                seeking_venue=form.seeking_venue.data or False,
                seeking_description=form.seeking_description.data,
            )
            db.session.add(artist)
            db.session.commit()
            flash(f"Artist '{artist.name}' was successfully listed!", "success")
            return redirect(url_for("show_artist", artist_id=artist.id))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred. Artist could not be listed. {e}", "danger")
        finally:
            db.session.close()
    else:
        flash("Form validation failed. Please check your input.", "danger")
    return render_template("forms/new_artist.html", form=form)


# -------------------------------------------------
# Routes: Shows
# -------------------------------------------------
@app.get("/shows")
def list_shows():
    shows = Show.query.order_by(asc(Show.start_time)).all()
    return render_template("pages/shows.html", shows=shows)


@app.route("/shows/create", methods=["GET"])
def create_show_form():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            show = Show(
                artist_id=int(form.artist_id.data),
                venue_id=int(form.venue_id.data),
                start_time=form.start_time.data,
            )
            db.session.add(show)
            db.session.commit()
            flash("Show was successfully listed!", "success")
            return redirect(url_for("list_shows"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred. Show could not be listed. {e}", "danger")
        finally:
            db.session.close()
    else:
        flash("Form validation failed. Please check your input.", "danger")
    return render_template("forms/new_show.html", form=form)


# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
