from app import app, db
from models import Episode, Guest, Appearance
from datetime import datetime

def seed_database():
    with app.app_context():
        db.create_all()

        episode1 = Episode(date=datetime(1999, 1, 11), number=1)
        episode2 = Episode(date=datetime(1999, 1, 12), number=2)

        guest1 = Guest(name="Michael J. Fox", occupation="actor")
        guest2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        guest3 = Guest(name="Tracey Ullman", occupation="television actress") 

        appearance1 = Appearance(rating=5, episode_id=1, guest_id=1)
        appearance2 = Appearance(rating=4, episode_id=2, guest_id=2)
        appearance3 = Appearance(rating=5, episode_id=2, guest_id=3)  

        db.session.add_all([episode1, episode2, guest1, guest2, guest3, appearance1, appearance2, appearance3])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()