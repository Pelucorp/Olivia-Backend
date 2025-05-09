"""
Expone plugins para importación fácil.
"""

from .document_analysis import DocumentAnalysisPlugin
from .legal_research import LegalResearchPlugin

__all__ = [
    "DocumentAnalysisPlugin",
    "LegalResearchPlugin",
]
