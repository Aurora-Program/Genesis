"""
Aurora Genesis newVersion
Sistema de transformación fractal basado en Trinity-3
"""

__version__ = "1.0.0"
__author__ = "Aurora Project"

from .core import (
    Trigate,
    TrigateRecord,
    Trit,
    Transcender,
    Evolver3,
    Extender,
    Harmonizer,
    HarmonyResult,
    FractalTensor,
    FractalTranscender,
)

from .pipeline.aurora_pipeline import (
    AuroraPipeline,
    KnowledgeBase,
    FractalEvolver,
)

__all__ = [
    # Core
    "Trigate",
    "TrigateRecord",
    "Trit",
    "Transcender",
    "Evolver3",
    "Extender",
    "Harmonizer",
    "HarmonyResult",
    "FractalTensor",
    "FractalTranscender",
    # Pipeline
    "AuroraPipeline",
    "KnowledgeBase",
    "FractalEvolver",
]
