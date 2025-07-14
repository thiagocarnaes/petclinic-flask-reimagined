from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import Schema, fields, validate, ValidationError
from datetime import date, datetime
from app.services.visit_service import VisitService
from app.services.pet_service import PetService
from .base_controller import validate_json, validate_pagination, handle_not_found, handle_success, handle_error

visit_bp = Blueprint('visit', __name__)

class VisitSchema(Schema):
    visit_date = fields.Date(required=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    pet_id = fields.Int(required=True)
    
    def validate_visit_date(self, value):
        if value > date.today():
            raise ValidationError('Visit date cannot be in the future')
    
    def validate_pet_id(self, value):
        pet = PetService.get_by_id(value)
        if not pet:
            raise ValidationError('Pet not found')

class VisitUpdateSchema(Schema):
    visit_date = fields.Date()
    description = fields.Str(validate=validate.Length(min=1, max=1000))
    pet_id = fields.Int()
    
    def validate_visit_date(self, value):
        if value and value > date.today():
            raise ValidationError('Visit date cannot be in the future')
    
    def validate_pet_id(self, value):
        if value:
            pet = PetService.get_by_id(value)
            if not pet:
                raise ValidationError('Pet not found')

@visit_bp.route('', methods=['GET'])
@validate_pagination()
def get_visits(page, per_page):
    """
    Get all visits with pagination
    ---
    tags:
      - Visits
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
      - name: pet_id
        in: query
        type: integer
        description: Filter by pet ID
      - name: start_date
        in: query
        type: string
        format: date
        description: Start date for date range filter
      - name: end_date
        in: query
        type: string
        format: date
        description: End date for date range filter
      - name: description
        in: query
        type: string
        description: Search in visit description
    responses:
      200:
        description: List of visits
    """
    try:
        pet_id = request.args.get('pet_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        description = request.args.get('description')
        
        if pet_id:
            visits = VisitService.get_visits_by_pet(pet_id)
            return handle_success([visit.to_dict() for visit in visits])
        
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                visits = VisitService.get_visits_by_date_range(start, end)
                return handle_success([visit.to_dict() for visit in visits])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if description:
            visits = VisitService.search_visits_by_description(description)
            return handle_success([visit.to_dict() for visit in visits])
        
        result = VisitService.get_all(page, per_page)
        return handle_success(result)
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    """
    Get visit by ID
    ---
    tags:
      - Visits
    parameters:
      - name: visit_id
        in: path
        type: integer
        required: true
        description: Visit ID
    responses:
      200:
        description: Visit details
      404:
        description: Visit not found
    """
    try:
        visit = VisitService.get_by_id(visit_id)
        if not visit:
            return handle_not_found('Visit')
        
        return handle_success(visit.to_dict())
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('', methods=['POST'])
@validate_json(VisitSchema)
def create_visit(data):
    """
    Create a new visit
    ---
    tags:
      - Visits
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - visit_date
            - description
            - pet_id
          properties:
            visit_date:
              type: string
              format: date
            description:
              type: string
              maxLength: 1000
            pet_id:
              type: integer
    responses:
      201:
        description: Visit created successfully
      400:
        description: Validation error
    """
    try:
        visit = VisitService.create(data)
        return handle_success(visit.to_dict(), 'Visit created successfully', 201)
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('/<int:visit_id>', methods=['PUT'])
@validate_json(VisitUpdateSchema)
def update_visit(data, visit_id):
    """
    Update visit by ID
    ---
    tags:
      - Visits
    parameters:
      - name: visit_id
        in: path
        type: integer
        required: true
        description: Visit ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            visit_date:
              type: string
              format: date
            description:
              type: string
              maxLength: 1000
            pet_id:
              type: integer
    responses:
      200:
        description: Visit updated successfully
      404:
        description: Visit not found
    """
    try:
        visit = VisitService.update(visit_id, data)
        if not visit:
            return handle_not_found('Visit')
        
        return handle_success(visit.to_dict(), 'Visit updated successfully')
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('/<int:visit_id>', methods=['DELETE'])
def delete_visit(visit_id):
    """
    Delete visit by ID
    ---
    tags:
      - Visits
    parameters:
      - name: visit_id
        in: path
        type: integer
        required: true
        description: Visit ID
    responses:
      200:
        description: Visit deleted successfully
      404:
        description: Visit not found
    """
    try:
        if VisitService.delete(visit_id):
            return handle_success(None, 'Visit deleted successfully')
        else:
            return handle_not_found('Visit')
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('/pet/<int:pet_id>', methods=['GET'])
def get_visits_by_pet(pet_id):
    """
    Get all visits by pet ID
    ---
    tags:
      - Visits
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
        description: Pet ID
    responses:
      200:
        description: List of visits for the pet
      404:
        description: Pet not found
    """
    try:
        # Check if pet exists
        pet = PetService.get_by_id(pet_id)
        if not pet:
            return handle_not_found('Pet')
        
        visits = VisitService.get_visits_by_pet(pet_id)
        return handle_success([visit.to_dict() for visit in visits])
    except Exception as e:
        return handle_error(str(e))

@visit_bp.route('/recent', methods=['GET'])
def get_recent_visits():
    """
    Get recent visits (last 30 days)
    ---
    tags:
      - Visits
    parameters:
      - name: days
        in: query
        type: integer
        default: 30
        description: Number of days to look back
    responses:
      200:
        description: List of recent visits
    """
    try:
        days = request.args.get('days', 30, type=int)
        if days < 1 or days > 365:
            return jsonify({'error': 'Days must be between 1 and 365'}), 400
        
        visits = VisitService.get_recent_visits(days)
        return handle_success([visit.to_dict() for visit in visits])
    except Exception as e:
        return handle_error(str(e))