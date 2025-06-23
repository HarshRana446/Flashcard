from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.flashcard import Flashcard
from sqlalchemy.future import select

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@router.get("/")
async def get_all_flashcards(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Flashcard))
        flashcards = result.scalars().all()
        return {"flashcards": [ 
            {
                "id": str(card.id),
                "question": card.question,
                "answer": card.answer,
                "source_document": card.source_document
            }
            for card in flashcards
        ]}
    except Exception as e:
        return {"error": str(e)}
