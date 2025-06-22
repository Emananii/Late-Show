from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from .models import db, Episode, Guest, Appearance

api = Blueprint("api", __name__)

@api.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        "id": episode.id,
        "date": episode.date.strftime('%-m/%-d/%y'),
        "number": episode.number
    } for episode in episodes]), 200


@api.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if episode is None:
        return jsonify({"error": "Episode not found"}), 404

    return jsonify({
        "id": episode.id,
        "date": episode.date.strftime('%-m/%-d/%y'),
        "number": episode.number,
        "appearances": [
            {
                "id": appearance.id,
                "rating": appearance.rating,
                "guest_id": appearance.guest_id,
                "episode_id": appearance.episode_id,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                }
            } for appearance in episode.appearances
        ]
    }), 200


@api.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        "id": guest.id,
        "name": guest.name,
        "occupation": guest.occupation
    } for guest in guests]), 200


@api.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    rating = data.get("rating")
    episode_id = data.get("episode_id")
    guest_id = data.get("guest_id")

    errors = []

    if not all([rating, episode_id, guest_id]):
        errors.append("All fields (rating, episode_id, guest_id) are required")

    if not isinstance(rating, int) or not (1 <= rating <= 5):
        errors.append("Rating must be an integer between 1 and 5")

    episode = Episode.query.get(episode_id)
    if not episode:
        errors.append("Episode does not exist")

    guest = Guest.query.get(guest_id)
    if not guest:
        errors.append("Guest does not exist")

    if errors:
        return jsonify({"errors": errors}), 400

   
    try:
        new_appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )

        db.session.add(new_appearance)
        db.session.commit()

       
        return jsonify({
            "id": new_appearance.id,
            "rating": new_appearance.rating,
            "guest_id": new_appearance.guest_id,
            "episode_id": new_appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date.strftime('%-m/%-d/%y'),
                "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Database error occurred"]}), 500
