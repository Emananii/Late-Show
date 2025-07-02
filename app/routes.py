from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from .models import db, Episode, Guest, Appearance

api = Blueprint("api", __name__)


# GET /episodes — list all episodes
@api.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict(include_appearances=False) for e in episodes]), 200


# GET /episodes/<id> — episode details with appearances and nested guest info
@api.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    return jsonify(episode.to_dict(include_appearances=True)), 200


# GET /guests — list all guests
@api.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests]), 200


# DELETE /episodes/<id>
@api.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)

    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    deleted_data = episode.to_dict(include_appearances=False)

    try:
        db.session.delete(episode)
        db.session.commit()
        return jsonify({
            "message": f"Episode {id} deleted successfully",
            "deleted_episode": deleted_data
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Could not delete episode",
            "details": str(e)
        }), 500


# POST /appearances — create a new appearance
@api.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    rating = data.get("rating")
    episode_id = data.get("episode_id")
    guest_id = data.get("guest_id")

    errors = []

    if rating is None or episode_id is None or guest_id is None:
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

        return jsonify(new_appearance.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Database error occurred"]}), 500
