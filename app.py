from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

from routes import user_routes, contact_routes, search_routes
app.register_blueprint(user_routes)
app.register_blueprint(contact_routes)
app.register_blueprint(search_routes)

with app.app_context():
    try:
        db.create_all()  
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    app.run(debug=True)
