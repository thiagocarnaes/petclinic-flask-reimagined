from typing import List, Optional, Dict, Any
from datetime import date
from app import db
from app.models.pet import Pet
from .base_service import BaseService

class PetService(BaseService):
    model = Pet
    
    @classmethod
    def get_pets_by_owner(cls, owner_id: int) -> List[Pet]:
        """Get all pets for a specific owner"""
        return cls.model.query.filter_by(owner_id=owner_id).all()
    
    @classmethod
    def get_pets_by_type(cls, type_id: int) -> List[Pet]:
        """Get all pets of a specific type"""
        return cls.model.query.filter_by(type_id=type_id).all()
    
    @classmethod
    def get_pet_with_visits(cls, pet_id: int) -> Optional[Pet]:
        """Get pet with all visits"""
        return cls.model.query.options(
            db.joinedload(Pet.visits),
            db.joinedload(Pet.owner),
            db.joinedload(Pet.pet_type)
        ).get(pet_id)
    
    @classmethod
    def find_pets_by_name(cls, name: str) -> List[Pet]:
        """Find pets by name"""
        return cls.model.query.filter(
            cls.model.name.ilike(f'%{name}%')
        ).all()
    
    @classmethod
    def get_pets_born_after(cls, birth_date: date) -> List[Pet]:
        """Get pets born after a specific date"""
        return cls.model.query.filter(
            cls.model.birth_date > birth_date
        ).all()
    
    @classmethod
    def get_pets_born_before(cls, birth_date: date) -> List[Pet]:
        """Get pets born before a specific date"""
        return cls.model.query.filter(
            cls.model.birth_date < birth_date
        ).all()