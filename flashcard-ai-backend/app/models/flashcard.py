from sqlalchemy import Column, Integer, String
from app.database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    source_document = Column(String, nullable=True)
