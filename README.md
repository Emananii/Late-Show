# Late Show API

A Flask-based backend application for managing episodes, guests, and their appearances on a late-night talk show.

## Project Structure

├── app/
├── init.py
├── models.py
├── routes.py
├── migrations/
├── data/
├── seed.csv
├── seed.py
├── requirements.txt
├── README.md

## Setup Instructions

1. **Clone the repository**

git clone <repository-url>
cd Late-Show

2. **Set up the virtual environment**

python3 -m venv venv
source venv/bin/activate

3. **Install dependencies**

pip install -r requirements.txt

4. **Set environment variables**

export FLASK_APP=app
export FLASK_ENV=development

5. **Run Database Migrations**

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

6. **Seed the Database**

python3 seed.py

7. **Run the Server**

Flask Run

## Dependencies

Flask

Flask-SQLAlchemy

Flask-Migrate

SQLAlchemy-Serializer

## License

This project is licensed under the MIT License.
