from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_number: str
    user_input: str
    ai_response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
