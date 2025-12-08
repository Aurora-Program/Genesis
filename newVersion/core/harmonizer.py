"""
Harmonizer - Reparación de incoherencias mediante 5 escalones
Estrategia autosimilar de resolución de conflictos
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from .trigate import Trit

Tripleta = Tuple[List[Trit], List[Trit], List[Trit]]  # (M1,M2,M3) de un componente

def norm3(v: List[Trit]) -> List[Trit]:
    v = (list(v) + [0, 0, 0])[:3]
    return [None if x is None else (1 if x == 1 else 0) for x in v]

def similarity3(a: List[Trit], b: List[Trit]) -> int:
    s = 0
    for x, y in zip(a, b):
        if x is None or y is None:
            continue
        if x == y:
            s += 1
    return s

def rotate3(v: List[Trit], s: int) -> List[Trit]:
    s %= 3
    return v[-s:] + v[:-s] if s else v


@dataclass
class HarmonyResult:
    """Resultado de armonización"""
    result: Dict[str, Any]  # Estado reparado
    audit: List[Dict[str, Any]]  # Pasos ejecutados
    repaired: bool
    escalated: bool = False


class Harmonizer:
    """
    Reparación escalonada de incoherencias.
    
    5 niveles (de suave a profundo):
      1. Soft: re-rotación Fibonacci de semillas
      2. Contextual: Extender top-down con Ss y dinámica
      3. Local: micro-ajuste bit a bit con Trigate
      4. Estructural: cambiar relator (wiring alternativo)
      5. Arquetípico: escalar (nuevo arquetipo en Evolver)
    """

    def __init__(
        self,
        trigate_cls,
        evolver,
        extender_cls,
        max_conflicts: int = 0,
        max_null_fills: int = 3,
        min_child_sim: int = 6
    ):
        self.T = trigate_cls
        self.EV = evolver
        self.EXT = extender_cls(trigate_cls, evolver)

        # Umbrales
        self.max_conflicts = max_conflicts
        self.max_null_fills = max_null_fills
        self.min_child_sim = min_child_sim

    def _coh_stats_ok(self, coh: Dict[str, int]) -> bool:
        """Verifica si coherencia cumple umbrales"""
        return (
            coh.get("conflict_resolved", 999) <= self.max_conflicts
            and coh.get("null_filled", 999) <= self.max_null_fills
        )

    def _score_tripleta(self, trip: Tripleta) -> int:
        """Cuenta bits definidos en tripleta"""
        return sum(0 if b is None else 1 for comp in trip for b in comp)

    def _soft_rerotate_seeds(
        self,
        seeds_trip: Tuple[Tripleta, Tripleta, Tripleta],
        Ss_trip: Dict[str, List[Trit]] = None
    ) -> Tuple[Tripleta, Tripleta, Tripleta]:
        """1. Soft: re-rotación Fibonacci de semillas"""
        def score_defined(trio: Tripleta) -> int:
            return sum(0 if b is None else 1 for comp in trio for b in comp)

        def best_rot_of(trio: Tripleta, Ss_d: List[Trit] = None) -> Tripleta:
            M1, M2, M3 = trio
            cands = [(rotate3(M1, s), rotate3(M2, s), rotate3(M3, s)) for s in (0, 1, 2)]
            if Ss_d is None:
                return max(cands, key=score_defined)
            return max(cands, key=lambda t: sum(similarity3(t[i], Ss_d) for i in range(3)))

        tags = ["x", "y", "z"]
        out = tuple(
            best_rot_of(trio, (Ss_trip or {}).get(tag))
            for tag, trio in zip(tags, seeds_trip)
        )
        return out

    def _micro_adjust(
        self,
        Ms_parent: List[Trit],
        trio: Tripleta
    ) -> Tuple[Tripleta, Dict[str, int]]:
        """3. Local: micro-ajuste con Trigate"""
        M1, M2, M3 = [norm3(x) for x in trio]
        R3 = self.T.infer(M1, M2, norm3(Ms_parent))
        R1 = self.T.infer(M2, M3, norm3(Ms_parent))
        R2 = self.T.infer(M3, M1, norm3(Ms_parent))

        def blend(obs: List[Trit], ded: List[Trit]) -> List[Trit]:
            """Prioriza deducido"""
            return [ded[i] if obs[i] is None else obs[i] if ded[i] is None else ded[i]
                    for i in range(len(obs))]

        M1n, M2n, M3n = blend(M1, R1), blend(M2, R2), blend(M3, R3)

        # Stats
        stats = {"null_filled": 0, "conflict_resolved": 0}
        for (orig, ded) in ((M1, R1), (M2, R2), (M3, R3)):
            for o, d in zip(orig, ded):
                if o is None and d is not None:
                    stats["null_filled"] += 1
                elif o is not None and d is not None and o != d:
                    stats["conflict_resolved"] += 1

        return (M1n, M2n, M3n), stats

    def harmonize_from_state(
        self,
        *,
        Ms_parent_triplet: Tripleta,
        children_observed: Dict[str, Tripleta],
        context_Ss: Dict[str, List[Trit]] = None
    ) -> HarmonyResult:
        """
        Armonización principal con 5 escalones.
        
        Returns:
            HarmonyResult con estado reparado y auditoría completa
        """
        audit: List[Dict[str, Any]] = []
        Msx, Msy, Msz = [norm3(c) for c in Ms_parent_triplet]
        seeds_x, seeds_y, seeds_z = (
            children_observed["x"],
            children_observed["y"],
            children_observed["z"]
        )

        # === 1) SOFT: re-rotación ===
        seeds_rot = self._soft_rerotate_seeds(
            (seeds_x, seeds_y, seeds_z), Ss_trip=context_Ss
        )
        audit.append({
            "step": "1_soft_rerotate",
            "defined_bits": sum(self._score_tripleta(s) for s in seeds_rot),
            "ctx_present": bool(context_Ss)
        })

        # === 2) CONTEXTUAL: Extender ===
        res_ext = self.EXT.extend_triplet((Msx, Msy, Msz), seeds_triplet=seeds_rot)
        coh = res_ext.get("coherence", {})
        audit.append({
            "step": "2_contextual_extend",
            "coherence": coh,
            "wiring_hints": res_ext.get("wiring_hints")
        })

        children_ctx = res_ext["children"]
        trip_x = (children_ctx["x"]["M1"], children_ctx["x"]["M2"], children_ctx["x"]["M3"])
        trip_y = (children_ctx["y"]["M1"], children_ctx["y"]["M2"], children_ctx["y"]["M3"])
        trip_z = (children_ctx["z"]["M1"], children_ctx["z"]["M2"], children_ctx["z"]["M3"])

        if coh and all(self._coh_stats_ok(coh[d]) for d in coh):
            return HarmonyResult(
                result={
                    "parent": {"Msx": Msx, "Msy": Msy, "Msz": Msz},
                    "children": {"x": trip_x, "y": trip_y, "z": trip_z}
                },
                audit=audit,
                repaired=True
            )

        # === 3) LOCAL: micro-ajuste ===
        (trip_x_adj, stats_x) = self._micro_adjust(Msx, trip_x)
        (trip_y_adj, stats_y) = self._micro_adjust(Msy, trip_y)
        (trip_z_adj, stats_z) = self._micro_adjust(Msz, trip_z)

        sim_gain = (
            sum(similarity3(a, b) for a, b in zip(trip_x, trip_x_adj))
            + sum(similarity3(a, b) for a, b in zip(trip_y, trip_y_adj))
            + sum(similarity3(a, b) for a, b in zip(trip_z, trip_z_adj))
        )
        audit.append({
            "step": "3_local_micro_adjust",
            "similarity_gain_bits": sim_gain,
            "local_stats": {"x": stats_x, "y": stats_y, "z": stats_z}
        })

        if sim_gain >= self.min_child_sim:
            return HarmonyResult(
                result={
                    "parent": {"Msx": Msx, "Msy": Msy, "Msz": Msz},
                    "children": {"x": trip_x_adj, "y": trip_y_adj, "z": trip_z_adj}
                },
                audit=audit,
                repaired=True
            )

        # === 4) ESTRUCTURAL: relator alternativo ===
        alt_hints = {}
        if hasattr(self.EV, "select_relator_k"):
            for tag, Ms in (("x", Msx), ("y", Msy), ("z", Msz)):
                alts = self.EV.select_relator_k(tag, Ms, k=2)
                alt_hints[tag] = alts[1] if len(alts) > 1 else None
        audit.append({"step": "4_structural_alt_relator", "alt_hints": alt_hints})

        res_ext2 = self.EXT.extend_triplet(
            (Msx, Msy, Msz),
            seeds_triplet=(trip_x_adj, trip_y_adj, trip_z_adj)
        )
        coh2 = res_ext2.get("coherence", {})
        audit.append({"step": "4_structural_reextend", "coherence": coh2})

        if coh2 and all(self._coh_stats_ok(coh2[d]) for d in coh2):
            ch2 = res_ext2["children"]
            return HarmonyResult(
                result={
                    "parent": {"Msx": Msx, "Msy": Msy, "Msz": Msz},
                    "children": {
                        "x": (ch2["x"]["M1"], ch2["x"]["M2"], ch2["x"]["M3"]),
                        "y": (ch2["y"]["M1"], ch2["y"]["M2"], ch2["y"]["M3"]),
                        "z": (ch2["z"]["M1"], ch2["z"]["M2"], ch2["z"]["M3"])
                    }
                },
                audit=audit,
                repaired=True
            )

        # === 5) ARQUETÍPICO: escalar ===
        incoherent = {
            "parent": {"Msx": Msx, "Msy": Msy, "Msz": Msz},
            "children": {"x": trip_x_adj, "y": trip_y_adj, "z": trip_z_adj}
        }
        audit.append({"step": "5_archetypic_escalate"})

        return HarmonyResult(
            result=incoherent,
            audit=audit,
            repaired=True,
            escalated=True
        )
