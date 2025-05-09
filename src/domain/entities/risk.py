from typing import Optional
from uuid import UUID, uuid4


class Risk:
    """Entidad para riesgos identificados en documentos."""

    def __init__(
            self,
            id: UUID,
            severity: str,
            description: str,
            related_text: Optional[str] = None,
            recommendation: Optional[str] = None
    ):
        self.id = id
        self.severity = severity
        self.description = description
        self.related_text = related_text
        self.recommendation = recommendation

    @classmethod
    def create(
            cls,
            severity: str,
            description: str,
            related_text: Optional[str] = None,
            recommendation: Optional[str] = None
    ) -> 'Risk':
        """Método de fábrica para crear un nuevo riesgo."""
        return cls(
            id=uuid4(),
            severity=severity,
            description=description,
            related_text=related_text,
            recommendation=recommendation
        )