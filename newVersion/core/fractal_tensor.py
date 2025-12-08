"""
FractalTensor - Representación jerárquica 3-9-27
Estructura fractal autosimilar con 3 niveles
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from .trigate import Trit
from .transcender import Transcender, norm3

@dataclass
class FractalTensor:
    """
    Tensor fractal 3-9-27.
    Cada celda es un vector ternario de 3 bits.
    """
    nivel_3: List[List[Trit]]   # len = 3
    nivel_9: List[List[Trit]]   # len = 9
    nivel_27: List[List[Trit]]  # len = 27

    @staticmethod
    def neutral() -> "FractalTensor":
        """Crea tensor neutro (todos ceros)"""
        z = [[0, 0, 0]]
        return FractalTensor(nivel_3=z * 3, nivel_9=z * 9, nivel_27=z * 27)

    def normalize(self):
        """Normaliza todos los vectores"""
        self.nivel_3 = [norm3(v) for v in self.nivel_3]
        self.nivel_9 = [norm3(v) for v in self.nivel_9]
        self.nivel_27 = [norm3(v) for v in self.nivel_27]
        return self

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el tensor a diccionario para serialización.
        
        Returns:
            Dict con 'nivel_3', 'nivel_9', 'nivel_27'
        """
        return {
            'nivel_3': [list(v) for v in self.nivel_3],
            'nivel_9': [list(v) for v in self.nivel_9],
            'nivel_27': [list(v) for v in self.nivel_27]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FractalTensor":
        """
        Crea tensor desde diccionario.
        
        Args:
            data: Dict con 'nivel_3', 'nivel_9', 'nivel_27'
        
        Returns:
            FractalTensor
        """
        return FractalTensor(
            nivel_3=data.get('nivel_3', [[0, 0, 0]] * 3),
            nivel_9=data.get('nivel_9', [[0, 0, 0]] * 9),
            nivel_27=data.get('nivel_27', [[0, 0, 0]] * 27)
        )

    def __repr__(self) -> str:
        """Representación legible"""
        def format_vec(v):
            return '[' + ','.join('·' if x is None else str(x) for x in v) + ']'

        lines = [
            "FractalTensor(",
            f"  nivel_3:  {[format_vec(v) for v in self.nivel_3]}",
            f"  nivel_9:  {[format_vec(v) for v in self.nivel_9[:3]]} + {len(self.nivel_9) - 3} more",
            f"  nivel_27: {[format_vec(v) for v in self.nivel_27[:3]]} + {len(self.nivel_27) - 3} more",
            ")"
        ]
        return '\n'.join(lines)


class FractalTranscender:
    """
    Orquesta síntesis fractal 27→9→3 sobre (A,B,C).
    
    Realiza dos tipos de síntesis:
      1. Cross-level: Compara A vs B vs C en cada nivel
      2. Self-synthesis: Sintetiza internamente cada tensor (27→9→3)
    
    Resultado: FractalTensor con Ms cruzadas + auditorías + locals
    """

    def __init__(self, transcender_cls):
        self.TX = transcender_cls

    @staticmethod
    def child_triplet_indices(parent_idx: int) -> Tuple[int, int, int]:
        """Índices de los 3 hijos de un padre"""
        base = 3 * parent_idx
        return base, base + 1, base + 2

    def _cross_level(
        self,
        A_vecs: List[List[Trit]],
        B_vecs: List[List[Trit]],
        C_vecs: List[List[Trit]],
        transcender
    ) -> Tuple[List[List[Trit]], List[List[Trit]], List[Dict[str, Any]]]:
        """Comparación cruzada A vs B vs C en un nivel"""
        Ms_list, Ss_list, audit = [], [], []
        for i in range(len(A_vecs)):
            res = transcender.solve(A_vecs[i], B_vecs[i], C_vecs[i], max_tries=3, check_reconstruction=True)
            Ms_list.append(norm3(res["Ms"]))
            Ss_list.append(norm3(res["Ss"]))
            audit.append({
                "MetaM": res["MetaM"],
                "wiring": res["wiring"],
                "score": res["score"],
                "reconstruction_ok": res["reconstruction_ok"]
            })
        return Ms_list, Ss_list, audit

    def _self_synthesize_up(
        self,
        child_vecs: List[List[Trit]],
        transcender
    ) -> List[List[Trit]]:
        """Auto-síntesis intra-tensor: cada 3 hijos → 1 padre Ms local"""
        assert len(child_vecs) % 3 == 0
        parents = []
        for p in range(len(child_vecs) // 3):
            i0, i1, i2 = self.child_triplet_indices(p)
            res = transcender.solve(child_vecs[i0], child_vecs[i1], child_vecs[i2], max_tries=3, check_reconstruction=False)
            parents.append(norm3(res["Ms"]))
        return parents

    def synthesize(
        self,
        A: FractalTensor,
        B: FractalTensor,
        C: FractalTensor,
        transcender
    ) -> Dict[str, Any]:
        """
        Síntesis fractal completa.
        
        Returns:
          - tensor_cross: FractalTensor con Ms cruzadas
          - Ss: Síntesis factuales por nivel
          - audits: Auditorías por nivel y nodo
          - locals: Ms locales de auto-síntesis A,B,C
        """
        A.normalize()
        B.normalize()
        C.normalize()

        audits = {"lvl27": [], "lvl9": [], "lvl3": []}
        localsynth = {"A": {}, "B": {}, "C": {}}

        # === Nivel 27: cross + auto-síntesis 27→9 ===
        Ms27, Ss27, audit27 = self._cross_level(A.nivel_27, B.nivel_27, C.nivel_27, transcender)
        audits["lvl27"] = audit27

        A9_local = self._self_synthesize_up(A.nivel_27, transcender)
        B9_local = self._self_synthesize_up(B.nivel_27, transcender)
        C9_local = self._self_synthesize_up(C.nivel_27, transcender)
        localsynth["A"]["lvl9"] = A9_local
        localsynth["B"]["lvl9"] = B9_local
        localsynth["C"]["lvl9"] = C9_local

        # === Nivel 9: cross + auto-síntesis 9→3 ===
        Ms9, Ss9, audit9 = self._cross_level(A9_local, B9_local, C9_local, transcender)
        audits["lvl9"] = audit9

        A3_local = self._self_synthesize_up(A9_local, transcender)
        B3_local = self._self_synthesize_up(B9_local, transcender)
        C3_local = self._self_synthesize_up(C9_local, transcender)
        localsynth["A"]["lvl3"] = A3_local
        localsynth["B"]["lvl3"] = B3_local
        localsynth["C"]["lvl3"] = C3_local

        # === Nivel 3: cross final ===
        Ms3, Ss3, audit3 = self._cross_level(A3_local, B3_local, C3_local, transcender)
        audits["lvl3"] = audit3

        # Tensor resultado (Ms cruzadas)
        tensor_cross = FractalTensor(
            nivel_3=Ms3,
            nivel_9=Ms9,
            nivel_27=Ms27
        ).normalize()

        # Ss por nivel
        Ss = {"lvl27": Ss27, "lvl9": Ss9, "lvl3": Ss3}

        return {
            "tensor_cross": tensor_cross,
            "Ss": Ss,
            "audits": audits,
            "locals": localsynth
        }
