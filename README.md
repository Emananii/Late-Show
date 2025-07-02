# 🎤 Late Show API

A RESTful Flask API for managing episodes, guests, and their appearances on a fictional late-night talk show. Designed to support frontend consumption via clean, nested JSON responses.

---

## 📌 Features

- View all talk show episodes with air dates and episode numbers
- View individual episode details including guest appearances
- Browse all show guests and their occupations
- Create new guest appearances and assign them to episodes
- Delete episodes, along with their associated appearances
- JSON responses follow best practices and include nested objects
- Handles invalid requests with proper HTTP status codes and clear error messages


## 🗂️ Project Structure
```
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
├── migrations/
├── data/
│ ├── seed.csv
├── seed.py
├── requirements.txt 
├── README.md

```

## 🚀 Getting Started

### 1. Clone the Repository
```
git clone https://github.com/Emananii/Late-Show.git
cd Late-Show
```
### 2. Set Up the Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows (PowerShell)
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Set Environment Variables
```
export FLASK_APP=app
export FLASK_ENV=development
```
### 5. Run Migrations
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
### 6. Seed the Database
```
python3 seed.py
```
### 7. Run the Server
```
flask run
```
## Example JSON Responses
### ✅ GET /episodes
```
[
  {
    "id": 1,
    "date": "5/28/24",
    "number": 101
  },
  ...
]
```
### ✅ GET /episodes/1
```
{
  "id": 1,
  "date": "5/28/24",
  "number": 101,
  "appearances": [
    {
      "id": 1,
      "rating": 5,
      "guest_id": 2,
      "episode_id": 1,
      "guest": {
        "id": 2,
        "name": "Jane Doe",
        "occupation": "Comedian"
      }
    }
  ]
}
```
### ❌ GET /episodes/999
```
{
  "error": "Episode not found"
}
```
## 📦 Dependencies

- Flask

- Flask-SQLAlchemy

- Flask-Migrate

- SQLAlchemy Serializer

- Python 3.8+

### You can install them all with:
```
pip install -r requirements.txt
```
## 👨‍💻 Author
```
Emmanuel Wambugu Ndiritu
GitHub: @Emananii
Email: emmanuelwambugu5@gmail.com
```
## 📄 License
This project is licensed under the MIT License.