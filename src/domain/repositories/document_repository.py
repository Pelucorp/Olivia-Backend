from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.document import Document


class DocumentRepository(ABC):
    """Interfaz para repositorio de documentos."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Document]:
        """
        Obtiene un documento por su ID.

        Args:
            id: ID del documento

        Returns:
            Document si se encuentra, None en caso contrario
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[Document]:
        """
        Obtiene todos los documentos.

        Returns:
            Lista de documentos
        """
        pass

    @abstractmethod
    async def save(self, document: Document) -> Document:
        """
        Guarda un nuevo documento.

        Args:
            document: Documento a guardar

        Returns:
            Documento guardado con ID actualizado
        """
        pass

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """
        Actualiza un documento existente.

        Args:
            document: Documento a actualizar

        Returns:
            Documento actualizado
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Elimina un documento por su ID.

        Args:
            id: ID del documento a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass