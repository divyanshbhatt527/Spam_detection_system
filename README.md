# Contact Management API

This project is a RESTful API built using Flask, SQLAlchemy, and JWT for managing users, contacts, and spam reporting. It includes features like user registration, login, contact management, spam detection, and search functionalities.

## Features
- **User Registration & Login**: Users can register with their name, phone number, email, and password. Login is protected using JWT.
- **Contact Management**: Authenticated users can add contacts and report phone numbers as spam.
- **Search**: Search for users or contacts by name or phone number.
- **Spam Detection**: Report phone numbers as spam and track spam likelihood for each number.

## Tech Stack
- **Flask**: Lightweight Python web framework.
- **SQLAlchemy**: ORM for database interaction.
- **JWT (JSON Web Tokens)**: Secure authentication.
- **SQLite**: Default database for local testing (can be swapped for PostgreSQL).
  
## Endpoints
1. **User Registration**: `/register` (POST)  
   Register a new user with required details.
   
2. **User Login**: `/login` (POST)  
   Login with a registered phone number and password to receive a JWT access token.
   
3. **Add Contact**: `/contacts` (POST)  
   Add a new contact to your contact list (JWT required).
   
4. **Report Spam**: `/spam` (POST)  
   Report a phone number as spam (JWT required).
   
5. **Search**: `/search` (GET)  
   Search for a user or contact by name or phone number (JWT required).

## Getting Started

### Prerequisites
- Python 3.7 or above
- Flask, SQLAlchemy, Flask-JWT-Extended, and related dependencies

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/contact-management-api.git
   cd contact-management-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

### Configuration
- The app uses a local SQLite database by default. You can modify the `SQLALCHEMY_DATABASE_URI` in `config.py` to use PostgreSQL or any other database.
- Update the `SECRET_KEY` and `JWT_SECRET_KEY` in `config.py` for production environments.

  
