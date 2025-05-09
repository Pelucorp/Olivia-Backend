from semantic_kernel import Context
from semantic_kernel.skill_definition import sk_function


class DocumentAnalysisPlugin:
    """
    Plugin SK para analizar documentos y encontrar riesgos.
    Se apoya en el servicio de chat (“ollama-chat”) configurado
    en KernelFactory.
    """

    @sk_function(
        description="Analiza un documento legal y devuelve riesgos en JSON.",
        name="analyze_document",
    )
    async def analyze_document(
        self,
        context: Context,
        document_text: str,
        document_type: str = "contrato",
    ) -> str:
        prompt = f"""
Eres un asistente legal experto en leyes peruanas.
Analiza el siguiente documento de tipo {document_type} e identifica riesgos.

DOCUMENTO:
{document_text}

Devuelve solo JSON con:
{{
  "risks": [
    {{
      "severity": "high|medium|low",
      "description": "...",
      "related_text": "...",
      "recommendation": "..."
    }}
  ]
}}
"""
        # Llama al servicio de chat registrado
        response = await context.kernel.chat.complete(prompt)
        return response
