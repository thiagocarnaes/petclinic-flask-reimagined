from typing import List, Optional, Dict, Any
from app.models.owner import Owner
from .base_service import BaseService

class OwnerService(BaseService):
    model = Owner
    
    @classmethod
    def find_by_last_name(cls, last_name: str) -> List[Owner]:
        """Find owners by last name"""
        return cls.model.query.filter(
            cls.model.last_name.ilike(f'%{last_name}%')
        ).all()
    
    @classmethod
    def get_owner_with_pets(cls, owner_id: int) -> Optional[Owner]:
        """Get owner with all their pets"""
        return cls.model.query.options(
            db.joinedload(Owner.pets)
        ).get(owner_id)
    
    @classmethod
    def search_owners(cls, search_term: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Search owners by name, address, city, or telephone"""
        query = cls.model.query.filter(
            db.or_(
                cls.model.first_name.ilike(f'%{search_term}%'),
                cls.model.last_name.ilike(f'%{search_term}%'),
                cls.model.address.ilike(f'%{search_term}%'),
                cls.model.city.ilike(f'%{search_term}%'),
                cls.model.telephone.ilike(f'%{search_term}%')
            )
        )
        
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'data': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }