# models.py
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from extensions import db

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

    genres = db.Column(ARRAY(db.String()), nullable=False, default=[])
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    venue_id  = db.Column(db.Integer, db.ForeignKey("venues.id",  ondelete="CASCADE"), nullable=False)

    artist = db.relationship("Artist", back_populates="shows", lazy="joined")
    venue  = db.relationship("Venue",  back_populates="shows", lazy="joined")

    def __repr__(self):
        return f"<Show id={self.id} artist_id={self.artist_id} venue_id={self.venue_id} start={self.start_time}>"
