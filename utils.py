import phonenumbers

from flask import jsonify
from models import db, User, Contact, SpamReport
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError


def is_phone_number(search_input):
    return validate_phone_number(search_input) and len(search_input) >= 7 

def search_by_phone_number(phone_number):
    """
    Search for a person by phone number in the global database. 
    Finding registered users with the given phone number. 
    If no registered users are found, it searches in the contacts database. 
    If no records are found in both, it returns a 404 error. 
    """
    try:
        # Search for registered users
        results = User.query.filter_by(phone_number=phone_number).all()
        
        # If no registered users exists then, search in contacts
        if not results:
            results = Contact.query.filter_by(phone_number=phone_number).all()
            if not results:
                return jsonify(message="No records found for the given phone number"), 404
        
        response = [{
            'name': user.name,
            'phone_number': user.phone_number,
            'spam_likelihood': get_spam_likelihood(user.phone_number),
            'email': get_email_if_contact(user.id)
        } for user in results]

        return jsonify(response), 200
    
    except SQLAlchemyError as e:
        return jsonify(message="Database error occurred", error=str(e)), 500
    
    except Exception as e:
        return jsonify(message="An unexpected error occurred", error=str(e)), 500

def search_by_name(name_query):
    """
    Search for a person by name in the global database. 
    Searches for users whose names start with the given query and users whose names contain the query but do not start with it.
    Returns results with names, phone numbers, and spam likelihoods.
    """
    try:

         # Search in the User model
        users_starting_with_query = User.query.filter(User.name.ilike(f'{name_query}%')).all()
        users_containing_query = User.query.filter(User.name.ilike(f'%{name_query}%')).filter(~User.name.ilike(f'{name_query}%')).all()
        
        # Search in the Contact model
        contacts_starting_with_query = Contact.query.filter(Contact.name.ilike(f'{name_query}%')).all()
        contacts_containing_query = Contact.query.filter(Contact.name.ilike(f'%{name_query}%')).filter(~Contact.name.ilike(f'{name_query}%')).all()
        
        # Combine results
        combined_results = users_starting_with_query + contacts_starting_with_query + users_containing_query + contacts_containing_query

        if not combined_results:
            return jsonify(message="No contact found!!"), 200
        
        response = [{
            'name': user.name,
            'phone_number': user.phone_number,
            'spam_likelihood': get_spam_likelihood(user.phone_number)
        } for user in combined_results]

        return jsonify(response), 200
    
    except Exception as e:
        return jsonify(message="An error occurred while searching by name", error=str(e)), 500

def get_spam_likelihood(phone_number):

    spam_report = SpamReport.query.filter_by(phone_number=phone_number).first()
    return spam_report.spam_count if spam_report else 0


def get_email_if_contact(user_id):
    current_user_id = get_jwt_identity()
    contact = Contact.query.filter_by(user_id=current_user_id, phone_number=User.query.get(user_id).phone_number).first()
    return User.query.get(user_id).email if contact else None

    
def report_spam(phone_number):
    """
    Report a phone number as spam. If the phone number already exists in the SpamReport table, 
    increment the spam count. If it does not exist, create a new entry for the phone number.
    """

    if not phone_number:
        return "Phone number is required."

    spam_report = SpamReport.query.filter_by(phone_number=phone_number).first()
    if spam_report:
        spam_report.spam_count += 1
    else:
        spam_report = SpamReport(phone_number=phone_number)
        db.session.add(spam_report)

    try:
        db.session.commit()
        return "Number reported as spam successfully."
    except Exception as e:
        db.session.rollback()
        raise Exception(f"An error occurred: {str(e)}")
    
def validate_contact_data(data):
    """
    Validate that the necessary contact data is present in the request.
    """
    name = data.get('name')
    phone_number = data.get('phone_number')
    
    if not name or not phone_number:
        return jsonify(message="Missing 'name' or 'phone_number' in request data"), 400

    return None

def check_existing_contact(phone_number, user_id):
    """
    Check if a contact with the given phone number already exists for the user.
    """
    existing_contact = Contact.query.filter_by(phone_number=phone_number, user_id=user_id).first()
    if existing_contact:
        return jsonify(message="Contact with this phone number already exists"), 409

    return None

def add_new_contact(name, phone_number, user_id):
    """
    Add a new contact to the database.
    """
    try:
        contact = Contact(name=name, phone_number=phone_number, user_id=user_id)
        db.session.add(contact)
        db.session.commit()
        return jsonify(message="Contact added successfully"), 201
    except SQLAlchemyError as e:
        db.session.rollback()  
        return jsonify(message="Database error occurred", error=str(e)), 500
    
def validate_phone_number(phone_number):
    """
    Validates phone numbers containing only digits, spaces, dashes, parentheses, and the plus sign.
    """
    allowed_chars = set('0123456789-() +')
    
    # Check if all characters in phone_number are allowed
    if all(char in allowed_chars for char in phone_number) and len(phone_number) >= 7:
        return True  
    else:
        return False