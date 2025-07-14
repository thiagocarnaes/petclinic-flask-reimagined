from typing import List, Optional, Dict, Any
from app import db
from app.models.vet import Vet
from app.models.specialty import Specialty
from .base_service import BaseService

class VetService(BaseService):
    model = Vet
    
    @classmethod
    def get_vets_with_specialties(cls) -> List[Vet]:
        """Get all vets with their specialties"""
        return cls.model.query.options(
            db.joinedload(Vet.specialties)
        ).all()
    
    @classmethod
    def get_vet_with_specialties(cls, vet_id: int) -> Optional[Vet]:
        """Get a specific vet with specialties"""
        return cls.model.query.options(
            db.joinedload(Vet.specialties)
        ).get(vet_id)
    
    @classmethod
    def find_vets_by_specialty(cls, specialty_name: str) -> List[Vet]:
        """Find vets by specialty name"""
        return cls.model.query.join(Vet.specialties).filter(
            Specialty.name.ilike(f'%{specialty_name}%')
        ).all()
    
    @classmethod
    def find_vets_by_name(cls, search_term: str) -> List[Vet]:
        """Find vets by first or last name"""
        return cls.model.query.filter(
            db.or_(
                cls.model.first_name.ilike(f'%{search_term}%'),
                cls.model.last_name.ilike(f'%{search_term}%')
            )
        ).all()
    
    @classmethod
    def add_specialty_to_vet(cls, vet_id: int, specialty_id: int) -> Optional[Vet]:
        """Add a specialty to a vet"""
        vet = cls.get_by_id(vet_id)
        specialty = Specialty.query.get(specialty_id)
        
        if vet and specialty and specialty not in vet.specialties:
            vet.specialties.append(specialty)
            db.session.commit()
            return vet
        return None
    
    @classmethod
    def remove_specialty_from_vet(cls, vet_id: int, specialty_id: int) -> Optional[Vet]:
        """Remove a specialty from a vet"""
        vet = cls.get_by_id(vet_id)
        specialty = Specialty.query.get(specialty_id)
        
        if vet and specialty and specialty in vet.specialties:
            vet.specialties.remove(specialty)
            db.session.commit()
            return vet
        return None