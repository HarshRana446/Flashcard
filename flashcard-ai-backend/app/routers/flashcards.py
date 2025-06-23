from fastapi import APIRouter

router = APIRouter()

@router.get("/flashcards")
async def get_flashcards():
    return {"message": "Flashcards endpoint working!"}
