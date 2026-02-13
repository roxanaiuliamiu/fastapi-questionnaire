# fastapi-questionnaire
For this evaluation, we will put ourselves in the shoes of a company that creates questionnaires via a smartphone or web browser application. To simplify the architecture of these different products, the company wants to set up an API. The purpose of this API is to query a database to return a series of questions.

#Requirements:
Python 3.12 plus
Uvicorn
pip
virtual env

Steps:
-created the repository and cloned it
-created the virtual environment
-installed dependencies 
-set up the database
-run the server

## Features

- **Random Question Retrieval** - Get random questions filtered by subject and test type
- **User Authentication** - Basic HTTP authentication for regular users
- **Admin Authentification** - Separate admin authentication for question creation
- **Input Validation** - Strict validation for request parameters
- **SQLite Database** - Lightweight database with 76+ questions
- **Interactive Documentation** - Auto-generated Swagger UI
- **Error Handling** - Clear error messages for invalid requests

API Endpoints

1. Health Check
Endpoint: GET /
Authentication: None required
Description: Verify the API is running.

2. Get Random Questions
Endpoint: POST /questions/random
Authentication: User credentials required
Description: Retrieve random questions filtered by test type and subjects.

User Credentials
Regular users can access the /questions/random endpoint:

Username	Password
alice	wonderland
bob	builder
clementine	mandarine
Admin Credentials
Admin can access the /questions endpoint:


3. Create Question (Admin Only)
Endpoint: POST /questions
Authentication: Admin password required
Description: Add a new question to the database.

Username	Password
admin	4dm1N

Interactive Documentation

FastAPI automatically generates interactive API documentation:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

Error handling

Invalid Credentials (401)
Invalid Limit (422)
Not Enough Questions (400)

Database Schema
The questions table has the following structure:

Column	Type	Description
id          Integer	    Primary key (auto-increment)
question    Text	    The question text
subject     String	    Subject/category
use 	    String	    Test type
correct	    String	    Correct answer (A, B, C, or D)
responseA	Text	    Answer option A
responseB	Text	    Answer option B (optional)
responseC	Text	    Answer option C (optional)
responseD	Text	    Answer option D (optional)

Technologies Used
FastAPI - Modern Python web framework
SQLAlchemy - SQL toolkit and ORM
Pydantic - Data validation using Python type annotations
Uvicorn - ASGI server
Pandas - Data manipulation for Excel import
SQLite - Lightweight database










