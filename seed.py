import csv
import random
from datetime import datetime
from app import create_app
from app.models import db, Episode, Guest, Appearance

app = create_app()

def seed_database():
    with app.app_context():
        print("Resetting the database...")
        db.drop_all()
        db.create_all()

        seen_dates = set()
        guest_cache = {}

        episode_number = 1

        with open('data/seed.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                
                raw_date = row['Show'].strip()
                try:
                    episode_date = datetime.strptime(raw_date, "%m/%d/%y").date()
                except ValueError:
                    print(f"Skipping invalid date: {raw_date}")
                    continue

                if episode_date not in seen_dates:
                    episode = Episode(date=episode_date, number=episode_number)
                    db.session.add(episode)
                    db.session.flush()
                    episode_number += 1
                    seen_dates.add(episode_date)
                else:
                    episode = Episode.query.filter_by(date=episode_date).first()

                guest_name = row['Raw_Guest_List'].strip()
                guest_occupation = row['GoogleKnowlege_Occupation'].strip()

                if guest_name not in guest_cache:
                    guest = Guest(name=guest_name, occupation=guest_occupation)
                    db.session.add(guest)
                    db.session.flush()
                    guest_cache[guest_name] = guest
                else:
                    guest = guest_cache[guest_name]

                appearance = Appearance(
                    rating=random.randint(1, 5),
                    episode_id=episode.id,
                    guest_id=guest.id
                )
                db.session.add(appearance)

        db.session.commit()
        print("Seeding complete.")

if __name__ == '__main__':
    seed_database()
