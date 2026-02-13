from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models import Question
from app.schemas import (
    QuestionRequest, 
    QuestionResponse, 
    QuestionsListResponse,
    CreateQuestionRequest,
    CreateQuestionResponse,
    StatusResponse
)
from app.auth import verify_user, verify_admin
from fastapi.security import HTTPBasicCredentials

# Create FastAPI app
app = FastAPI(
    title="Questionnaire API",
    description="API for managing and retrieving multiple choice questions",
    version="1.0.0"
)

@app.get("/", response_model=StatusResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is functional.
    No authentication required.
    """
    return {
        "status": "ok",
        "message": "Questionnaire API is running"
    }

@app.post("/questions/random", response_model=QuestionsListResponse, tags=["Questions"])
def get_random_questions(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    username: str = Depends(verify_user)
):
    """
    Get random questions based on test type (use) and subjects.
    
    Requires user authentication.
    
    - **use**: Test type (e.g., "Positioning test")
    - **subjects**: List of subjects to filter by (e.g., ["Databases", "Programming"])
    - **limit**: Number of questions to return (must be 5, 10, or 20)
    
    Returns different random questions each time with the same parameters.
    Note: The correct answer is NOT included in the response.
    """
    
    # Query database with filters
    query = db.query(Question).filter(
        Question.use == request.use,
        Question.subject.in_(request.subjects)
    )
    
    # Get all matching questions
    all_questions = query.all()
    
    # Check if we have enough questions
    if len(all_questions) < request.limit:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough questions found. Only {len(all_questions)} available, but {request.limit} requested."
        )
    
    # Select random questions
    random_questions = random.sample(all_questions, request.limit)
    
    # Format response (without correct answer)
    questions_response = []
    for q in random_questions:
        questions_response.append({
            "id": q.id,
            "question": q.question,
            "subject": q.subject,
            "responses": {
                "A": q.responseA if q.responseA else None,
                "B": q.responseB if q.responseB else None,
                "C": q.responseC if q.responseC else None,
                "D": q.responseD if q.responseD else None
            }
        })
    
    return {
        "questions": questions_response,
        "total_returned": len(questions_response)
    }

@app.post("/questions", response_model=CreateQuestionResponse, tags=["Admin"])
def create_question(
    request: CreateQuestionRequest,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(verify_admin)
):
    """
    Create a new question in the database.
    
    Requires admin authentication (password: 4dm1N).
    
    - **question**: The question text
    - **subject**: Subject/category
    - **use**: Test type
    - **correct**: Correct answer (A, B, C, or D)
    - **responseA**: Answer option A (required)
    - **responseB**: Answer option B (optional)
    - **responseC**: Answer option C (optional)
    - **responseD**: Answer option D (optional)
    """
    
    # Create new question
    new_question = Question(
        question=request.question,
        subject=request.subject,
        use=request.use,
        correct=request.correct,
        responseA=request.responseA,
        responseB=request.responseB or '',
        responseC=request.responseC or '',
        responseD=request.responseD or ''
    )
    
    # Add to database
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return {
        "id": new_question.id,
        "message": "Question created successfully"
    }

@app.get("/status", response_model=StatusResponse, tags=["Health"])
def status_check():
    """
    Alternative health check endpoint.
    No authentication required.
    """
    return {
        "status": "ok",
        "message": "Questionnaire API is running"
    }

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return HTTPException(status_code=400, detail=str(exc))