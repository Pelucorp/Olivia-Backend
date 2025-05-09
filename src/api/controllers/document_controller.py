from fastapi import HTTPException, UploadFile, Depends
from uuid import UUID
from typing import List, Optional

from src.application.use_cases.get_document_use_case import GetDocumentUseCase
from src.application.use_cases.analyze_document_use_case import AnalyzeDocumentUseCase
from src.application.use_cases.upload_document_use_case import UploadDocumentUseCase
from src.application.dtos.document_dto import DocumentResponseDTO


class DocumentController:
    def __init__(
            self,
            get_document_use_case: GetDocumentUseCase = Depends(),
            analyze_document_use_case: AnalyzeDocumentUseCase = Depends(),
            upload_document_use_case: UploadDocumentUseCase = Depends()
    ):
        self.get_document_use_case = get_document_use_case
        self.analyze_document_use_case = analyze_document_use_case
        self.upload_document_use_case = upload_document_use_case

    async def get_document(self, document_id: UUID) -> DocumentResponseDTO:
        """
        Obtiene un documento por su ID
        """
        try:
            document = await self.get_document_use_case.execute(document_id)
            return document
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def analyze_document(self, document_id: UUID) -> DocumentResponseDTO:
        """
        Analiza un documento existente
        """
        try:
            document = await self.analyze_document_use_case.execute(document_id)
            return document
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def upload_document(
            self,
            file: UploadFile,
            title: str,
            doc_type: str
    ) -> DocumentResponseDTO:
        """
        Sube y procesa un nuevo documento
        """
        try:
            document = await self.upload_document_use_case.execute(
                file=file,
                title=title,
                doc_type=doc_type
            )
            return document
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))