from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes]), 200

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if episode:
        return jsonify({
            "id": episode.id,
            "date": episode.date.strftime("%m/%d/%y"),
            "number": episode.number,
            "appearances": [appearance.to_dict_with_related() for appearance in episode.appearances]
        }), 200
    else:
        return jsonify({"error": "Episode not found"}), 404

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests]), 200

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        if not all(key in data for key in ("rating", "episode_id", "guest_id")):
            return jsonify({"errors": ["Missing required fields"]}), 400

        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(new_appearance)
        db.session.commit()

        return jsonify(new_appearance.to_dict_with_related()), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["Failed to create appearance", str(e)]}), 500

@app.route('/search_table', methods=['GET'])
def search_table():
    table_name = request.args.get('table_name')  
    if not table_name:
        return jsonify({"error": "Table name is required"}), 400

    try:
        if table_name == "episodes":
            rows = Episode.query.all()
            return jsonify([row.to_dict() for row in rows])
        elif table_name == "guests":
            rows = Guest.query.all()
            return jsonify([row.to_dict() for row in rows])
        elif table_name == "appearances":
            rows = Appearance.query.all()
            return jsonify([row.to_dict_with_related() for row in rows])
        else:
            return jsonify({"error": f"Table '{table_name}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

@app.route('/show_tables', methods=['GET'])
def show_tables():
    try:
        episodes = Episode.query.all()
        episodes_data = [episode.to_dict() for episode in episodes]

        guests = Guest.query.all()
        guests_data = [guest.to_dict() for guest in guests]

        appearances = Appearance.query.all()
        appearances_data = [appearance.to_dict_with_related() for appearance in appearances]

        return jsonify({
            "episodes": episodes_data,
            "guests": guests_data,
            "appearances": appearances_data
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

@app.route('/show_all_tables', methods=['GET'])
def show_all_tables():
    try:
        episodes = Episode.query.all()
        episodes_data = [episode.to_dict() for episode in episodes]

        guests = Guest.query.all()
        guests_data = [guest.to_dict() for guest in guests]

        appearances = Appearance.query.all()
        appearances_data = [appearance.to_dict_with_related() for appearance in appearances]

        return jsonify({
            "episodes": episodes_data,
            "guests": guests_data,
            "appearances": appearances_data
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def show_table_data():
    table_name = request.args.get('table_name')  
    if not table_name:
        return jsonify({"error": "Table name is required"}), 400

    try:
        if table_name == "episodes":
            rows = Episode.query.all()
            return jsonify([row.to_dict() for row in rows]), 200
        elif table_name == "guests":
            rows = Guest.query.all()
            return jsonify([row.to_dict() for row in rows]), 200
        elif table_name == "appearances":
            rows = Appearance.query.all()
            return jsonify([row.to_dict() for row in rows]), 200
        else:
            return jsonify({"error": f"Table '{table_name}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Hello, Postman!"}), 200

@app.route('/show_db', methods=['GET'])
def show_db():
    table_name = request.args.get('table_name')  
    if not table_name:
        return jsonify({"error": "Table name is required"}), 400

    try:
        if table_name == "episodes":
            rows = Episode.query.all()
            return jsonify([row.to_dict() for row in rows]), 200
        elif table_name == "guests":
            rows = Guest.query.all()
            return jsonify([row.to_dict() for row in rows]), 200
        elif table_name == "appearances":
            rows = Appearance.query.all()
            return jsonify([row.to_dict_with_related() for row in rows]), 200
        else:
            return jsonify({"error": f"Table '{table_name}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)