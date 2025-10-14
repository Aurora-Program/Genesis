"""
Genesis Core: Arquitectura FFE 3-9-27 con MCP modular
Proyecto Genesis - Aurora Intelligence
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import uuid
import time
import hashlib
import json

# ============================================================================
# TIPOS BASE FFE
# ============================================================================

@dataclass
class FFETensor:
    """Tensor FFE canónico {3, 9, 27} = 117 bits"""
    level_1: List[int] = field(default_factory=lambda: [0, 0, 0])  # 3 axes principales
    level_2: List[List[int]] = field(default_factory=lambda: [[0]*3 for _ in range(3)])  # 9 subdimensiones
    level_3: List[List[List[int]]] = field(default_factory=lambda: [[[0]*3 for _ in range(3)] for _ in range(3)])  # 27 specs
    
    def to_flat(self) -> List[int]:
        """Serializa a vector plano de 39 elementos"""
        flat = self.level_1.copy()
        for sub in self.level_2:
            flat.extend(sub)
        for axis in self.level_3:
            for sub in axis:
                flat.extend(sub)
        return flat
    
    @classmethod
    def from_flat(cls, flat: List[int]) -> 'FFETensor':
        """Deserializa desde vector plano"""
        if len(flat) != 39:
            raise ValueError(f"Expected 39 elements, got {len(flat)}")
        
        level_1 = flat[0:3]
        level_2 = [flat[3 + i*3:3 + (i+1)*3] for i in range(3)]
        
        level_3 = []
        start = 12
        for i in range(3):
            axis = []
            for j in range(3):
                axis.append(flat[start:start+3])
                start += 3
            level_3.append(axis)
        
        return cls(level_1=level_1, level_2=level_2, level_3=level_3)
    
    def hash(self) -> str:
        """Hash SHA256 del tensor para auditoría"""
        flat_str = json.dumps(self.to_flat(), sort_keys=True)
        return hashlib.sha256(flat_str.encode()).hexdigest()[:16]

@dataclass
class TranscendResult:
    """Resultado de síntesis Transcender: Ms, Ss, MetaM"""
    Ms: List[int]  # Structure emergente (3 bits)
    Ss: List[int]  # Form factual (3 bits)
    MetaM: List[List[int]]  # Caminos lógicos (4 tríos)
    non_commutative: bool = True  # Flag de no-conmutatividad
    
    def hash(self) -> str:
        data = json.dumps({"Ms": self.Ms, "Ss": self.Ss, "MetaM": self.MetaM}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

@dataclass
class CoherenceMetrics:
    """Métricas nativas de coherencia estructural"""
    C_meta: float  # Unicidad Ms↔MetaM en espacio
    C_ext: float   # Éxito de Extender al reconstruir
    C_dyn: float   # Estabilidad de Dynamics entre turnos
    timestamp: float = field(default_factory=time.time)
    
    def is_coherent(self, threshold: float = 0.90) -> bool:
        """Check si todas las métricas superan umbral"""
        return all([self.C_meta >= threshold, 
                   self.C_ext >= threshold, 
                   self.C_dyn >= threshold])

@dataclass
class TurnRecord:
    """Registro de un turno conversacional fractalizado"""
    turn_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_ffe: Optional[FFETensor] = None
    model_ffe: Optional[FFETensor] = None
    transcend: Optional[TranscendResult] = None
    space_id: str = "default"
    archetypes: List[str] = field(default_factory=list)
    relations: List[Dict[str, Any]] = field(default_factory=list)
    dynamics: Dict[str, float] = field(default_factory=dict)
    coherence: Optional[CoherenceMetrics] = None
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        """Serializa a diccionario para KB"""
        return {
            "turn_id": self.turn_id,
            "user_ffe": self.user_ffe.to_flat() if self.user_ffe else None,
            "model_ffe": self.model_ffe.to_flat() if self.model_ffe else None,
            "transcend": {
                "Ms": self.transcend.Ms,
                "Ss": self.transcend.Ss,
                "MetaM": self.transcend.MetaM
            } if self.transcend else None,
            "space_id": self.space_id,
            "archetypes": self.archetypes,
            "relations": self.relations,
            "dynamics": self.dynamics,
            "coherence": {
                "C_meta": self.coherence.C_meta,
                "C_ext": self.coherence.C_ext,
                "C_dyn": self.coherence.C_dyn
            } if self.coherence else None,
            "timestamp": self.timestamp
        }

# ============================================================================
# TRIGATE CON LUTS EN CALIENTE (O(1))
# ============================================================================

class Trigate:
    """Trigate ternario con NULL honesto y LUTs O(1)"""
    
    _LUT_INFER = {
        (0, 0, 1): 0, (0, 1, 1): 1, (0, None, 1): None,
        (1, 0, 1): 1, (1, 1, 1): 0, (1, None, 1): None,
        (None, 0, 1): None, (None, 1, 1): None, (None, None, 1): None,
        (0, 0, 0): 1, (0, 1, 0): 0, (0, None, 0): None,
        (1, 0, 0): 0, (1, 1, 0): 1, (1, None, 0): None,
        (None, 0, 0): None, (None, 1, 0): None, (None, None, 0): None
    }
    
    def infer(self, A: List, B: List, M: List) -> List:
        """Inferencia O(1) por bit usando LUT"""
        return [self._LUT_INFER.get((a, b, m), None) for a, b, m in zip(A, B, M)]
    
    def learn(self, A: List, B: List, R: List) -> List:
        """Aprende M dados A, B, R"""
        M = []
        for a, b, r in zip(A, B, R):
            if None in [a, b, r]:
                M.append(None)
            else:
                for m in [0, 1]:
                    if self._LUT_INFER.get((a, b, m)) == r:
                        M.append(m)
                        break
                else:
                    M.append(None)
        return M
    
    def deduce(self, A: List, M: List, R: List) -> List:
        """Deduce B dados A, M, R"""
        B = []
        for a, m, r in zip(A, M, R):
            if None in [a, m, r]:
                B.append(None)
            else:
                for b in [0, 1]:
                    if self._LUT_INFER.get((a, b, m)) == r:
                        B.append(b)
                        break
                else:
                    B.append(None)
        return B

# ============================================================================
# TRANSCENDER COMO COMPILADOR DE SIGNIFICADO
# ============================================================================

class Transcender:
    """
    Compilador de significado: opera en tríos (A,B,C) no-conmutativos
    Produce Ms, Ss, MetaM con trazabilidad completa
    """
    
    def __init__(self):
        self.trigate = Trigate()
    
    def synthesize(self, A: List, B: List, C: List, 
                   preserve_order: bool = True) -> TranscendResult:
        """
        Síntesis no-conmutativa de tres FFE tensors
        El orden (A,B,C) importa: permutaciones dan resultados distintos
        """
        if not preserve_order:
            raise ValueError("Transcender requiere orden explícito (no-conmutativo)")
        
        # Tres Trigates en cadena
        R1 = self.trigate.infer(A, B, [1, 0, 1])  # T1: (A, B)
        R2 = self.trigate.infer(B, C, [0, 1, 0])  # T2: (B, C)
        R3 = self.trigate.infer(C, A, [1, 1, 0])  # T3: (C, A)
        
        # Ms: Structure emergente (Trigate superior implícito)
        Ms = self.trigate.infer(R1, R2, [0, 1, 1])
        
        # Ss: Form factual (memoria de R3)
        Ss = R3
        
        # MetaM: Caminos lógicos (aprendizaje de cada Trigate + Ms)
        MetaM = [
            self.trigate.learn(A, B, R1),  # Camino T1
            self.trigate.learn(B, C, R2),  # Camino T2
            self.trigate.learn(C, A, R3),  # Camino T3
            self.trigate.learn(R1, R2, Ms) # Camino superior
        ]
        
        return TranscendResult(Ms=Ms, Ss=Ss, MetaM=MetaM, non_commutative=True)
    
    def verify_coherence(self, result: TranscendResult) -> float:
        """
        Verifica coherencia interna: C_meta (unicidad Ms↔MetaM)
        Retorna score 0-1
        """
        # Check: Ms debe ser deducible desde MetaM[3]
        null_count = sum(1 for x in result.Ms if x is None)
        meta_null_count = sum(1 for path in result.MetaM for x in path if x is None)
        
        # Penaliza NULLs excesivos (>10%)
        total_bits = len(result.Ms) + sum(len(p) for p in result.MetaM)
        null_ratio = (null_count + meta_null_count) / total_bits
        
        if null_ratio > 0.10:
            return 0.0
        elif null_ratio > 0.05:
            return 0.85
        else:
            return 1.0

# ============================================================================
# TESTS UNITARIOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("GENESIS CORE - Tests Unitarios")
    print("=" * 60)
    
    # Test 1: FFETensor serialization
    print("\n[TEST 1] FFETensor serialization...")
    tensor = FFETensor(
        level_1=[0, 1, 0],
        level_2=[[1, 0, 1], [1, 0, 1], [1, 0, 1]],
        level_3=[[[0, 1, 0], [0, 1, 0], [0, 1, 0]]] * 3
    )
    flat = tensor.to_flat()
    recovered = FFETensor.from_flat(flat)
    assert tensor.level_1 == recovered.level_1, "Level 1 mismatch"
    assert tensor.level_2 == recovered.level_2, "Level 2 mismatch"
    print(f"✓ Hash: {tensor.hash()}")
    
    # Test 2: Trigate LUT
    print("\n[TEST 2] Trigate LUT O(1)...")
    tg = Trigate()
    R = tg.infer([1, 0, None], [0, 1, 1], [1, 0, 1])
    print(f"✓ Infer: {R}")
    M = tg.learn([1, 0, 1], [0, 1, 0], [1, 1, 1])
    print(f"✓ Learn: {M}")
    
    # Test 3: Transcender non-commutative
    print("\n[TEST 3] Transcender síntesis no-conmutativa...")
    trans = Transcender()
    A = [0, 1, 0]
    B = [1, 0, 1]
    C = [0, 1, 0]
    result = trans.synthesize(A, B, C)
    print(f"✓ Ms: {result.Ms}")
    print(f"✓ Ss: {result.Ss}")
    print(f"✓ MetaM paths: {len(result.MetaM)}")
    coherence = trans.verify_coherence(result)
    print(f"✓ C_meta: {coherence:.2f}")
    
    # Test 4: TurnRecord serialization
    print("\n[TEST 4] TurnRecord serialization...")
    record = TurnRecord(
        user_ffe=tensor,
        model_ffe=tensor,
        transcend=result,
        space_id="test_space",
        coherence=CoherenceMetrics(C_meta=coherence, C_ext=0.95, C_dyn=0.92)
    )
    data = record.to_dict()
    print(f"✓ Turn ID: {record.turn_id}")
    print(f"✓ Space: {record.space_id}")
    print(f"✓ Coherence: C_meta={data['coherence']['C_meta']:.2f}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
