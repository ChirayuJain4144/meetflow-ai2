import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.database import SessionLocal, Base, engine
import app.models
from app.services.seed_service import seed_demo_data

def main():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding sample demo data (Meeting 1 & Meeting 2 with conflict)...")
        result = seed_demo_data(db, force_reset=True)
        print(f"Result: {result}")
        print("Demo data loaded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
