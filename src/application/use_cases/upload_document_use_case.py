from fastapi import UploadFile
import uuid
from datetime import datetime

from src.domain.repositories.document_repository import DocumentRepository
from src.domain.entities.document import Document
from src.application.dtos.document_dto import DocumentResponseDTO
from src.infrastructure.mappers.document_mapper import document_to_response_dto


class UploadDocumentUseCase:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def execute(
            self,
            file: UploadFile,
            title: str,
            doc_type: str
    ) -> DocumentResponseDTO:
        """
        Sube y procesa un nuevo documento

        Args:
            file: Archivo a procesar
            title: Título del documento
            doc_type: Tipo de documento

        Returns:
            DTO del documento creado
        """
        # Leer contenido del archivo
        content = await file.read()

        # En una implementación real, aquí procesaríamos el PDF para extraer texto
        # Por simplificación, usamos el contenido binario como texto
        text_content = content.decode('utf-8', errors='ignore')

        # Crear entidad de documento
        document = Document(
            id=uuid.uuid4(),
            title=title,
            content=text_content[:5000],  # Limitar el contenido para este ejemplo
            type=doc_type,
            created_at=datetime.now(),
            risks=[]
        )

        # Persistir documento
        saved_document = await self.document_repository.save(document)

        # Mapear y retornar DTO
        return document_to_response_dto(saved_document)