from app import db
from .base import BaseModel

class Visit(BaseModel):
    __tablename__ = 'visits'
    
    visit_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Foreign key
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    
    def __repr__(self):
        return f'<Visit {self.visit_date} - Pet {self.pet_id}>'
    
    def to_dict(self):
        data = super().to_dict()
        data['pet'] = {
            'id': self.pet.id,
            'name': self.pet.name,
            'owner': self.pet.owner.full_name()
        } if self.pet else None
        return data