from typing import List, Optional, Dict, Any
from app import db

class BaseService:
    model = None
    
    @classmethod
    def get_all(cls, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get all records with pagination"""
        pagination = cls.model.query.paginate(
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
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional[object]:
        """Get a record by ID"""
        return cls.model.query.get(id)
    
    @classmethod
    def create(cls, data: Dict[str, Any]) -> object:
        """Create a new record"""
        instance = cls.model(**data)
        return instance.save()
    
    @classmethod
    def update(cls, id: int, data: Dict[str, Any]) -> Optional[object]:
        """Update a record by ID"""
        instance = cls.get_by_id(id)
        if instance:
            return instance.update(**data)
        return None
    
    @classmethod
    def delete(cls, id: int) -> bool:
        """Delete a record by ID"""
        instance = cls.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
    
    @classmethod
    def search(cls, filters: Dict[str, Any], page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Search records with filters"""
        query = cls.model.query
        
        for key, value in filters.items():
            if hasattr(cls.model, key) and value is not None:
                if isinstance(value, str):
                    query = query.filter(getattr(cls.model, key).ilike(f'%{value}%'))
                else:
                    query = query.filter(getattr(cls.model, key) == value)
        
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