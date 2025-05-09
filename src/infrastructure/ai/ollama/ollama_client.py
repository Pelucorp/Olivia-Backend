import aiohttp
import json
from typing import Dict, Any, List, Optional
import os


class OllamaClient:
    """Cliente para comunicación con el servicio Ollama."""

    def __init__(
            self,
            base_url: str = None,
            model_name: str = None
    ):
        self.base_url = base_url or os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Genera texto a partir de un prompt.

        Args:
            prompt: Texto de la consulta
            system_prompt: Instrucciones de sistema (opcional)

        Returns:
            Texto generado

        Raises:
            Exception: Si hay error en la comunicación con Ollama
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Error from Ollama API: {error_text}")

                data = await response.json()
                return data["response"]

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Mantiene una conversación con el modelo.

        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]

        Returns:
            Respuesta del modelo

        Raises:
            Exception: Si hay error en la comunicación con Ollama
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Error from Ollama API: {error_text}")

                data = await response.json()
                return data["message"]["content"]

    async def get_models(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de modelos disponibles en Ollama.

        Returns:
            Lista de modelos

        Raises:
            Exception: Si hay error en la comunicación con Ollama
        """
        url = f"{self.base_url}/api/tags"

        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Error from Ollama API: {error_text}")

                data = await response.json()
                return data.get("models", [])