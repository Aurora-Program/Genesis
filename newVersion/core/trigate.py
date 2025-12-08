"""
Trigate - Unidad fundamental de computación ternaria
Lógica 0/1/None con LUTs O(1) para 4 operaciones:
  - infer(A,B,M) → R
  - learn(A,B,R) → M
  - deduce_a(B,M,R) → A
  - deduce_b(A,M,R) → B
"""

from dataclasses import dataclass
from typing import List, Optional

Trit = Optional[int]  # 0 | 1 | None

def _norm3(v: List[Trit]) -> List[Trit]:
    """Normaliza a vector ternario de 3 bits"""
    v = list(v)[:3] + [0, 0, 0]
    return [(None if x is None else (1 if x == 1 else 0)) for x in v[:3]]

def _xor(a: Trit, b: Trit) -> Trit:
    return None if (a is None or b is None) else (a ^ b)

def _xnor(a: Trit, b: Trit) -> Trit:
    return None if (a is None or b is None) else (1 if a == b else 0)


@dataclass
class TrigateRecord:
    """Record completo de un Trigate (SIEMPRE 3 bits)"""
    A: List[Trit]  # entrada 1
    B: List[Trit]  # entrada 2
    M: List[Trit]  # control/aprendizaje
    R: List[Trit]  # salida

    def __post_init__(self):
        self.A = _norm3(self.A)
        self.B = _norm3(self.B)
        self.M = _norm3(self.M)
        self.R = _norm3(self.R)


class Trigate:
    """
    Trigate: Unidad de computación ternaria con LUTs.
    Todas las operaciones son O(1) bit a bit.
    """
    
    # LUTs ternarias (27 combinaciones por operación)
    _INF, _LRN, _DA, _DB = {}, {}, {}, {}

    @classmethod
    def init_luts(cls):
        """Inicializa las 4 LUTs ternarias"""
        vals = [0, 1, None]
        
        # Infer: (a,b,m)→r
        for a in vals:
            for b in vals:
                for m in vals:
                    if None in (a, b, m):
                        r = None
                    else:
                        r = _xor(a, b) if m == 1 else (1 - _xor(a, b))
                    cls._INF[(a, b, m)] = r
        
        # Learn: (a,b,r)→m
        for a in vals:
            for b in vals:
                for r in vals:
                    if None in (a, b, r):
                        m = None
                    else:
                        m = 1 if r == _xor(a, b) else 0
                    cls._LRN[(a, b, r)] = m
        
        # Deduce A: (b,m,r)→a
        for b in vals:
            for m in vals:
                for r in vals:
                    if None in (b, m, r):
                        a = None
                    else:
                        a = (b ^ r) if m == 1 else (1 - (b ^ r))
                    cls._DA[(b, m, r)] = a
        
        # Deduce B: (a,m,r)→b
        for a in vals:
            for m in vals:
                for r in vals:
                    if None in (a, m, r):
                        b = None
                    else:
                        b = (a ^ r) if m == 1 else (1 - (a ^ r))
                    cls._DB[(a, m, r)] = b

    # --- Operaciones núcleo (bit a bit) ---
    @staticmethod
    def infer(A: List[Trit], B: List[Trit], M: List[Trit]) -> List[Trit]:
        """R = infer(A, B, M)"""
        A, B, M = _norm3(A), _norm3(B), _norm3(M)
        return [Trigate._INF[(a, b, m)] for a, b, m in zip(A, B, M)]

    @staticmethod
    def learn(A: List[Trit], B: List[Trit], R: List[Trit]) -> List[Trit]:
        """M = learn(A, B, R)"""
        A, B, R = _norm3(A), _norm3(B), _norm3(R)
        return [Trigate._LRN[(a, b, r)] for a, b, r in zip(A, B, R)]

    @staticmethod
    def deduce_a(B: List[Trit], M: List[Trit], R: List[Trit]) -> List[Trit]:
        """A = deduce_a(B, M, R)"""
        B, M, R = _norm3(B), _norm3(M), _norm3(R)
        return [Trigate._DA[(b, m, r)] for b, m, r in zip(B, M, R)]

    @staticmethod
    def deduce_b(A: List[Trit], M: List[Trit], R: List[Trit]) -> List[Trit]:
        """B = deduce_b(A, M, R)"""
        A, M, R = _norm3(A), _norm3(M), _norm3(R)
        return [Trigate._DB[(a, m, r)] for a, m, r in zip(A, M, R)]

    # --- Helpers para construir records coherentes ---
    @staticmethod
    def from_inputs(A: List[Trit], B: List[Trit], M: List[Trit]) -> TrigateRecord:
        """Crea record desde inputs, infiriendo R"""
        R = Trigate.infer(A, B, M)
        return TrigateRecord(A=_norm3(A), B=_norm3(B), M=_norm3(M), R=_norm3(R))

    @staticmethod
    def from_learning(A: List[Trit], B: List[Trit], R: List[Trit]) -> TrigateRecord:
        """Crea record desde inputs+output, aprendiendo M"""
        M = Trigate.learn(A, B, R)
        return TrigateRecord(A=_norm3(A), B=_norm3(B), M=_norm3(M), R=_norm3(R))


# Inicializar LUTs al importar
Trigate.init_luts()
