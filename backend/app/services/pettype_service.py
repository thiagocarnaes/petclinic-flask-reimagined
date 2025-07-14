from typing import List, Optional, Dict, Any
from app.models.pettype import PetType
from .base_service import BaseService

class PetTypeService(BaseService):
    model = PetType
    
    @classmethod
    def find_by_name(cls, name: str) -> Optional[PetType]:
        """Find pet type by exact name"""
        return cls.model.query.filter_by(name=name).first()
    
    @classmethod
    def search_by_name(cls, search_term: str) -> List[PetType]:
        """Search pet types by name"""
        return cls.model.query.filter(
            cls.model.name.ilike(f'%{search_term}%')
        ).all()
    
    @classmethod
    def get_pet_types_with_pets(cls) -> List[PetType]:
        """Get all pet types with their associated pets"""
        return cls.model.query.options(
            db.joinedload(PetType.pets)
        ).all()