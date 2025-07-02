from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import date

db = SQLAlchemy()


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship(
        'Appearance',
        back_populates='episode',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    serialize_rules = ('-appearances.episode',)

    def to_dict(self, include_appearances=True):
        episode_dict = {
            "id": self.id,
            "date": self.date.strftime('%-m/%-d/%y') if isinstance(self.date, date) else self.date,
            "number": self.number,
        }

        if include_appearances:
            episode_dict["appearances"] = [a.to_dict(include_episode=False) for a in self.appearances]

        return episode_dict


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)

    appearances = db.relationship(
        'Appearance',
        back_populates='guest',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    serialize_rules = ('-appearances.guest',)

    def to_dict(self, include_appearances=False):
        guest_dict = {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation,
        }

        if include_appearances:
            guest_dict["appearances"] = [a.to_dict(include_guest=False) for a in self.appearances]

        return guest_dict


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(
        db.Integer,
        db.ForeignKey('episodes.id', ondelete='CASCADE'),
        nullable=False
    )

    guest_id = db.Column(
        db.Integer,
        db.ForeignKey('guests.id', ondelete='CASCADE'),
        nullable=False
    )

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def to_dict(self, include_episode=True, include_guest=True):
        appearance_dict = {
            "id": self.id,
            "rating": self.rating,
            "episode_id": self.episode_id,
            "guest_id": self.guest_id,
        }

        if include_episode and self.episode:
            appearance_dict["episode"] = self.episode.to_dict(include_appearances=False)

        if include_guest and self.guest:
            appearance_dict["guest"] = self.guest.to_dict(include_appearances=False)

        return appearance_dict
