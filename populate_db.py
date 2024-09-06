from app import app,db
from models import User, Contact
from faker import Faker

fake = Faker()

def populate_db(num_users=10):
    for _ in range(num_users):
        user = User(
            name=fake.name(),
            phone_number=fake.phone_number(),
            email=fake.email(),
            password=fake.password()
        )
        db.session.add(user)
        db.session.commit()

        for _ in range(5):
            contact = Contact(
                name=fake.name(),
                phone_number=fake.phone_number(),
                user_id=user.id
            )
            db.session.add(contact)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        populate_db()
