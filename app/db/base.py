"""
Database base class for all SQLAlchemy models.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base class that all models will inherit from
Base = declarative_base()
