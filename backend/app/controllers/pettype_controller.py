from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from app.services.pettype_service import PetTypeService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

pettype_bp = Blueprint('pettype', __name__)

class PetTypeSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))

class PetTypeUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=80))

@pettype_bp.route('', methods=['GET'])
@validate_pagination()
def get_pet_types(page, per_page):
    """
    Get all pet types with pagination
    ---
    tags:
      - Pet Types
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
        description: Search term for pet type name
    responses:
      200:
        description: List of pet types
    """
    try:
        search_term = request.args.get('search')
        
        if search_term:
            pet_types = PetTypeService.search_by_name(search_term)
            return handle_success([pet_type.to_dict() for pet_type in pet_types])
        
        result = PetTypeService.get_all(page, per_page)
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@pettype_bp.route('/<int:pet_type_id>', methods=['GET'])
def get_pet_type(pet_type_id):
    """
    Get pet type by ID
    ---
    tags:
      - Pet Types
    parameters:
      - name: pet_type_id
        in: path
        type: integer
        required: true
        description: Pet Type ID
    responses:
      200:
        description: Pet type details
      404:
        description: Pet type not found
    """
    try:
        pet_type = PetTypeService.get_by_id(pet_type_id)
        if not pet_type:
            return handle_not_found('Pet Type')
        
        return handle_success(pet_type.to_dict())
    except Exception as e:
        return handle_error(str(e))

@pettype_bp.route('', methods=['POST'])
@validate_json(PetTypeSchema)
def create_pet_type(data):
    """
    Create a new pet type
    ---
    tags:
      - Pet Types
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
        description: Pet type created successfully
      400:
        description: Validation error or pet type already exists
    """
    try:
        # Check if pet type already exists
        existing_pet_type = PetTypeService.find_by_name(data['name'])
        if existing_pet_type:
            return jsonify({
                'error': 'Pet type already exists',
                'message': f'Pet type with name "{data["name"]}" already exists'
            }), 400
        
        pet_type = PetTypeService.create(data)
        return handle_success(pet_type.to_dict(), 'Pet type created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@pettype_bp.route('/<int:pet_type_id>', methods=['PUT'])
@validate_json(PetTypeUpdateSchema)
def update_pet_type(data, pet_type_id):
    """
    Update pet type by ID
    ---
    tags:
      - Pet Types
    parameters:
      - name: pet_type_id
        in: path
        type: integer
        required: true
        description: Pet Type ID
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
        description: Pet type updated successfully
      404:
        description: Pet type not found
      400:
        description: Pet type name already exists
    """
    try:
        # Check if new name already exists (if name is being changed)
        if 'name' in data:
            existing_pet_type = PetTypeService.find_by_name(data['name'])
            if existing_pet_type and existing_pet_type.id != pet_type_id:
                return jsonify({
                    'error': 'Pet type already exists',
                    'message': f'Pet type with name "{data["name"]}" already exists'
                }), 400
        
        pet_type = PetTypeService.update(pet_type_id, data)
        if not pet_type:
            return handle_not_found('Pet Type')
        
        return handle_success(pet_type.to_dict(), 'Pet type updated successfully')
    except Exception as e:
        return handle_error(str(e))

@pettype_bp.route('/<int:pet_type_id>', methods=['DELETE'])
def delete_pet_type(pet_type_id):
    """
    Delete pet type by ID
    ---
    tags:
      - Pet Types
    parameters:
      - name: pet_type_id
        in: path
        type: integer
        required: true
        description: Pet Type ID
    responses:
      200:
        description: Pet type deleted successfully
      404:
        description: Pet type not found
      400:
        description: Cannot delete pet type with associated pets
    """
    try:
        # Check if pet type has associated pets
        pet_type = PetTypeService.get_by_id(pet_type_id)
        if not pet_type:
            return handle_not_found('Pet Type')
        
        if pet_type.pets:
            return jsonify({
                'error': 'Cannot delete pet type',
                'message': 'Pet type has associated pets and cannot be deleted'
            }), 400
        
        if PetTypeService.delete(pet_type_id):
            return handle_success(None, 'Pet type deleted successfully')
        else:
            return handle_not_found('Pet Type')
    except Exception as e:
        return handle_error(str(e))