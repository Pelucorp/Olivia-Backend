from src.domain.entities.document import Document
from src.domain.entities.risk import Risk
from src.application.dtos.document_dto import DocumentDTO, DocumentResponseDTO, RiskDTO
from typing import Dict, Any
from uuid import UUID


def document_to_dto(document: Document) -> DocumentDTO:
    """
    Convierte una entidad Document a DTO.

    Args:
        document: Entidad Document

    Returns:
        DTO del documento
    """
    return DocumentDTO(
        id=document.id,
        title=document.title,
        content=document.content,
        type=document.type,
        created_at=document.created_at
    )


def document_to_response_dto(document: Document) -> DocumentResponseDTO:
    """
    Convierte una entidad Document a ResponseDTO (incluye riesgos).

    Args:
        document: Entidad Document

    Returns:
        DTO completo del documento con riesgos
    """
    return DocumentResponseDTO(
        id=document.id,
        title=document.title,
        content=document.content,
        type=document.type,
        created_at=document.created_at,
        risks=[risk_to_dto(risk) for risk in document.risks]
    )


def risk_to_dto(risk: Risk) -> RiskDTO:
    """
    Convierte una entidad Risk a DTO.

    Args:
        risk: Entidad Risk

    Returns:
        DTO del riesgo
    """
    return RiskDTO(
        id=risk.id,
        severity=risk.severity,
        description=risk.description,
        related_text=risk.related_text,
        recommendation=risk.recommendation
    )