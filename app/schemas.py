from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class QuestionRequest(BaseModel):
    """Request model for getting random questions"""
    use: str = Field(..., description="Test type (e.g., 'Positioning test')")
    subjects: List[str] = Field(..., description="List of subjects to filter by")
    limit: int = Field(..., description="Number of questions (5, 10, or 20)")
    
    @field_validator('limit')
    @classmethod
    def validate_limit(cls, v):
        """Ensure limit is 5, 10, or 20"""
        if v not in [5, 10, 20]:
            raise ValueError('Limit must be 5, 10, or 20')
        return v

class QuestionResponse(BaseModel):
    """Response model for a single question (without correct answer)"""
    id: int
    question: str
    subject: str
    responses: Dict[str, Optional[str]]
    
    class Config:
        from_attributes = True

class QuestionsListResponse(BaseModel):
    """Response model for list of questions"""
    questions: List[QuestionResponse]
    total_returned: int

class CreateQuestionRequest(BaseModel):
    """Request model for creating a new question"""
    question: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    use: str = Field(..., min_length=1)
    correct: str = Field(..., pattern="^[A-D]$", description="Correct answer: A, B, C, or D")
    responseA: str = Field(..., min_length=1)
    responseB: Optional[str] = None
    responseC: Optional[str] = None
    responseD: Optional[str] = None
    
    @field_validator('correct')
    @classmethod
    def validate_correct(cls, v):
        """Ensure correct answer is A, B, C, or D"""
        if v not in ['A', 'B', 'C', 'D']:
            raise ValueError('Correct answer must be A, B, C, or D')
        return v

class CreateQuestionResponse(BaseModel):
    """Response model for created question"""
    id: int
    message: str

class StatusResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str