# Lateshow Heroes API

A Flask-based API to manage and track episodes, guests, and their appearances on a late-night show.

---

## Features

- **Episodes**: List all episodes or retrieve details about a specific episode.
- **Guests**: List all guests in the system.
- **Appearances**: Record a guest's appearance in an episode, including their rating (1-5).
- **Relationships**: Maintain relationships between episodes, guests, and appearances.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <https://github.com/mitch-spec4/lateshow-mitch-kamau>
   cd lateshow-mitch-kamau
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Initialize migrations:
     ```bash
     flask db init
     ```
   - Generate migration files:
     ```bash
     flask db migrate -m "Create tables"
     ```
   - Apply migrations:
     ```bash
     flask db upgrade
     ```

5. **Seed the Database**:
   ```bash
   python3 seed.py
   ```

6. **Run the Application**:
   ```bash
   flask run
   ```

---

## API Endpoints

### **1. Episodes**

#### **GET /episodes**
- **Description**: Retrieve a list of all episodes.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "date": "1/11/99",
      "number": 1
    },
    {
      "id": 2,
      "date": "1/12/99",
      "number": 2
    }
  ]
  ```

#### **GET /episodes/:id**
- **Description**: Retrieve details about a specific episode, including its appearances and related guests.
- **Response** (if the episode exists):
  ```json
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1,
    "appearances": [
      {
        "id": 1,
        "rating": 4,
        "episode_id": 1,
        "guest_id": 1,
        "guest": {
          "id": 1,
          "name": "Michael J. Fox",
          "occupation": "actor"
        }
      }
    ]
  }
  ```
- **Response** (if the episode does not exist):
  ```json
  {
    "error": "Episode not found"
  }
  ```

---

### **2. Guests**

#### **GET /guests**
- **Description**: Retrieve a list of all guests.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Michael J. Fox",
      "occupation": "actor"
    },
    {
      "id": 2,
      "name": "Sandra Bernhard",
      "occupation": "Comedian"
    },
    {
      "id": 3,
      "name": "Tracey Ullman",
      "occupation": "television actress"
    }
  ]
  ```

---

### **3. Appearances**

#### **POST /appearances**
- **Description**: Create a new appearance for a guest in an episode.
- **Request Body**:
  ```json
  {
    "rating": 5,
    "episode_id": 2,
    "guest_id": 3
  }
  ```
- **Response** (if successful):
  ```json
  {
    "id": 162,
    "rating": 5,
    "guest_id": 3,
    "episode_id": 2,
    "episode": {
      "date": "1/12/99",
      "id": 2,
      "number": 2
    },
    "guest": {
      "id": 3,
      "name": "Tracey Ullman",
      "occupation": "television actress"
    }
  }
  ```
- **Response** (if validation fails):
  ```json
  {
    "errors": ["Validation errors"]
  }
  ```

---

## Database Schema

### **Tables**
1. **Episodes**
   - `id`: Primary key
   - `date`: Date of the episode
   - `number`: Episode number

2. **Guests**
   - `id`: Primary key
   - `name`: Name of the guest
   - `occupation`: Occupation of the guest

3. **Appearances**
   - `id`: Primary key
   - `rating`: Rating of the guest's appearance (1-5)
   - `episode_id`: Foreign key referencing `Episodes`
   - `guest_id`: Foreign key referencing `Guests`

---

## Validations

- **Appearance**:
  - `rating` must be between 1 and 5 (inclusive).

---

## Testing the API

1. **Using Postman**:
   - Import the provided Postman collection to test all endpoints.

2. **Using `curl`**:
   - Example: Test the `/episodes` endpoint:
     ```bash
     curl http://127.0.0.1:5000/episodes
     ```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
