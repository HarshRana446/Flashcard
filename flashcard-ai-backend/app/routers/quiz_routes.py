from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.quiz_result import QuizResult
from sqlalchemy.future import select
import uuid

router = APIRouter(prefix="/quiz-results", tags=["Quiz Results"])

def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuizResultCreate(BaseModel):
    user_id: str
    document_id: str
    total_questions: int
    correct_answers: int

@router.post("/")
async def create_quiz_result(result: QuizResultCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_result = QuizResult(
            user_id=uuid.UUID(result.user_id),
            document_id=uuid.UUID(result.document_id),
            total_questions=result.total_questions,
            correct_answers=result.correct_answers
        )
        db.add(new_result)
        await db.commit()
        await db.refresh(new_result)

        return {
            "message": "Quiz result saved.",
            "quiz_result_id": str(new_result.id)
        }
    except Exception as e:
        return {"error": str(e)}
@router.get("/")
async def get_all_quiz_results(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(QuizResult))
        quiz_results = result.scalars().all()
        return {
            "quiz_results": [
                {
                    "id": str(q.id),
                    "user_id": str(q.user_id),
                    "document_id": str(q.document_id),
                    "total_questions": q.total_questions,
                    "correct_answers": q.correct_answers,
                    "created_at": q.created_at
                }
                for q in quiz_results
            ]
        }
    except Exception as e:
        return {"error": str(e)}
