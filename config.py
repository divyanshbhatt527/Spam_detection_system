import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'temporary_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'temporary_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 
