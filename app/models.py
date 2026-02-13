from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Question(Base):
    """
    Database model for questions.
    Matches the structure of the Excel file.
    """
    __tablename__ = "questions"
    
    # Primary key (unique ID for each question)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Question text
    question = Column(Text, nullable=False)
    
    # Category/Subject (e.g., "Databases")
    subject = Column(String(100), nullable=False, index=True)
    
    # Test type (e.g., "Positioning test")
    use = Column(String(100), nullable=False, index=True)
    
    # Correct answer (A, B, C, or D)
    correct = Column(String(1), nullable=False)
    
    # Answer options
    responseA = Column(Text, nullable=False)
    responseB = Column(Text, nullable=True)
    responseC = Column(Text, nullable=True)
    responseD = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Question(id={self.id}, subject={self.subject})>"