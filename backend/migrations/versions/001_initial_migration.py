"""Initial migration - Create all tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create pet_types table
    op.create_table('pet_types',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create owners table
    op.create_table('owners',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=30), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=80), nullable=False),
        sa.Column('telephone', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create specialties table
    op.create_table('specialties',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create vets table
    op.create_table('vets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=30), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create pets table
    op.create_table('pets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
        sa.ForeignKeyConstraint(['type_id'], ['pet_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create visits table
    op.create_table('visits',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('visit_date', sa.Date(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('pet_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create vet_specialties association table
    op.create_table('vet_specialties',
        sa.Column('vet_id', sa.Integer(), nullable=False),
        sa.Column('specialty_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['specialty_id'], ['specialties.id'], ),
        sa.ForeignKeyConstraint(['vet_id'], ['vets.id'], ),
        sa.PrimaryKeyConstraint('vet_id', 'specialty_id')
    )


def downgrade() -> None:
    op.drop_table('vet_specialties')
    op.drop_table('visits')
    op.drop_table('pets')
    op.drop_table('vets')
    op.drop_table('specialties')
    op.drop_table('owners')
    op.drop_table('pet_types')