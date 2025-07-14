from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from datetime import date, datetime
from app.services.pet_service import PetService
from app.services.owner_service import OwnerService
from app.services.pettype_service import PetTypeService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

pet_bp = Blueprint('pet', __name__)

class PetSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    birth_date = fields.Date(required=True)
    owner_id = fields.Int(required=True)
    type_id = fields.Int(required=True)
    
    def validate_birth_date(self, value):
        if value > date.today():
            raise ValidationError('Birth date cannot be in the future')
    
    def validate_owner_id(self, value):
        owner = OwnerService.get_by_id(value)
        if not owner:
            raise ValidationError('Owner not found')
    
    def validate_type_id(self, value):
        pet_type = PetTypeService.get_by_id(value)
        if not pet_type:
            raise ValidationError('Pet type not found')

class PetUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=30))
    birth_date = fields.Date()
    owner_id = fields.Int()
    type_id = fields.Int()
    
    def validate_birth_date(self, value):
        if value and value > date.today():
            raise ValidationError('Birth date cannot be in the future')
    
    def validate_owner_id(self, value):
        if value:
            owner = OwnerService.get_by_id(value)
            if not owner:
                raise ValidationError('Owner not found')
    
    def validate_type_id(self, value):
        if value:
            pet_type = PetTypeService.get_by_id(value)
            if not pet_type:
                raise ValidationError('Pet type not found')

@pet_bp.route('', methods=['GET'])
@validate_pagination()
def get_pets(page, per_page):
    """
    Get all pets with pagination
    ---
    tags:
      - Pets
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
      - name: owner_id
        in: query
        type: integer
        description: Filter by owner ID
      - name: type_id
        in: query
        type: integer
        description: Filter by pet type ID
      - name: name
        in: query
        type: string
        description: Search by pet name
    responses:
      200:
        description: List of pets
    """
    try:
        filters = {}
        owner_id = request.args.get('owner_id', type=int)
        type_id = request.args.get('type_id', type=int)
        name = request.args.get('name')
        
        if owner_id:
            filters['owner_id'] = owner_id
        if type_id:
            filters['type_id'] = type_id
        if name:
            filters['name'] = name
        
        if filters:
            result = PetService.search(filters, page, per_page)
        else:
            result = PetService.get_all(page, per_page)
        
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@pet_bp.route('/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """
    Get pet by ID
    ---
    tags:
      - Pets
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
        description: Pet ID
    responses:
      200:
        description: Pet details
      404:
        description: Pet not found
    """
    try:
        pet = PetService.get_pet_with_visits(pet_id)
        if not pet:
            return handle_not_found('Pet')
        
        return handle_success(pet.to_dict())
    except Exception as e:
        return handle_error(str(e))

@pet_bp.route('', methods=['POST'])
@validate_json(PetSchema)
def create_pet(data):
    """
    Create a new pet
    ---
    tags:
      - Pets
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - birth_date
            - owner_id
            - type_id
          properties:
            name:
              type: string
              maxLength: 30
            birth_date:
              type: string
              format: date
            owner_id:
              type: integer
            type_id:
              type: integer
    responses:
      201:
        description: Pet created successfully
      400:
        description: Validation error
    """
    try:
        pet = PetService.create(data)
        return handle_success(pet.to_dict(), 'Pet created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@pet_bp.route('/<int:pet_id>', methods=['PUT'])
@validate_json(PetUpdateSchema)
def update_pet(data, pet_id):
    """
    Update pet by ID
    ---
    tags:
      - Pets
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
        description: Pet ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              maxLength: 30
            birth_date:
              type: string
              format: date
            owner_id:
              type: integer
            type_id:
              type: integer
    responses:
      200:
        description: Pet updated successfully
      404:
        description: Pet not found
    """
    try:
        pet = PetService.update(pet_id, data)
        if not pet:
            return handle_not_found('Pet')
        
        return handle_success(pet.to_dict(), 'Pet updated successfully')
    except Exception as e:
        return handle_error(str(e))

@pet_bp.route('/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """
    Delete pet by ID
    ---
    tags:
      - Pets
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
        description: Pet ID
    responses:
      200:
        description: Pet deleted successfully
      404:
        description: Pet not found
    """
    try:
        if PetService.delete(pet_id):
            return handle_success(None, 'Pet deleted successfully')
        else:
            return handle_not_found('Pet')
    except Exception as e:
        return handle_error(str(e))

@pet_bp.route('/owner/<int:owner_id>', methods=['GET'])
def get_pets_by_owner(owner_id):
    """
    Get all pets by owner ID
    ---
    tags:
      - Pets
    parameters:
      - name: owner_id
        in: path
        type: integer
        required: true
        description: Owner ID
    responses:
      200:
        description: List of pets for the owner
      404:
        description: Owner not found
    """
    try:
        # Check if owner exists
        owner = OwnerService.get_by_id(owner_id)
        if not owner:
            return handle_not_found('Owner')
        
        pets = PetService.get_pets_by_owner(owner_id)
        return handle_success([pet.to_dict() for pet in pets])
    except Exception as e:
        return handle_error(str(e))