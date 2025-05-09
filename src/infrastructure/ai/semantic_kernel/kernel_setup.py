import os
from functools import lru_cache
import semantic_kernel as sk
from semantic_kernel.connectors.ai.ollama import (
    OllamaChatCompletion,
    OllamaTextCompletion,
)

# Plugins locales
from .plugins.document_analysis import DocumentAnalysisPlugin
from .plugins.legal_research import LegalResearchPlugin


class KernelFactory:
    """
    Singleton muy simple para crear / obtener una instancia de SK
    configurada con Ollama y registrar plugins caseros.
    """

    _kernel = None

    @classmethod
    @lru_cache  # garantiza que solo se ejecute una vez
    def get_kernel(cls) -> sk.Kernel:
        if cls._kernel is not None:
            return cls._kernel

        # Valores de entorno o defaults
        base_url = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
        model_id = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

        kernel = sk.Kernel()

        # Servicios de texto y chat (ambos apuntan al mismo modelo)
        kernel.add_chat_service(
            "ollama-chat",
            OllamaChatCompletion(ai_model_id=model_id, base_url=base_url),
        )
        kernel.add_text_service(
            "ollama-text",
            OllamaTextCompletion(ai_model_id=model_id, base_url=base_url),
        )

        # Registrar plugins
        kernel.import_plugin(DocumentAnalysisPlugin(), "document_analysis")
        kernel.import_plugin(LegalResearchPlugin(), "legal_research")

        cls._kernel = kernel
        return kernel
