from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from uuid import UUID
from typing import List

from src.api.controllers.document_controller import DocumentController
from src.application.dtos.document_dto import DocumentResponseDTO
from src.api.dependencies import get_document_controller

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("/{document_id}", response_model=DocumentResponseDTO)
async def get_document(
    document_id: UUID,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    Obtiene un documento por su ID
    """
    return await document_controller.get_document(document_id)

@router.post("/upload", response_model=DocumentResponseDTO)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    doc_type: str = Form(...),
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    Sube un nuevo documento
    """
    return await document_controller.upload_document(
        file=file,
        title=title,
        doc_type=doc_type
    )

@router.post("/{document_id}/analyze", response_model=DocumentResponseDTO)
async def analyze_document(
    document_id: UUID,
    document_controller: DocumentController = Depends(get_document_controller)
):
    """
    Analiza un documento existente
    """
    return await document_controller.analyze_document(document_id)