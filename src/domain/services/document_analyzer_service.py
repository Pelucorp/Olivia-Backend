from src.domain.entities.document import Document
from src.domain.entities.risk import Risk
import json
from typing import List, Dict, Any
from uuid import uuid4


class DocumentAnalyzerService:
    """Servicio de dominio para analizar documentos legales."""

    def __init__(self, ai_service):
        """
        Inicializa el servicio con un cliente de IA.

        Args:
            ai_service: Cliente para comunicación con servicios de IA
        """
        self.ai_service = ai_service

    async def analyze_document(self, document: Document) -> Document:
        """
        Analiza un documento para identificar riesgos.

        Args:
            document: Documento a analizar

        Returns:
            Documento con riesgos identificados
        """
        # Construir el prompt para analizar el documento
        prompt = self._build_analysis_prompt(document)

        # Obtener respuesta del servicio de IA
        raw_response = await self.ai_service.generate(prompt)

        # Procesar la respuesta para extraer riesgos
        risks = self._extract_risks_from_response(raw_response)

        # Añadir riesgos al documento
        for risk in risks:
            document.add_risk(risk)

        return document

    def _build_analysis_prompt(self, document: Document) -> str:
        """
        Construye el prompt para el análisis de documentos.

        Args:
            document: Documento a analizar

        Returns:
            String con el prompt formateado
        """
        return f"""
        Eres un asistente legal especializado. Analiza el siguiente documento de tipo {document.type} 
        e identifica posibles riesgos legales.

        DOCUMENTO:
        {document.content}

        Proporciona tu análisis en formato JSON con la siguiente estructura:
        {{
            "risks": [
                {{
                    "severity": "high|medium|low",
                    "description": "Descripción del riesgo",
                    "related_text": "Texto relacionado con el riesgo (extracto del documento)",
                    "recommendation": "Recomendación para mitigar el riesgo"
                }}
            ]
        }}

        Responde únicamente con el JSON, sin explicaciones adicionales.
        """

    def _extract_risks_from_response(self, response: str) -> List[Risk]:
        """
        Extrae riesgos de la respuesta del LLM.

        Args:
            response: Respuesta del LLM

        Returns:
            Lista de entidades Risk
        """
        risks = []

        try:
            # Intentar encontrar el bloque JSON en la respuesta
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)

                for risk_data in data.get('risks', []):
                    risk = Risk(
                        id=uuid4(),
                        severity=risk_data.get('severity', 'medium'),
                        description=risk_data.get('description', ''),
                        related_text=risk_data.get('related_text'),
                        recommendation=risk_data.get('recommendation')
                    )
                    risks.append(risk)
        except (json.JSONDecodeError, KeyError) as e:
            # En caso de error, crear un riesgo genérico de error
            risk = Risk(
                id=uuid4(),
                severity='high',
                description='Error al procesar la respuesta del análisis',
                related_text=None,
                recommendation='Revisar manualmente el documento'
            )
            risks.append(risk)

        return risks