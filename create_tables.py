from app.database import engine, Base
from app.models import Question

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("📁 Database file: questionnaire.db")

if __name__ == "__main__":
    create_tables()