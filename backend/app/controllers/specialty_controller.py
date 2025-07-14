from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from app.services.specialty_service import SpecialtyService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

specialty_bp = Blueprint('specialty', __name__)

class SpecialtySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))

class SpecialtyUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=80))

@specialty_bp.route('', methods=['GET'])
@validate_pagination()
def get_specialties(page, per_page):
    """
    Get all specialties with pagination
    ---
    tags:
      - Specialties
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
        description: Search term for specialty name
    responses:
      200:
        description: List of specialties
    """
    try:
        search_term = request.args.get('search')
        
        if search_term:
            specialties = SpecialtyService.search_by_name(search_term)
            return handle_success([specialty.to_dict() for specialty in specialties])
        
        result = SpecialtyService.get_all(page, per_page)
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@specialty_bp.route('/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    """
    Get specialty by ID
    ---
    tags:
      - Specialties
    parameters:
      - name: specialty_id
        in: path
        type: integer
        required: true
        description: Specialty ID
    responses:
      200:
        description: Specialty details
      404:
        description: Specialty not found
    """
    try:
        specialty = SpecialtyService.get_by_id(specialty_id)
        if not specialty:
            return handle_not_found('Specialty')
        
        return handle_success(specialty.to_dict())
    except Exception as e:
        return handle_error(str(e))

@specialty_bp.route('', methods=['POST'])
@validate_json(SpecialtySchema)
def create_specialty(data):
    """
    Create a new specialty
    ---
    tags:
      - Specialties
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              maxLength: 80
    responses:
      201:
        description: Specialty created successfully
      400:
        description: Validation error or specialty already exists
    """
    try:
        # Check if specialty already exists
        existing_specialty = SpecialtyService.find_by_name(data['name'])
        if existing_specialty:
            return jsonify({
                'error': 'Specialty already exists',
                'message': f'Specialty with name "{data["name"]}" already exists'
            }), 400
        
        specialty = SpecialtyService.create(data)
        return handle_success(specialty.to_dict(), 'Specialty created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@specialty_bp.route('/<int:specialty_id>', methods=['PUT'])
@validate_json(SpecialtyUpdateSchema)
def update_specialty(data, specialty_id):
    """
    Update specialty by ID
    ---
    tags:
      - Specialties
    parameters:
      - name: specialty_id
        in: path
        type: integer
        required: true
        description: Specialty ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              maxLength: 80
    responses:
      200:
        description: Specialty updated successfully
      404:
        description: Specialty not found
      400:
        description: Specialty name already exists
    """
    try:
        # Check if new name already exists (if name is being changed)
        if 'name' in data:
            existing_specialty = SpecialtyService.find_by_name(data['name'])
            if existing_specialty and existing_specialty.id != specialty_id:
                return jsonify({
                    'error': 'Specialty already exists',
                    'message': f'Specialty with name "{data["name"]}" already exists'
                }), 400
        
        specialty = SpecialtyService.update(specialty_id, data)
        if not specialty:
            return handle_not_found('Specialty')
        
        return handle_success(specialty.to_dict(), 'Specialty updated successfully')
    except Exception as e:
        return handle_error(str(e))

@specialty_bp.route('/<int:specialty_id>', methods=['DELETE'])
def delete_specialty(specialty_id):
    """
    Delete specialty by ID
    ---
    tags:
      - Specialties
    parameters:
      - name: specialty_id
        in: path
        type: integer
        required: true
        description: Specialty ID
    responses:
      200:
        description: Specialty deleted successfully
      404:
        description: Specialty not found
    """
    try:
        if SpecialtyService.delete(specialty_id):
            return handle_success(None, 'Specialty deleted successfully')
        else:
            return handle_not_found('Specialty')
    except Exception as e:
        return handle_error(str(e))