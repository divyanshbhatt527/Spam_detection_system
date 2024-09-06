from app import app,db
from models import User, Contact

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'User: {user.name}, Phone: {user.phone_number}, Email: {user.email}')
        contacts = Contact.query.filter_by(user_id=user.id).all()
        for contact in contacts:
            print(f'  Contact: {contact.name}, Phone: {contact.phone_number}')
