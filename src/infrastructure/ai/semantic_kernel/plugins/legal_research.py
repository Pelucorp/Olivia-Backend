from semantic_kernel import Context
from semantic_kernel.skill_definition import sk_function


class LegalResearchPlugin:
    """
    Plugin simple para consultas doctrinales / jurisprudenciales.
    """

    @sk_function(
        description="Responde preguntas legales breves sobre legislación peruana.",
        name="quick_research",
    )
    async def quick_research(self, context: Context, question: str) -> str:
        prompt = f"""
Eres un investigador jurídico peruano. Responde en máximo 5–6 líneas:

PREGUNTA:
{question}
"""
        return await context.kernel.chat.complete(prompt)
