from datetime import date
from app import db
from .base import BaseModel

class Pet(BaseModel):
    __tablename__ = 'pets'
    
    name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    
    # Foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('pet_types.id'), nullable=False)
    
    # Relationship with visits
    visits = db.relationship('Visit', backref='pet', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Pet {self.name}>'
    
    def age(self):
        """Calculate pet's age in years"""
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def to_dict(self):
        data = super().to_dict()
        data['age'] = self.age()
        data['owner'] = {
            'id': self.owner.id,
            'full_name': self.owner.full_name()
        } if self.owner else None
        data['type'] = {
            'id': self.pet_type.id,
            'name': self.pet_type.name
        } if self.pet_type else None
        data['visits'] = [visit.to_dict() for visit in self.visits]
        return data