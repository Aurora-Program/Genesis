"""
Evolver - Aprendizaje de arquetipos y dinámicas
3 bancos de patrones:
  - RELATOR: relaciones entre dimensiones
  - EMERGENCIA: patrones de síntesis (M1,M2,M3 → Ms)
  - DINÁMICA: transiciones temporales
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from functools import lru_cache
import time
from .trigate import Trit

def norm3(v: List[Trit]) -> List[Trit]:
    """Normaliza a 3 bits"""
    v = (list(v) + [0, 0, 0])[:3]
    return [None if x is None else (1 if x == 1 else 0) for x in v]

def rotate3(v: List[Trit], s: int) -> List[Trit]:
    """Rotación circular"""
    s %= 3
    return v[-s:] + v[:-s] if s else v

@lru_cache(maxsize=512)
def similarity3_cached(a_tuple: Tuple[Trit, ...], b_tuple: Tuple[Trit, ...]) -> int:
    """Similitud entre vectores (0..3)"""
    s = 0
    for x, y in zip(a_tuple, b_tuple):
        if x is None or y is None:
            continue
        if x == y:
            s += 1
    return s

def similarity3(a: List[Trit], b: List[Trit]) -> int:
    """Wrapper para listas"""
    return similarity3_cached(tuple(a), tuple(b))


@dataclass
class Proto:
    """Prototipo aprendido"""
    key: Tuple[Any, ...]
    proto: List[Trit]
    weight: float = 0.0
    count: int = 0
    last_seen: float = field(default_factory=lambda: time.time())


class Evolver3:
    """
    Evolver autosimilar (todo con Trigate).
    
    Bancos:
      1. RELATOR: aprende conexiones entre dimensiones condicionadas por Ms padre
      2. EMERGENCIA: aprende síntesis (M1,M2,M3) → Ms
      3. DINÁMICA: aprende transiciones entrada→salida
    """

    def __init__(self, trigate_cls, *, th_match: int = 2, decay: float = 0.9):
        self.T = trigate_cls
        self.th = th_match
        self.decay = decay
        
        # Bancos de patrones
        self._relator: Dict[Tuple, Proto] = {}
        self._emerg: Dict[Tuple, Proto] = {}
        self._dyn: Dict[Tuple, Proto] = {}
        
        # Contexto para dinámica
        self._last_round_ms: List[List[Trit]] = []

    def _reinforce(self, bank: Dict[Tuple, Proto], key: Tuple, candidate: List[Trit]) -> None:
        """Refuerzo EMA + llenado honesto de NULLs"""
        cand = norm3(candidate)
        if key not in bank:
            bank[key] = Proto(key=key, proto=cand, weight=1.0, count=1)
            return
        
        p = bank[key]
        p.weight = p.weight * self.decay + similarity3(cand, p.proto)
        p.count += 1
        p.last_seen = time.time()
        
        # Solo rellena NULLs con nueva evidencia
        for i, (a, b) in enumerate(zip(p.proto, cand)):
            if a is None and b is not None:
                p.proto[i] = b

    # === RELATOR ===
    def observe_relator(self, Ms_parent: List[Trit], wiring: List[Tuple[str, str, str]], M1: List[Trit], M2: List[Trit], M3: List[Trit]):
        """Aprende conexiones dimensionales condicionadas por Ms padre"""
        Ms_parent = norm3(Ms_parent)
        Mloc = [norm3(M1), norm3(M2), norm3(M3)]
        wiring_hash = tuple(wiring)
        
        for role_idx, M_i in enumerate(Mloc):
            key = (tuple(Ms_parent), wiring_hash, role_idx)
            self._reinforce(self._relator, key, M_i)

    # === EMERGENCIA ===
    def observe_emergence(self, M1: List[Trit], M2: List[Trit], M3: List[Trit], Ms: List[Trit]):
        """Aprende síntesis: (M1,M2,M3) → Ms"""
        M1, M2, M3, Ms = map(norm3, (M1, M2, M3, Ms))
        
        # Ley superior
        ley_sup = self.T.learn(M1, M2, M3)
        shape = self.T.infer(M1, M2, Ms)
        
        # Patrón principal
        key_main = ("emerg",)
        self._reinforce(self._emerg, key_main, ley_sup)
        
        # Firma de hijos
        key_sig = ("emerg_sig", tuple(M1), tuple(M2), tuple(M3))
        self._reinforce(self._emerg, key_sig, Ms)
        
        # Forma
        key_shape = ("emerg_shape",)
        self._reinforce(self._emerg, key_shape, shape)

    # === DINÁMICA ===
    def observe_dynamics_round(self, ms_list_this_round: List[List[Trit]], level_tag: str):
        """Aprende transiciones entre rondas"""
        ms_curr = [norm3(m) for m in ms_list_this_round]
        
        # Transición local
        if self._last_round_ms:
            for m_prev, m_curr in zip(self._last_round_ms[:len(ms_curr)], ms_curr):
                trans = self.T.learn(m_prev, m_curr, m_curr)
                key = ("dyn_local", level_tag)
                self._reinforce(self._dyn, key, trans)
        
        # Resumen de nivel
        for i in range(0, len(ms_curr), 3):
            block = ms_curr[i:i + 3]
            if len(block) == 3:
                Ms_level = self.T.learn(block[0], block[1], block[2])
                keyL = ("dyn_level", level_tag)
                self._reinforce(self._dyn, keyL, Ms_level)
        
        self._last_round_ms = ms_curr

    # === Ingesta de resultados ===
    def observe_transcender(self, result: Dict[str, Any], level_tag: str = "node"):
        """Ingiere resultado de Transcender.solve()"""
        M1, M2, M3, Ms = result["M1"], result["M2"], result["M3"], result["Ms"]
        self.observe_relator(Ms, result["wiring"], M1, M2, M3)
        self.observe_emergence(M1, M2, M3, Ms)
        
        # Coherencia
        if result.get("coherence"):
            coh = result["coherence"]
            keyC = ("coh_parent", tuple(norm3(coh["parent"])))
            marks = [
                1 if coh["totals"]["null_filled"] > 0 else 0,
                1 if coh["totals"]["conflict_resolved"] > 0 else 0,
                1 if coh["totals"]["kept_observed"] > 0 else 0,
            ]
            self._reinforce(self._emerg, keyC, marks)

    def observe_fractal(self, res: Dict[str, Any], level_name: str):
        """Ingiere FractalTranscender.synthesize()"""
        lvl_to_ms = {
            "lvl27": res["tensor_cross"].nivel_27,
            "lvl9": res["tensor_cross"].nivel_9,
            "lvl3": res["tensor_cross"].nivel_3,
        }
        
        for lvl, ms_list in lvl_to_ms.items():
            self.observe_dynamics_round(ms_list, level_tag=f"{level_name}:{lvl}")

    # === Consultas ===
    def relator_top(self, k: int = 5):
        """Top K relatores"""
        items = sorted(self._relator.values(), key=lambda p: (p.weight, p.count), reverse=True)
        return [{"key": p.key, "proto": p.proto, "w": round(p.weight, 3), "n": p.count} for p in items[:k]]

    def emergence_top(self, k: int = 5):
        """Top K emergencias"""
        items = sorted(self._emerg.values(), key=lambda p: (p.weight, p.count), reverse=True)
        return [{"key": p.key, "proto": p.proto, "w": round(p.weight, 3), "n": p.count} for p in items[:k]]

    def dynamics_top(self, k: int = 5):
        """Top K dinámicas"""
        items = sorted(self._dyn.values(), key=lambda p: (p.weight, p.count), reverse=True)
        return [{"key": p.key, "proto": p.proto, "w": round(p.weight, 3), "n": p.count} for p in items[:k]]

    # === Para Harmonizer y Extender ===
    def select_relator(self, tag: str, Ms_parent: List[Trit]) -> Optional[List[Tuple[str, str, str]]]:
        """Selecciona mejor wiring para un Ms padre"""
        Ms_parent = norm3(Ms_parent)
        best_wiring = None
        best_score = -1
        
        for key, proto in self._relator.items():
            if len(key) >= 2:
                stored_ms = key[0]
                if similarity3(list(stored_ms), Ms_parent) >= self.th:
                    if proto.weight > best_score:
                        best_score = proto.weight
                        best_wiring = key[1] if len(key) >= 2 else None
        
        return best_wiring

    def select_relator_k(self, tag: str, Ms: List[Trit], k: int = 3) -> List[Dict[str, Any]]:
        """Retorna k mejores relatores candidatos"""
        Ms = norm3(Ms)
        candidates = []
        
        for key, proto in self._relator.items():
            if len(key) >= 2:
                stored_ms = key[0]
                sim = similarity3(list(stored_ms), Ms)
                if sim >= self.th - 1:
                    candidates.append({
                        "proto": proto.proto,
                        "weight": proto.weight,
                        "count": proto.count,
                        "wiring": key[1] if len(key) >= 2 else None,
                        "similarity": sim
                    })
        
        candidates.sort(key=lambda c: c["weight"] * (c["similarity"] + 1), reverse=True)
        return candidates[:k]

    def suggest_repair(self, Ms: List[Trit], *, context: str = "unknown") -> List[Trit]:
        """Sugiere reparación para Ms con NULLs"""
        Ms = norm3(Ms)
        
        if all(x is not None for x in Ms):
            return Ms
        
        # Buscar mejor match
        best_match = None
        best_sim = -1
        
        for proto in self._emerg.values():
            sim = 0
            for i, (m, p) in enumerate(zip(Ms, proto.proto)):
                if m is not None and p is not None:
                    if m == p:
                        sim += 1
            
            if sim > best_sim:
                best_sim = sim
                best_match = proto.proto
        
        # Rellenar con patrón
        if best_match:
            return [m if m is not None else b for m, b in zip(Ms, best_match)]
        
        # Fallback
        return [m if m is not None else 0 for m in Ms]
