from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from app.services.owner_service import OwnerService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

owner_bp = Blueprint('owner', __name__)

class OwnerSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    city = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    telephone = fields.Str(required=True, validate=validate.Length(min=1, max=20))

class OwnerUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=30))
    last_name = fields.Str(validate=validate.Length(min=1, max=30))
    address = fields.Str(validate=validate.Length(min=1, max=255))
    city = fields.Str(validate=validate.Length(min=1, max=80))
    telephone = fields.Str(validate=validate.Length(min=1, max=20))

@owner_bp.route('', methods=['GET'])
@validate_pagination()
def get_owners(page, per_page):
    """
    Get all owners with pagination
    ---
    tags:
      - Owners
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        default: 20
        description: Items per page (max 100)
      - name: search
        in: query
        type: string
        description: Search term for name, address, city, or telephone
    responses:
      200:
        description: List of owners
    """
    try:
        search_term = request.args.get('search')
        
        if search_term:
            result = OwnerService.search_owners(search_term, page, per_page)
        else:
            result = OwnerService.get_all(page, per_page)
        
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@owner_bp.route('/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):
    """
    Get owner by ID
    ---
    tags:
      - Owners
    parameters:
      - name: owner_id
        in: path
        type: integer
        required: true
        description: Owner ID
    responses:
      200:
        description: Owner details
      404:
        description: Owner not found
    """
    try:
        owner = OwnerService.get_by_id(owner_id)
        if not owner:
            return handle_not_found('Owner')
        
        return handle_success(owner.to_dict())
    except Exception as e:
        return handle_error(str(e))

@owner_bp.route('', methods=['POST'])
@validate_json(OwnerSchema)
def create_owner(data):
    """
    Create a new owner
    ---
    tags:
      - Owners
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
            - address
            - city
            - telephone
          properties:
            first_name:
              type: string
              maxLength: 30
            last_name:
              type: string
              maxLength: 30
            address:
              type: string
              maxLength: 255
            city:
              type: string
              maxLength: 80
            telephone:
              type: string
              maxLength: 20
    responses:
      201:
        description: Owner created successfully
      400:
        description: Validation error
    """
    try:
        owner = OwnerService.create(data)
        return handle_success(owner.to_dict(), 'Owner created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@owner_bp.route('/<int:owner_id>', methods=['PUT'])
@validate_json(OwnerUpdateSchema)
def update_owner(data, owner_id):
    """
    Update owner by ID
    ---
    tags:
      - Owners
    parameters:
      - name: owner_id
        in: path
        type: integer
        required: true
        description: Owner ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
              maxLength: 30
            last_name:
              type: string
              maxLength: 30
            address:
              type: string
              maxLength: 255
            city:
              type: string
              maxLength: 80
            telephone:
              type: string
              maxLength: 20
    responses:
      200:
        description: Owner updated successfully
      404:
        description: Owner not found
    """
    try:
        owner = OwnerService.update(owner_id, data)
        if not owner:
            return handle_not_found('Owner')
        
        return handle_success(owner.to_dict(), 'Owner updated successfully')
    except Exception as e:
        return handle_error(str(e))

@owner_bp.route('/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    """
    Delete owner by ID
    ---
    tags:
      - Owners
    parameters:
      - name: owner_id
        in: path
        type: integer
        required: true
        description: Owner ID
    responses:
      200:
        description: Owner deleted successfully
      404:
        description: Owner not found
    """
    try:
        if OwnerService.delete(owner_id):
            return handle_success(None, 'Owner deleted successfully')
        else:
            return handle_not_found('Owner')
    except Exception as e:
        return handle_error(str(e))

@owner_bp.route('/search/lastname/<string:last_name>', methods=['GET'])
def find_owners_by_lastname(last_name):
    """
    Find owners by last name
    ---
    tags:
      - Owners
    parameters:
      - name: last_name
        in: path
        type: string
        required: true
        description: Last name to search for
    responses:
      200:
        description: List of owners with matching last name
    """
    try:
        owners = OwnerService.find_by_last_name(last_name)
        return handle_success([owner.to_dict() for owner in owners])
    except Exception as e:
        return handle_error(str(e))