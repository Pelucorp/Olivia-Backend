from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class RiskDTO(BaseModel):
    id: UUID
    severity: str
    description: str
    related_text: Optional[str] = None
    recommendation: Optional[str] = None

    class Config:
        orm_mode = True


class DocumentDTO(BaseModel):
    id: UUID
    title: str
    content: str
    type: str
    created_at: datetime

    class Config:
        orm_mode = True


class DocumentResponseDTO(DocumentDTO):
    risks: Optional[List[RiskDTO]] = Field(default_factory=list)