import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database.database import engine
from app.database.models import Base

# This will create all tables defined in models.py
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")