from functools import lru_cache

from src.api.controllers.document_controller import DocumentController
from src.application.use_cases.get_document_use_case import GetDocumentUseCase
from src.application.use_cases.analyze_document_use_case import AnalyzeDocumentUseCase
from src.application.use_cases.upload_document_use_case import UploadDocumentUseCase
from src.domain.repositories.document_repository import DocumentRepository
from src.domain.services.document_analyzer_service import DocumentAnalyzerService
from src.infrastructure.repositories.mongodb_document_repository import MongoDBDocumentRepository
from src.infrastructure.ai.ollama.ollama_client import OllamaClient
from src.infrastructure.database.mongodb_client import MongoDBClient


@lru_cache
def get_mongodb_client():
    return MongoDBClient()


@lru_cache
def get_document_repository() -> DocumentRepository:
    mongodb_client = get_mongodb_client()
    return MongoDBDocumentRepository(mongodb_client)


@lru_cache
def get_ollama_client() -> OllamaClient:
    return OllamaClient()


@lru_cache
def get_document_analyzer_service() -> DocumentAnalyzerService:
    ollama_client = get_ollama_client()
    return DocumentAnalyzerService(ollama_client)


@lru_cache
def get_get_document_use_case() -> GetDocumentUseCase:
    document_repository = get_document_repository()
    return GetDocumentUseCase(document_repository)


@lru_cache
def get_analyze_document_use_case() -> AnalyzeDocumentUseCase:
    document_repository = get_document_repository()
    document_analyzer_service = get_document_analyzer_service()
    return AnalyzeDocumentUseCase(document_repository, document_analyzer_service)


@lru_cache
def get_upload_document_use_case() -> UploadDocumentUseCase:
    document_repository = get_document_repository()
    return UploadDocumentUseCase(document_repository)


@lru_cache
def get_document_controller() -> DocumentController:
    get_document_use_case = get_get_document_use_case()
    analyze_document_use_case = get_analyze_document_use_case()
    upload_document_use_case = get_upload_document_use_case()

    return DocumentController(
        get_document_use_case,
        analyze_document_use_case,
        upload_document_use_case
    )