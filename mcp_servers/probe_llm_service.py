"""
MCP Service 1: probe_llm
Extrae embeddings del LLM y metadata conversacional
"""

from typing import Dict, List, Optional
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from genesis_core import FFETensor


class ProbeLLMService:
    """
    Extrae representaciones internas del LLM
    Timeout: 2s por request
    """
    
    def __init__(self, llm_endpoint: str = "local"):
        self.endpoint = llm_endpoint
        self.timeout = 2.0
    
    def extract_embedding(self, text: str, 
                         layer: int = -1) -> Optional[np.ndarray]:
        """
        Extrae embedding de una capa específica del LLM
        Returns: vector de dimensión variable (típicamente 768-4096)
        """
        # TODO: Integrar con LLM real (OpenAI, local, etc.)
        # Por ahora: simulación basada en hash del texto
        seed = hash(text) % (2**32)
        np.random.seed(seed)
        embedding = np.random.randn(768)
        # Normalizar
        return embedding / np.linalg.norm(embedding)
    
    def extract_metadata(self, text: str) -> Dict:
        """
        Extrae metadata conversacional: topic, sentiment, intent
        """
        # Análisis básico
        words = text.split()
        
        # Detección simple de sentimiento
        positive_words = {"bien", "bueno", "excelente", "feliz", "amor", "paz"}
        negative_words = {"mal", "malo", "triste", "odio", "guerra", "dolor"}
        
        pos_count = sum(1 for w in words if w.lower() in positive_words)
        neg_count = sum(1 for w in words if w.lower() in negative_words)
        
        sentiment = 0.0
        if pos_count + neg_count > 0:
            sentiment = (pos_count - neg_count) / (pos_count + neg_count)
        
        # Detección de pregunta
        is_question = "?" in text or any(text.lower().startswith(q) for q in ["qué", "cómo", "por qué", "cuál", "dónde"])
        
        return {
            "length": len(text),
            "words": len(words),
            "language": "es" if any(c in text.lower() for c in "ñáéíóú") else "en",
            "sentiment": sentiment,
            "is_question": is_question,
            "topic_hint": "question" if is_question else "statement"
        }
    
    def probe(self, text: str) -> Dict:
        """
        Endpoint MCP principal: extrae embedding + metadata
        
        Contract:
        Input: {"text": str}
        Output: {"embedding": array, "metadata": dict, "status": str}
        """
        try:
            embedding = self.extract_embedding(text)
            metadata = self.extract_metadata(text)
            
            return {
                "embedding": embedding.tolist(),
                "metadata": metadata,
                "status": "ok",
                "service": "probe_llm_v1"
            }
        except Exception as e:
            return {
                "embedding": None,
                "metadata": {},
                "status": "error",
                "error": str(e),
                "service": "probe_llm_v1"
            }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("PROBE LLM SERVICE - Test")
    print("=" * 60)
    
    service = ProbeLLMService()
    
    # Test 1: Extracción básica
    print("\n[TEST 1] Extracción básica...")
    result = service.probe("Hola, ¿cómo estás?")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Embedding shape: {len(result['embedding'])}")
    print(f"✓ Metadata: {result['metadata']}")
    
    # Test 2: Sentimiento
    print("\n[TEST 2] Análisis de sentimiento...")
    texts = [
        "Me siento muy feliz y en paz",
        "Esto es terrible y doloroso",
        "El cielo es azul"
    ]
    for text in texts:
        result = service.probe(text)
        sentiment = result['metadata']['sentiment']
        print(f"✓ '{text[:30]}...' → sentiment={sentiment:.2f}")
    
    # Test 3: Consistencia de embeddings
    print("\n[TEST 3] Consistencia de embeddings...")
    text = "Test de consistencia"
    emb1 = service.extract_embedding(text)
    emb2 = service.extract_embedding(text)
    similarity = np.dot(emb1, emb2)
    print(f"✓ Mismo texto, mismo embedding: similarity={similarity:.4f}")
    assert similarity > 0.99, "Los embeddings deben ser idénticos para el mismo texto"
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
