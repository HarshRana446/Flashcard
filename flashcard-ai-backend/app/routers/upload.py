from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.flashcard import Flashcard
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

router = APIRouter(prefix="/upload", tags=["Upload"])

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@router.post("/text")
async def upload_text(content: str, db: AsyncSession = Depends(get_db)):
    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not loaded.")

    client = AsyncOpenAI(api_key=openai_key)

    try:
        # Prompt to generate flashcards in JSON format
        prompt = f"""
        Convert the following study notes into 3 JSON flashcards in this format:
        [{{"question": "...", "answer": "..."}}]

        Notes:
        {content}
        """

        # OpenAI Chat Completion request
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )

        # Extract and safely parse the JSON response
        raw_output = response.choices[0].message.content.strip()
        flashcards_data = json.loads(raw_output)

        saved_cards = []

        for card in flashcards_data:
            new_flashcard = Flashcard(
                question=card["question"],
                answer=card["answer"]
            )
            db.add(new_flashcard)
            saved_cards.append(card)

        await db.commit()

        return {
            "message": "Flashcards generated and saved!",
            "flashcards": saved_cards
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
