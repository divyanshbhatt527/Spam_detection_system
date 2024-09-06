from flask import Blueprint, request, jsonify
from models import db, User, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import is_phone_number, search_by_name, search_by_phone_number, report_spam, validate_contact_data, check_existing_contact, add_new_contact, validate_phone_number

user_routes = Blueprint('user_routes', __name__)
contact_routes = Blueprint('contact_routes', __name__)
search_routes = Blueprint('search_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify(message="No input data provided"), 400
    
    required_fields = ['name', 'phone_number', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify(message=f"Missing required field: {field}"), 400

    name = data['name']
    phone_number = data['phone_number']
    password = data['password']
    email = data.get('email')

    if not validate_phone_number(phone_number) or len(phone_number) < 10:
        return jsonify(error="Invalid phone number format"), 400

    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify(error="Phone number already registered"), 400
    if email and User.query.filter_by(email=email).first():
        return jsonify(error="Email address already registered"), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(name=name, phone_number=phone_number, email=email, password=hashed_password)
    
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(error="An error occurred while registering the user"), 500

    return jsonify(message="User registered successfully"), 201

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify(error="No input data provided"), 400
    
    required_fields = ['phone_number', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify(error=f"Missing required field: {field}"), 400

    phone_number = data['phone_number']
    password = data['password']

    
    if not validate_phone_number(phone_number) or len(phone_number) < 10:
        return jsonify(error="Invalid phone number format"), 400

    user = User.query.filter_by(phone_number=phone_number).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify(error="Invalid credentials"), 401

@contact_routes.route('/contacts', methods=['POST'])
@jwt_required()
def add_contact():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify(message="No input data provided"), 400
        
        validation_error = validate_contact_data(data)
        if validation_error:
            return validation_error
        
        name = data['name']
        phone_number = data['phone_number']
        user_id = get_jwt_identity()

        existing_contact_error = check_existing_contact(phone_number, user_id)
        if existing_contact_error:
            return existing_contact_error
        
        return add_new_contact(name, phone_number, user_id)
    except Exception as e:
        return jsonify(message="An unexpected error occurred", error=str(e)), 500

@contact_routes.route('/spam', methods=['POST'])
@jwt_required()
def report_spam_route():
    data = request.get_json()

    if not data or 'phone_number' not in data:
        return jsonify(message="Phone number is required"), 400

    phone_number = data['phone_number']
    try:
        result = report_spam(phone_number)  
        return jsonify(message=result), 201
    except Exception as e:
        return jsonify(message=str(e)), 500

@search_routes.route('/search', methods=['GET'])
@jwt_required()
def search():
    search_input = request.args.get('search_input')
    
    if not search_input:
        return jsonify(message="Query parameter 'search_input' is required"), 400
    
    # Identifying if input is a phone number or name
    if is_phone_number(search_input):
        return search_by_phone_number(search_input)
    else:
        return search_by_name(search_input)
