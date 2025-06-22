from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

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