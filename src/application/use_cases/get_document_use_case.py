from uuid import UUID

from src.domain.repositories.document_repository import DocumentRepository
from src.application.dtos.document_dto import DocumentResponseDTO
from src.infrastructure.mappers.document_mapper import document_to_response_dto


class GetDocumentUseCase:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def execute(self, document_id: UUID) -> DocumentResponseDTO:
        """
        Obtiene un documento por su ID

        Args:
            document_id: ID del documento a obtener

        Returns:
            DTO del documento

        Raises:
            ValueError: Si el documento no existe
        """
        document = await self.document_repository.get_by_id(document_id)

        if not document:
            raise ValueError(f"Document with ID {document_id} not found")

        return document_to_response_dto(document)