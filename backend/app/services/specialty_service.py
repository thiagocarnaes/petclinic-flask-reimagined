from typing import List, Optional, Dict, Any
from app.models.specialty import Specialty
from .base_service import BaseService

class SpecialtyService(BaseService):
    model = Specialty
    
    @classmethod
    def find_by_name(cls, name: str) -> Optional[Specialty]:
        """Find specialty by exact name"""
        return cls.model.query.filter_by(name=name).first()
    
    @classmethod
    def search_by_name(cls, search_term: str) -> List[Specialty]:
        """Search specialties by name"""
        return cls.model.query.filter(
            cls.model.name.ilike(f'%{search_term}%')
        ).all()
    
    @classmethod
    def get_specialties_with_vets(cls) -> List[Specialty]:
        """Get all specialties with their associated vets"""
        return cls.model.query.options(
            db.joinedload(Specialty.vets)
        ).all()