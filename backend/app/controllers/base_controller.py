from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_json(schema_class):
    """Decorator to validate JSON input using Marshmallow schema"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema = schema_class()
                data = schema.load(request.json or {})
                return f(data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'error': 'Validation error',
                    'messages': err.messages
                }), 400
            except Exception as err:
                return jsonify({
                    'error': 'Invalid JSON format',
                    'message': str(err)
                }), 400
        return decorated_function
    return decorator

def validate_pagination():
    """Decorator to validate pagination parameters"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                page = request.args.get('page', 1, type=int)
                per_page = request.args.get('per_page', 20, type=int)
                
                if page < 1:
                    return jsonify({'error': 'Page must be greater than 0'}), 400
                if per_page < 1 or per_page > 100:
                    return jsonify({'error': 'Per page must be between 1 and 100'}), 400
                
                return f(page, per_page, *args, **kwargs)
            except ValueError:
                return jsonify({'error': 'Invalid pagination parameters'}), 400
        return decorated_function
    return decorator

def handle_not_found(resource_name):
    """Helper function to return 404 error"""
    return jsonify({
        'error': 'Not Found',
        'message': f'{resource_name} not found'
    }), 404

def handle_success(data, message=None, status_code=200):
    """Helper function to return success response"""
    response = {'data': data}
    if message:
        response['message'] = message
    return jsonify(response), status_code

def handle_error(error_message, status_code=500):
    """Helper function to return error response"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': error_message
    }), status_code