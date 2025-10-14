"""
MCP Service 2: ffe_encoder
Convierte embeddings LLM → tensores FFE {3,9,27}
"""

import numpy as np
from typing import List, Dict, Optional
import sys
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from genesis_core import FFETensor


class FFEEncoderService:
    """
    Codifica embeddings planos a estructura FFE fractal
    Timeout: 1s por request
    """
    
    def __init__(self, catalog_path: str = "catalogs/ffe_catalog.yaml"):
        self.timeout = 1.0
        catalog_full_path = Path(__file__).parent.parent / catalog_path
        with open(catalog_full_path, 'r', encoding='utf-8') as f:
            self.catalog = yaml.safe_load(f)
    
    def quantize_to_discrete(self, values: np.ndarray, n_levels: int = 8) -> List[int]:
        """
        Cuantiza valores continuos a discretos {0..n_levels-1}
        """
        # Normalizar a [0, 1]
        normalized = (values - values.min()) / (values.max() - values.min() + 1e-8)
        # Cuantizar
        quantized = (normalized * (n_levels - 0.01)).astype(int)
        return np.clip(quantized, 0, n_levels - 1).tolist()
    
    def encode_hierarchical(self, embedding: np.ndarray) -> FFETensor:
        """
        Codificación jerárquica en 3 niveles: {3, 9, 27}
        Usa partición semántica del espacio de embeddings
        
        Estrategia:
        - Level 1 (3): Partición principal en tercios
        - Level 2 (9): Subdivisión de cada tercio en 3 partes
        - Level 3 (27): Subdivisión final en 3 partes
        """
        n_dim = len(embedding)
        
        # Nivel 1: 3 particiones principales
        chunk_size_l1 = n_dim // 3
        level_1 = []
        level_2 = []
        level_3 = []
        
        for i in range(3):
            # Chunk para axis i
            start_l1 = i * chunk_size_l1
            end_l1 = start_l1 + chunk_size_l1 if i < 2 else n_dim
            chunk_l1 = embedding[start_l1:end_l1]
            
            # Level 1: promedio del chunk principal
            avg_l1 = np.mean(chunk_l1)
            # Cuantizar a 0-7
            level_1.append(int((avg_l1 + 1) / 2 * 7.99) % 8)
            
            # Level 2: 3 sub-chunks
            chunk_size_l2 = len(chunk_l1) // 3
            sub_values_l2 = []
            axis_level_3 = []
            
            for j in range(3):
                start_l2 = j * chunk_size_l2
                end_l2 = start_l2 + chunk_size_l2 if j < 2 else len(chunk_l1)
                chunk_l2 = chunk_l1[start_l2:end_l2]
                
                # Level 2 value
                avg_l2 = np.mean(chunk_l2)
                sub_values_l2.append(int((avg_l2 + 1) / 2 * 7.99) % 8)
                
                # Level 3: 3 micro-chunks
                chunk_size_l3 = len(chunk_l2) // 3
                sub_values_l3 = []
                
                for k in range(3):
                    start_l3 = k * chunk_size_l3
                    end_l3 = start_l3 + chunk_size_l3 if k < 2 else len(chunk_l2)
                    chunk_l3 = chunk_l2[start_l3:end_l3]
                    
                    if len(chunk_l3) > 0:
                        avg_l3 = np.mean(chunk_l3)
                        sub_values_l3.append(int((avg_l3 + 1) / 2 * 7.99) % 8)
                    else:
                        sub_values_l3.append(0)
                
                axis_level_3.append(sub_values_l3)
            
            level_2.append(sub_values_l2)
            level_3.append(axis_level_3)
        
        return FFETensor(level_1=level_1, level_2=level_2, level_3=level_3)
    
    def encode(self, embedding: List[float]) -> Dict:
        """
        Endpoint MCP principal: embedding → FFETensor
        
        Contract:
        Input: {"embedding": List[float]}
        Output: {"ffe_tensor": dict, "status": str}
        """
        try:
            arr = np.array(embedding)
            tensor = self.encode_hierarchical(arr)
            
            return {
                "ffe_tensor": {
                    "level_1": tensor.level_1,
                    "level_2": tensor.level_2,
                    "level_3": tensor.level_3,
                    "flat": tensor.to_flat(),
                    "hash": tensor.hash()
                },
                "status": "ok",
                "service": "ffe_encoder_v1"
            }
        except Exception as e:
            return {
                "ffe_tensor": None,
                "status": "error",
                "error": str(e),
                "service": "ffe_encoder_v1"
            }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("FFE ENCODER SERVICE - Test")
    print("=" * 60)
    
    encoder = FFEEncoderService()
    
    # Test 1: Codificación básica
    print("\n[TEST 1] Codificación básica...")
    fake_embedding = np.random.randn(768).tolist()
    result = encoder.encode(fake_embedding)
    print(f"✓ Status: {result['status']}")
    print(f"✓ FFE Hash: {result['ffe_tensor']['hash']}")
    print(f"✓ Level 1: {result['ffe_tensor']['level_1']}")
    print(f"✓ Flat size: {len(result['ffe_tensor']['flat'])} (expected 39)")
    assert len(result['ffe_tensor']['flat']) == 39, "Flat tensor debe tener 39 elementos"
    
    # Test 2: Valores en rango 0-7
    print("\n[TEST 2] Validación de rango 0-7...")
    flat = result['ffe_tensor']['flat']
    assert all(0 <= v <= 7 for v in flat), "Todos los valores deben estar en [0, 7]"
    print(f"✓ Todos los valores en rango correcto")
    print(f"✓ Min: {min(flat)}, Max: {max(flat)}")
    
    # Test 3: Consistencia
    print("\n[TEST 3] Consistencia de codificación...")
    result1 = encoder.encode(fake_embedding)
    result2 = encoder.encode(fake_embedding)
    assert result1['ffe_tensor']['hash'] == result2['ffe_tensor']['hash'], "Mismo embedding debe dar mismo hash"
    print(f"✓ Hash consistente: {result1['ffe_tensor']['hash']}")
    
    # Test 4: Diversidad
    print("\n[TEST 4] Diversidad entre embeddings distintos...")
    emb1 = np.random.randn(768).tolist()
    emb2 = np.random.randn(768).tolist()
    res1 = encoder.encode(emb1)
    res2 = encoder.encode(emb2)
    assert res1['ffe_tensor']['hash'] != res2['ffe_tensor']['hash'], "Embeddings distintos deben dar hashes distintos"
    print(f"✓ Hash 1: {res1['ffe_tensor']['hash']}")
    print(f"✓ Hash 2: {res2['ffe_tensor']['hash']}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
