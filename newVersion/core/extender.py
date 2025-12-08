"""
Extender - Reconstrucción top-down
Transcender invertido: dado Ms padre, reconstruye hijas
"""

from typing import List, Optional, Tuple, Dict, Any
from .trigate import Trit

def norm3(v: List[Trit]) -> List[Trit]:
    """Normaliza a 3 bits"""
    v = (list(v) + [0, 0, 0])[:3]
    return [None if x is None else (1 if x == 1 else 0) for x in v]


class Extender:
    """
    Reconstrucción top-down guiada por Ms padre.
    
    Usa:
      - Trigate para cierre triádico
      - Evolver para priors dinámicos y wirings
    """

    def __init__(self, trigate_cls, evolver):
        self.T = trigate_cls
        self.EV = evolver

    def _reconcile_bit(self, obs: Trit, ded: Trit, prefer_ded: bool = True) -> Tuple[Trit, Dict[str, int]]:
        """Reconcilia observado vs deducido"""
        stats = {"null_filled": 0, "conflict_resolved": 0, "kept_observed": 0}
        if obs is None and ded is not None:
            stats["null_filled"] += 1
            return ded, stats
        if obs is not None and ded is None:
            stats["kept_observed"] += 1
            return obs, stats
        if obs is not None and ded is not None and obs != ded:
            if prefer_ded:
                stats["conflict_resolved"] += 1
                return ded, stats
            else:
                stats["kept_observed"] += 1
                return obs, stats
        return obs, stats

    def _enforce_component(
        self,
        Ms_parent: List[Trit],
        M1: List[Trit],
        M2: List[Trit],
        M3: List[Trit]
    ) -> Tuple[List[Trit], List[Trit], List[Trit], Dict[str, int]]:
        """Coherencia absoluta para 3 hijas de un componente"""
        T = self.T
        M3_hat = T.infer(M1, M2, Ms_parent)
        M1_hat = T.infer(M2, M3, Ms_parent)
        M2_hat = T.infer(M3, M1, Ms_parent)

        rep = {"null_filled": 0, "conflict_resolved": 0, "kept_observed": 0}
        M1n, M2n, M3n = [], [], []
        
        for i in range(3):
            v, s = self._reconcile_bit(M1[i], M1_hat[i], True)
            M1n.append(v)
            for k in rep:
                rep[k] += s[k]
            
            v, s = self._reconcile_bit(M2[i], M2_hat[i], True)
            M2n.append(v)
            for k in rep:
                rep[k] += s[k]
            
            v, s = self._reconcile_bit(M3[i], M3_hat[i], True)
            M3n.append(v)
            for k in rep:
                rep[k] += s[k]
        
        return M1n, M2n, M3n, rep

    def _prior_child(self, d_tag: str) -> List[Trit]:
        """Obtiene prior dinámico del Evolver o NULL"""
        if not hasattr(self.EV, 'dynamics_top'):
            return [None, None, None]
        
        try:
            tops = self.EV.dynamics_top(1)
            if tops and len(tops) > 0:
                proto = tops[0].get("proto")
                if isinstance(proto, list) and len(proto) >= 3:
                    return norm3(proto)
        except Exception:
            pass
        
        return [None, None, None]

    def extend_component(
        self,
        Ms_parent: List[Trit],
        *,
        seeds: List[List[Trit]] = None
    ) -> Dict[str, Any]:
        """Reconstruye 3 hijas Ms para un componente"""
        Ms_parent = norm3(Ms_parent)
        seeds = seeds or [[None, None, None], [None, None, None], [None, None, None]]

        # Wiring sugerido
        wiring = None
        if hasattr(self.EV, "select_relator"):
            wiring = self.EV.select_relator("comp", Ms_parent)

        # Inicializar hijas
        M1, M2, M3 = [norm3(seeds[i]) for i in range(3)]
        need_prior = [all(x is None for x in M1), all(x is None for x in M2), all(x is None for x in M3)]
        
        if any(need_prior):
            prior = self._prior_child("comp")
            if need_prior[0]:
                M1 = prior[:]
            if need_prior[1]:
                M2 = prior[:]
            if need_prior[2]:
                M3 = prior[:]

        # Coherencia absoluta
        M1c, M2c, M3c, rep = self._enforce_component(Ms_parent, M1, M2, M3)

        return {
            "Ms_parent": Ms_parent,
            "children": {"M1": M1c, "M2": M2c, "M3": M3c},
            "wiring_hint": wiring,
            "coherence_stats": rep
        }

    def extend_triplet(
        self,
        Ms_triplet_parent: Tuple[List[Trit], List[Trit], List[Trit]],
        *,
        seeds_triplet: Tuple[List[List[Trit]], List[List[Trit]], List[List[Trit]]] = None
    ) -> Dict[str, Any]:
        """Reconstruye tripleta de hijas (x,y,z) para un nodo"""
        (Msx, Msy, Msz) = Ms_triplet_parent
        seeds_triplet = seeds_triplet or (None, None, None)

        rx = self.extend_component(Msx, seeds=seeds_triplet[0] or None)
        ry = self.extend_component(Msy, seeds=seeds_triplet[1] or None)
        rz = self.extend_component(Msz, seeds=seeds_triplet[2] or None)

        return {
            "parent": {"Msx": norm3(Msx), "Msy": norm3(Msy), "Msz": norm3(Msz)},
            "children": {
                "x": rx["children"],
                "y": ry["children"],
                "z": rz["children"]
            },
            "coherence": {
                "x": rx["coherence_stats"],
                "y": ry["coherence_stats"],
                "z": rz["coherence_stats"]
            },
            "wiring_hints": {
                "x": rx["wiring_hint"],
                "y": ry["wiring_hint"],
                "z": rz["wiring_hint"]
            }
        }
