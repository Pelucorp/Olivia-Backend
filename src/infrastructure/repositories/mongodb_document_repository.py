from typing import List, Optional, Dict, Any
from uuid import UUID

from src.domain.entities.document import Document
from src.domain.entities.risk import Risk
from src.domain.repositories.document_repository import DocumentRepository
from src.infrastructure.database.mongodb_client import MongoDBClient


class MongoDBDocumentRepository(DocumentRepository):
    """Implementación del repositorio de documentos con MongoDB."""

    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client

    async def get_collection(self):
        """Obtiene la colección de documentos."""
        db = await self.mongodb_client.get_database()
        return db.documents

    async def get_by_id(self, id: UUID) -> Optional[Document]:
        """Obtiene un documento por su ID."""
        collection = await self.get_collection()
        doc_data = await collection.find_one({"id": str(id)})

        if not doc_data:
            return None

        return self._map_to_entity(doc_data)

    async def get_all(self) -> List[Document]:
        """Obtiene todos los documentos."""
        collection = await self.get_collection()
        cursor = collection.find()
        documents = await cursor.to_list(length=100)  # Limitar a 100 documentos por consulta

        return [self._map_to_entity(doc_data) for doc_data in documents]

    async def save(self, document: Document) -> Document:
        """Guarda un nuevo documento."""
        collection = await self.get_collection()
        doc_data = self._map_to_dict(document)

        await collection.insert_one(doc_data)
        return document

    async def update(self, document: Document) -> Document:
        """Actualiza un documento existente."""
        collection = await self.get_collection()
        doc_data = self._map_to_dict(document)

        await collection.replace_one({"id": str(document.id)}, doc_data)
        return document

    async def delete(self, id: UUID) -> bool:
        """Elimina un documento por su ID."""
        collection = await self.get_collection()
        result = await collection.delete_one({"id": str(id)})

        return result.deleted_count > 0

    def _map_to_entity(self, doc_data: Dict[str, Any]) -> Document:
        """Convierte un diccionario a entidad Document."""
        # Mapear riesgos
        risks = []
        for risk_data in doc_data.get("risks", []):
            risk = Risk(
                id=UUID(risk_data["id"]),
                severity=risk_data["severity"],
                description=risk_data["description"],
                related_text=risk_data.get("related_text"),
                recommendation=risk_data.get("recommendation")
            )
            risks.append(risk)

        # Crear documento
        document = Document(
            id=UUID(doc_data["id"]),
            title=doc_data["title"],
            content=doc_data["content"],
            type=doc_data["type"],
            created_at=doc_data["created_at"],
            risks=risks
        )

        return document

    def _map_to_dict(self, document: Document) -> Dict[str, Any]:
        """Convierte una entidad Document a diccionario para MongoDB."""
        # Mapear riesgos
        risks_data = []
        for risk in document.risks:
            risk_data = {
                "id": str(risk.id),
                "severity": risk.severity,
                "description": risk.description
            }

            if risk.related_text:
                risk_data["related_text"] = risk.related_text

            if risk.recommendation:
                risk_data["recommendation"] = risk.recommendation

            risks_data.append(risk_data)

        # Crear diccionario
        doc_data = {
            "id": str(document.id),
            "title": document.title,
            "content": document.content,
            "type": document.type,
            "created_at": document.created_at,
            "risks": risks_data
        }

        return doc_data