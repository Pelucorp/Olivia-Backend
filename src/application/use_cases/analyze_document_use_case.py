from uuid import UUID

from src.domain.repositories.document_repository import DocumentRepository
from src.domain.services.document_analyzer_service import DocumentAnalyzerService
from src.application.dtos.document_dto import DocumentResponseDTO
from src.infrastructure.mappers.document_mapper import document_to_response_dto


class AnalyzeDocumentUseCase:
    def __init__(
            self,
            document_repository: DocumentRepository,
            document_analyzer_service: DocumentAnalyzerService
    ):
        self.document_repository = document_repository
        self.document_analyzer_service = document_analyzer_service

    async def execute(self, document_id: UUID) -> DocumentResponseDTO:
        """
        Analiza un documento para identificar riesgos

        Args:
            document_id: ID del documento a analizar

        Returns:
            DTO del documento analizado

        Raises:
            ValueError: Si el documento no existe
        """
        # Obtener documento
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            raise ValueError(f"Document with ID {document_id} not found")

        # Analizar documento
        analyzed_document = await self.document_analyzer_service.analyze_document(document)

        # Guardar documento analizado
        updated_document = await self.document_repository.update(analyzed_document)

        # Mapear y retornar DTO
        return document_to_response_dto(updated_document)