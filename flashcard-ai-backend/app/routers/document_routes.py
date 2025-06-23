from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.document import Document
from sqlalchemy.future import select
from pydantic import BaseModel

router = APIRouter(prefix="/documents", tags=["Documents"])

# Pydantic schema for creating a document
class DocumentCreate(BaseModel):
    title: str
    content: str

# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

# GET all documents
@router.get("/")
async def get_all_documents(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Document))
        documents = result.scalars().all()
        return {"documents": [
            {
                "id": str(doc.id),
                "title": doc.title,
                "content": doc.content,
                "created_at": doc.created_at
            }
            for doc in documents
        ]}
    except Exception as e:
        return {"error": str(e)}

# POST create document
@router.post("/")
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_doc = Document(
            title=document.title,
            content=document.content
        )
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)

        return {
            "message": "Document created successfully.",
            "document": {
                "id": str(new_doc.id),
                "title": new_doc.title,
                "content": new_doc.content
            }
        }
    except Exception as e:
        return {"error": str(e)}
