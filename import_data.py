import pandas as pd
from app.database import SessionLocal
from app.models import Question

def clean_value(value):
    """Convert any value to a clean string"""
    if pd.isna(value):
        return ''
    return str(value).strip()

def import_questions():
    """Import questions from Excel file into database"""
    
    # Read Excel file
    print("📖 Reading Excel file...")
    df = pd.read_excel('data/questions_en.xlsx')
    
    print(f"📊 Found {len(df)} questions in Excel file")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing questions (optional - for fresh import)
        db.query(Question).delete()
        
        # Import each row
        imported = 0
        for index, row in df.iterrows():
            question = Question(
                question=clean_value(row['question']),
                subject=clean_value(row['subject']),
                use=clean_value(row['use']),
                correct=clean_value(row['correct']),
                responseA=clean_value(row['responseA']),
                responseB=clean_value(row['responseB']),
                responseC=clean_value(row['responseC']),
                responseD=clean_value(row['responseD'])
            )
            db.add(question)
            imported += 1
        
        # Commit all changes
        db.commit()
        print(f"✅ Successfully imported {imported} questions!")
        
        # Show some statistics
        print("\n📈 Statistics:")
        subjects = db.query(Question.subject).distinct().all()
        print(f"   Subjects: {', '.join([s[0] for s in subjects])}")
        
        uses = db.query(Question.use).distinct().all()
        print(f"   Test types: {', '.join([u[0] for u in uses])}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    import_questions()