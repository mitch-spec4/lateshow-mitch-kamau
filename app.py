from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models.models import db, Episode, Guest, Appearance

app = Flask(__name__)


app.config.from_object('config.Config')


db.init_app(app)
migrate = Migrate(app, db)

# GET /episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    try:
        episodes = Episode.query.all()
        return jsonify([episode.to_dict(include_appearances=True) for episode in episodes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /episodes/<id>
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    try:
        episode = db.session.get(Episode, id)
        if episode:
            return jsonify(episode.to_dict(include_appearances=True)), 200
        return jsonify({"error": "Episode not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /guests
@app.route('/guests', methods=['GET'])
def get_guests():
    try:
        guests = Guest.query.all()
        return jsonify([guest.to_dict() for guest in guests]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST /appearances
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.json
        print("Request Data: ", data)

        rating = data.get('rating')
        if not (1 <= rating <= 5):
            return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

        episode = db.session.get(Episode, data.get('episode_id'))
        guest = db.session.get(Guest, data.get('guest_id'))

        if not episode or not guest:
            print(f"Episode: {episode}, Guest: {guest}")
            return jsonify({"errors": ["Episode or Guest not found"]}), 404

        appearance = Appearance(
            rating=rating,
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict(include_nested=True)), 201
    except Exception as e:
        print("Error: ", str(e))
        db.session.rollback()
        return jsonify({"errors": str(e)}), 500

# DELETE /episodes/<id>
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    try:
        episode = db.session.get(Episode, id)
        if episode:
            db.session.delete(episode)
            db.session.commit()
            return jsonify({"message": "Episode deleted successfully"}), 200
        return jsonify({"error": "Episode not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE /guests/<id>
@app.route('/guests/<int:id>', methods=['DELETE'])
def delete_guest(id):
    try:
        guest = db.session.get(Guest, id)
        if guest:
            db.session.delete(guest)
            db.session.commit()
            return jsonify({"message": "Guest deleted successfully"}), 200
        return jsonify({"error": "Guest not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
