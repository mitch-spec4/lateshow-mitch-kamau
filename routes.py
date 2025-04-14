# routes.py
from flask import request, jsonify
from models import db, Episode, Guest, Appearance

def setup_routes(app):
    
    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        episodes = Episode.query.all()
        return jsonify([episode.to_dict() for episode in episodes])

    @app.route('/episodes/<int:id>', methods=['GET'])
    def get_episode_by_id(id):
        episode = Episode.query.get(id)
        if episode:
            return jsonify(episode.to_dict())
        return jsonify({"error": "Episode not found"}), 404

    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()
        return jsonify([guest.to_dict() for guest in guests])

    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        data = request.json
        rating = data.get('rating')

        if not (1 <= rating <= 5):
            return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

        appearance = Appearance(
            rating=rating,
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()

        return jsonify(appearance.to_dict()), 201
