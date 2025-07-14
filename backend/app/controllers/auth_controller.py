from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .base_controller import validate_json, handle_success, handle_error

auth_bp = Blueprint('auth', __name__)

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=100))

@auth_bp.route('/login', methods=['POST'])
@validate_json(LoginSchema)
def login(data):
    """
    Login endpoint (simplified for demo)
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              maxLength: 50
            password:
              type: string
              maxLength: 100
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            message:
              type: string
      401:
        description: Invalid credentials
    """
    try:
        username = data['username']
        password = data['password']
        
        # Simplified authentication (in production, use proper password hashing)
        if username == 'admin' and password == 'admin123':
            access_token = create_access_token(identity=username)
            return handle_success({
                'access_token': access_token,
                'username': username
            }, 'Login successful')
        else:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username or password is incorrect'
            }), 401
    except Exception as e:
        return handle_error(str(e))

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected endpoint example
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Access granted
      401:
        description: Unauthorized
    """
    try:
        current_user = get_jwt_identity()
        return handle_success({
            'user': current_user,
            'message': 'Access granted to protected route'
        })
    except Exception as e:
        return handle_error(str(e))

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Current user information
      401:
        description: Unauthorized
    """
    try:
        current_user = get_jwt_identity()
        return handle_success({
            'username': current_user,
            'role': 'admin'  # Simplified role
        })
    except Exception as e:
        return handle_error(str(e))