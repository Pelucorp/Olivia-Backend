from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from src.domain.entities.risk import Risk


class Document:
    """Entidad principal para documentos legales."""

    def __init__(
            self,
            id: UUID,
            title: str,
            content: str,
            type: str,
            created_at: datetime = None,
            risks: List[Risk] = None
    ):
        self.id = id
        self.title = title
        self.content = content
        self.type = type
        self.created_at = created_at if created_at else datetime.now()
        self.risks = risks if risks else []

    def add_risk(self, risk: Risk) -> None:
        """Añade un riesgo al documento."""
        self.risks.append(risk)

    def has_high_risks(self) -> bool:
        """Verifica si el documento tiene riesgos altos."""
        return any(risk.severity == "high" for risk in self.risks)

    def get_text_excerpt(self, max_length: int = 200) -> str:
        """Retorna un extracto del contenido del documento."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."

    @classmethod
    def create(cls, title: str, content: str, type: str) -> 'Document':
        """Método de fábrica para crear un nuevo documento."""
        return cls(
            id=uuid4(),
            title=title,
            content=content,
            type=type
        )