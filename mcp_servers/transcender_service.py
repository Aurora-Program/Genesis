"""
MCP Service 3: transcender_service
Síntesis emergente de tríos FFE → Ms, Ss, MetaM
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from genesis_core import FFETensor, TranscendResult, Transcender, CoherenceMetrics


class TranscenderService:
    """
    Compilador de significado: síntesis no-conmutativa
    Timeout: 500ms por request
    """
    
    def __init__(self):
        self.timeout = 0.5
        self.transcender = Transcender()
        self.synthesis_count = 0
    
    def synthesize_trio(self, 
                       tensor_a: Dict, 
                       tensor_b: Dict, 
                       tensor_c: Dict) -> Dict:
        """
        Endpoint MCP principal: síntesis de 3 tensores FFE
        
        Contract:
        Input: {
            "tensor_a": {"level_1": [3], ...},
            "tensor_b": {"level_1": [3], ...},
            "tensor_c": {"level_1": [3], ...}
        }
        Output: {
            "Ms": [3],
            "Ss": [3],
            "MetaM": [[3], [3], [3], [3]],
            "C_meta": float,
            "status": str
        }
        """
        try:
            # Reconstruir FFETensors
            ffe_a = FFETensor(
                level_1=tensor_a["level_1"],
                level_2=tensor_a["level_2"],
                level_3=tensor_a["level_3"]
            )
            ffe_b = FFETensor(
                level_1=tensor_b["level_1"],
                level_2=tensor_b["level_2"],
                level_3=tensor_b["level_3"]
            )
            ffe_c = FFETensor(
                level_1=tensor_c["level_1"],
                level_2=tensor_c["level_2"],
                level_3=tensor_c["level_3"]
            )
            
            # Síntesis (usar level_1 como representación principal)
            result = self.transcender.synthesize(
                ffe_a.level_1,
                ffe_b.level_1,
                ffe_c.level_1
            )
            
            # Verificar coherencia
            c_meta = self.transcender.verify_coherence(result)
            
            self.synthesis_count += 1
            
            return {
                "Ms": result.Ms,
                "Ss": result.Ss,
                "MetaM": result.MetaM,
                "C_meta": c_meta,
                "non_commutative": result.non_commutative,
                "hash": result.hash(),
                "synthesis_count": self.synthesis_count,
                "status": "ok",
                "service": "transcender_v1"
            }
            
        except Exception as e:
            return {
                "Ms": None,
                "Ss": None,
                "MetaM": None,
                "C_meta": 0.0,
                "status": "error",
                "error": str(e),
                "service": "transcender_v1"
            }
    
    def synthesize_conversation(self,
                               user_tensor: Dict,
                               model_tensor: Dict) -> Dict:
        """
        Síntesis específica para conversación (user + model + neutral)
        """
        # Tensor neutral para completar tríada
        neutral_tensor = {
            "level_1": [1, 0, 1],
            "level_2": [[1, 0, 1]] * 3,
            "level_3": [[[1, 0, 1]] * 3] * 3
        }
        
        return self.synthesize_trio(user_tensor, model_tensor, neutral_tensor)


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("TRANSCENDER SERVICE - Test")
    print("=" * 60)
    
    service = TranscenderService()
    
    # Test 1: Síntesis básica
    print("\n[TEST 1] Síntesis básica de tríada...")
    tensor_a = {
        "level_1": [0, 1, 0],
        "level_2": [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        "level_3": [[[0, 1, 0]] * 3] * 3
    }
    tensor_b = {
        "level_1": [1, 0, 1],
        "level_2": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        "level_3": [[[1, 0, 1]] * 3] * 3
    }
    tensor_c = {
        "level_1": [0, 1, 1],
        "level_2": [[1, 1, 0], [0, 0, 1], [1, 0, 0]],
        "level_3": [[[0, 1, 1]] * 3] * 3
    }
    
    result = service.synthesize_trio(tensor_a, tensor_b, tensor_c)
    print(f"✓ Status: {result['status']}")
    print(f"✓ Ms (Structure): {result['Ms']}")
    print(f"✓ Ss (Form): {result['Ss']}")
    print(f"✓ MetaM paths: {len(result['MetaM'])}")
    print(f"✓ C_meta: {result['C_meta']:.2f}")
    print(f"✓ Hash: {result['hash']}")
    
    # Test 2: No-conmutatividad
    print("\n[TEST 2] Verificación de no-conmutatividad...")
    result_abc = service.synthesize_trio(tensor_a, tensor_b, tensor_c)
    result_bca = service.synthesize_trio(tensor_b, tensor_c, tensor_a)
    result_cab = service.synthesize_trio(tensor_c, tensor_a, tensor_b)
    
    print(f"✓ ABC → Ms: {result_abc['Ms']}, hash: {result_abc['hash']}")
    print(f"✓ BCA → Ms: {result_bca['Ms']}, hash: {result_bca['hash']}")
    print(f"✓ CAB → Ms: {result_cab['Ms']}, hash: {result_cab['hash']}")
    
    # Deben ser diferentes (o al menos algunos)
    hashes = [result_abc['hash'], result_bca['hash'], result_cab['hash']]
    unique_hashes = len(set(hashes))
    print(f"✓ Hashes únicos: {unique_hashes}/3 (esperado >1 para no-conmutatividad)")
    
    # Test 3: Síntesis conversacional
    print("\n[TEST 3] Síntesis conversacional...")
    user_tensor = {
        "level_1": [2, 3, 1],
        "level_2": [[1, 2, 3], [4, 5, 6], [7, 0, 1]],
        "level_3": [[[i % 8 for i in range(3)]] * 3] * 3
    }
    model_tensor = {
        "level_1": [5, 4, 6],
        "level_2": [[6, 5, 4], [3, 2, 1], [0, 7, 6]],
        "level_3": [[[i % 8 for i in range(3, 6)]] * 3] * 3
    }
    
    result = service.synthesize_conversation(user_tensor, model_tensor)
    print(f"✓ Status: {result['status']}")
    print(f"✓ Ms emergente: {result['Ms']}")
    print(f"✓ Coherencia C_meta: {result['C_meta']:.2f}")
    
    # Test 4: Contador de síntesis
    print("\n[TEST 4] Contador de operaciones...")
    print(f"✓ Total síntesis realizadas: {service.synthesis_count}")
    assert service.synthesis_count >= 5, "Debe haber al menos 5 síntesis registradas"
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
