from typing import List, Optional, Dict, Any
from datetime import date
from app import db
from app.models.visit import Visit
from .base_service import BaseService

class VisitService(BaseService):
    model = Visit
    
    @classmethod
    def get_visits_by_pet(cls, pet_id: int) -> List[Visit]:
        """Get all visits for a specific pet"""
        return cls.model.query.filter_by(pet_id=pet_id).order_by(
            cls.model.visit_date.desc()
        ).all()
    
    @classmethod
    def get_visits_by_date_range(cls, start_date: date, end_date: date) -> List[Visit]:
        """Get visits within a date range"""
        return cls.model.query.filter(
            cls.model.visit_date.between(start_date, end_date)
        ).order_by(cls.model.visit_date.desc()).all()
    
    @classmethod
    def get_visits_by_date(cls, visit_date: date) -> List[Visit]:
        """Get all visits on a specific date"""
        return cls.model.query.filter_by(visit_date=visit_date).all()
    
    @classmethod
    def get_recent_visits(cls, days: int = 30) -> List[Visit]:
        """Get visits from the last N days"""
        from datetime import datetime, timedelta
        cutoff_date = date.today() - timedelta(days=days)
        return cls.model.query.filter(
            cls.model.visit_date >= cutoff_date
        ).order_by(cls.model.visit_date.desc()).all()
    
    @classmethod
    def search_visits_by_description(cls, search_term: str) -> List[Visit]:
        """Search visits by description"""
        return cls.model.query.filter(
            cls.model.description.ilike(f'%{search_term}%')
        ).order_by(cls.model.visit_date.desc()).all()