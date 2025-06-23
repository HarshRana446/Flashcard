from fastapi import FastAPI
from sqlalchemy import text
from app.routers import flashcards, upload
from app.database import engine
from app.routers import flashcard_routes, document_routes, quiz_routes

app = FastAPI()

# Include routers
app.include_router(upload.router)
app.include_router(flashcards.router)
app.include_router(flashcard_routes.router)
app.include_router(document_routes.router)
app.include_router(quiz_routes.router)


@app.get("/")
def read_root():
    return {"message": "Flashcard AI Backend Running!"}

@app.get("/test-db")
async def test_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # ✅ wrapped in text()
        return {"message": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}
