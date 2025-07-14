from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from app.services.vet_service import VetService
from app.services.specialty_service import SpecialtyService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

vet_bp = Blueprint('vet', __name__)

class VetSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))

class VetUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=30))
    last_name = fields.Str(validate=validate.Length(min=1, max=30))

class VetSpecialtySchema(Schema):
    specialty_id = fields.Int(required=True)
    
    def validate_specialty_id(self, value):
        specialty = SpecialtyService.get_by_id(value)
        if not specialty:
            raise ValidationError('Specialty not found')

@vet_bp.route('', methods=['GET'])
@validate_pagination()
def get_vets(page, per_page):
    """
    Get all vets with pagination
    ---
    tags:
      - Vets
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
        description: Search term for first or last name
      - name: specialty
        in: query
        type: string
        description: Filter by specialty name
    responses:
      200:
        description: List of vets
    """
    try:
        search_term = request.args.get('search')
        specialty = request.args.get('specialty')
        
        if search_term:
            vets = VetService.find_vets_by_name(search_term)
            return handle_success([vet.to_dict() for vet in vets])
        
        if specialty:
            vets = VetService.find_vets_by_specialty(specialty)
            return handle_success([vet.to_dict() for vet in vets])
        
        result = VetService.get_all(page, per_page)
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('/<int:vet_id>', methods=['GET'])
def get_vet(vet_id):
    """
    Get vet by ID with specialties
    ---
    tags:
      - Vets
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: Vet ID
    responses:
      200:
        description: Vet details with specialties
      404:
        description: Vet not found
    """
    try:
        vet = VetService.get_vet_with_specialties(vet_id)
        if not vet:
            return handle_not_found('Vet')
        
        return handle_success(vet.to_dict())
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('', methods=['POST'])
@validate_json(VetSchema)
def create_vet(data):
    """
    Create a new vet
    ---
    tags:
      - Vets
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
          properties:
            first_name:
              type: string
              maxLength: 30
            last_name:
              type: string
              maxLength: 30
    responses:
      201:
        description: Vet created successfully
      400:
        description: Validation error
    """
    try:
        vet = VetService.create(data)
        return handle_success(vet.to_dict(), 'Vet created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('/<int:vet_id>', methods=['PUT'])
@validate_json(VetUpdateSchema)
def update_vet(data, vet_id):
    """
    Update vet by ID
    ---
    tags:
      - Vets
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: Vet ID
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
    responses:
      200:
        description: Vet updated successfully
      404:
        description: Vet not found
    """
    try:
        vet = VetService.update(vet_id, data)
        if not vet:
            return handle_not_found('Vet')
        
        return handle_success(vet.to_dict(), 'Vet updated successfully')
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('/<int:vet_id>', methods=['DELETE'])
def delete_vet(vet_id):
    """
    Delete vet by ID
    ---
    tags:
      - Vets
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: Vet ID
    responses:
      200:
        description: Vet deleted successfully
      404:
        description: Vet not found
    """
    try:
        if VetService.delete(vet_id):
            return handle_success(None, 'Vet deleted successfully')
        else:
            return handle_not_found('Vet')
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('/<int:vet_id>/specialties', methods=['POST'])
@validate_json(VetSpecialtySchema)
def add_specialty_to_vet(data, vet_id):
    """
    Add specialty to vet
    ---
    tags:
      - Vets
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: Vet ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - specialty_id
          properties:
            specialty_id:
              type: integer
    responses:
      200:
        description: Specialty added to vet successfully
      404:
        description: Vet or specialty not found
    """
    try:
        vet = VetService.add_specialty_to_vet(vet_id, data['specialty_id'])
        if not vet:
            return handle_not_found('Vet or Specialty')
        
        return handle_success(vet.to_dict(), 'Specialty added to vet successfully')
    except Exception as e:
        return handle_error(str(e))

@vet_bp.route('/<int:vet_id>/specialties/<int:specialty_id>', methods=['DELETE'])
def remove_specialty_from_vet(vet_id, specialty_id):
    """
    Remove specialty from vet
    ---
    tags:
      - Vets
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: Vet ID
      - name: specialty_id
        in: path
        type: integer
        required: true
        description: Specialty ID
    responses:
      200:
        description: Specialty removed from vet successfully
      404:
        description: Vet or specialty not found
    """
    try:
        vet = VetService.remove_specialty_from_vet(vet_id, specialty_id)
        if not vet:
            return handle_not_found('Vet or Specialty')
        
        return handle_success(vet.to_dict(), 'Specialty removed from vet successfully')
    except Exception as e:
        return handle_error(str(e))