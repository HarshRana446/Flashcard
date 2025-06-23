import asyncio
from app.database import engine, Base
from app.models.flashcard import Flashcard
from app.models.user import User
from app.models.document import Document
from app.models.quiz_result import QuizResult

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Tables created successfully.")