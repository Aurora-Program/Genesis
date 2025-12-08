"""
Aurora Pipeline - Coordinador central del sistema Genesis
Orquesta el ciclo completo: Ingesta → Síntesis → Aprendizaje → Armonización
"""

from typing import List, Optional, Dict, Any, Tuple
import json
import sys
from pathlib import Path

# Agregar parent dir para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.trigate import Trigate, Trit
from core.transcender import Transcender
from core.evolver import Evolver3
from core.extender import Extender
from core.harmonizer import Harmonizer
from core.fractal_tensor import FractalTensor, FractalTranscender


class KnowledgeBase:
    """
    Knowledge Base mínima en memoria.
    Almacena resultados y alimenta automáticamente al Evolver.
    """

    def __init__(self, evolver: Evolver3):
        self.evolver = evolver
        self.patterns = {}  # key -> data completa
        self.by_ms = {}     # Ms_str -> [keys]
        self.stats = {
            "total_stored": 0,
            "total_harmonized": 0,
            "total_escalated": 0
        }

    def store(self, key: str, data: Dict[str, Any], tag: str = "default"):
        """Almacena resultado y alimenta al Evolver"""
        self.patterns[key] = {
            "data": data,
            "tag": tag,
            "harmonized": data.get("harmony_applied", False),
            "escalated": data.get("harmony_escalated", False)
        }

        # Indexar por Ms
        if "tensor_cross" in data:
            tensor = data["tensor_cross"]
            ms_key = self._ms_to_key(tensor.nivel_3)
            if ms_key not in self.by_ms:
                self.by_ms[ms_key] = []
            self.by_ms[ms_key].append(key)

        # Alimentar Evolver
        if "audits" in data:
            self.evolver.observe_fractal(data, tag)  # Usando positional arg como en core.py original

        # Stats
        self.stats["total_stored"] += 1
        if data.get("harmony_applied"):
            self.stats["total_harmonized"] += 1
        if data.get("harmony_escalated"):
            self.stats["total_escalated"] += 1

    def retrieve(self, key: str) -> Optional[Dict]:
        """Recupera por clave exacta"""
        entry = self.patterns.get(key)
        return entry["data"] if entry else None

    def query_by_ms(self, ms_vector: List[List[Trit]]) -> List[Dict]:
        """Recupera patrones con Ms similar"""
        ms_key = self._ms_to_key(ms_vector)
        keys = self.by_ms.get(ms_key, [])
        return [self.patterns[k]["data"] for k in keys]

    def get_stats(self) -> Dict:
        """Estadísticas de la KB"""
        return {
            **self.stats,
            "unique_ms": len(self.by_ms),
            "evolver_relators": len(self.evolver._relator),
            "evolver_emergences": len(self.evolver._emerg),
            "evolver_dynamics": len(self.evolver._dyn)
        }

    @staticmethod
    def _ms_to_key(ms_vector: List[List[Trit]]) -> str:
        """Convierte Ms a string para indexación"""
        return str([[x if x is not None else -1 for x in v] for v in ms_vector])


class FractalEvolver:
    """
    Evolucionador fractal con reparación automática.
    Ejecuta síntesis 27→9→3 y aplica Harmonizer post-síntesis.
    """

    def __init__(self, transcender_cls, trigate_cls, evolver, extender_cls, harmonizer_cls=None):
        self.trigate_cls = trigate_cls
        self.transcender_core = transcender_cls(trigate_cls)
        self.fractal_tx = FractalTranscender(transcender_cls)
        self.evolver = evolver
        self.extender = extender_cls(trigate_cls, evolver)
        self.harmonizer = harmonizer_cls(trigate_cls, evolver, extender_cls) if harmonizer_cls else None

    def synthesize_with_harmony(
        self,
        A: FractalTensor,
        B: FractalTensor,
        C: FractalTensor,
        apply_harmony: bool = True
    ) -> Dict[str, Any]:
        """Síntesis fractal completa con armonización opcional"""
        # 1. Síntesis base
        result = self.fractal_tx.synthesize(A, B, C, self.transcender_core)

        tensor = result["tensor_cross"]
        audits = result["audits"]
        Ss = result["Ss"]

        # 2. Harmonizer
        harmony_applied = False
        harmony_escalated = False
        harmony_audit = []

        if apply_harmony and self.harmonizer:
            Ms_triplet = (tensor.nivel_3[0], tensor.nivel_3[1], tensor.nivel_3[2])
            children_observed = {
                "x": (A.nivel_3[0], A.nivel_3[1], A.nivel_3[2]),
                "y": (B.nivel_3[0], B.nivel_3[1], B.nivel_3[2]),
                "z": (C.nivel_3[0], C.nivel_3[1], C.nivel_3[2])
            }

            context_Ss = {}
            if Ss and "lvl3" in Ss and len(Ss["lvl3"]) >= 3:
                context_Ss = {
                    "x": Ss["lvl3"][0],
                    "y": Ss["lvl3"][1],
                    "z": Ss["lvl3"][2]
                }

            harmony = self.harmonizer.harmonize_from_state(
                Ms_parent_triplet=Ms_triplet,
                children_observed=children_observed,
                context_Ss=context_Ss
            )

            if harmony.repaired:
                harmony_applied = True
                harmony_escalated = harmony.escalated
                harmony_audit = harmony.audit

                # Actualizar tensor
                children = harmony.result["children"]
                tensor.nivel_3 = [children["x"][0], children["y"][0], children["z"][0]]

                if "lvl3" in audits and len(audits["lvl3"]) > 0:
                    audits["lvl3"][0]["harmony"] = {
                        "applied": True,
                        "escalated": harmony_escalated,
                        "steps": len(harmony_audit)
                    }

        return {
            "tensor_cross": tensor,
            "Ss": Ss,
            "audits": audits,
            "locals": result.get("locals", {}),
            "harmony_applied": harmony_applied,
            "harmony_audit": harmony_audit,
            "harmony_escalated": harmony_escalated
        }


class AuroraPipeline:
    """
    Coordinador central del sistema Aurora.
    
    Flujo:
      1. Inicializa todos los módulos core
      2. Procesa inputs → FractalTensors
      3. Ejecuta síntesis fractal con armonización
      4. Almacena en KB (alimenta Evolver automáticamente)
    """

    def __init__(self, enable_harmony: bool = True, verbose: bool = True):
        self.verbose = verbose
        self.enable_harmony = enable_harmony

        if self.verbose:
            print("🌅 Inicializando Aurora Pipeline...")

        # Módulos core
        self.trigate_cls = Trigate
        if self.verbose:
            print("  ✅ Trigate (LUTs ternarias)")

        self.evolver = Evolver3(Trigate, th_match=2, decay=0.9)
        if self.verbose:
            print("  ✅ Evolver3 (RELATOR + EMERGENCIA + DINÁMICA)")

        self.transcender_cls = Transcender
        self.transcender = Transcender(Trigate)
        if self.verbose:
            print("  ✅ Transcender (síntesis jerárquica)")

        self.extender_cls = Extender
        self.extender = Extender(Trigate, self.evolver)
        if self.verbose:
            print("  ✅ Extender (reconstrucción top-down)")

        self.harmonizer_cls = Harmonizer if enable_harmony else None
        self.harmonizer = Harmonizer(Trigate, self.evolver, Extender) if enable_harmony else None
        if self.verbose:
            if enable_harmony:
                print("  ✅ Harmonizer (reparación 5 niveles)")
            else:
                print("  ⚠️  Harmonizer deshabilitado")

        self.fractal_evolver = FractalEvolver(
            transcender_cls=Transcender,
            trigate_cls=Trigate,
            evolver=self.evolver,
            extender_cls=Extender,
            harmonizer_cls=Harmonizer if enable_harmony else None
        )
        if self.verbose:
            print("  ✅ FractalEvolver (síntesis + armonización)")

        self.kb = KnowledgeBase(self.evolver)
        if self.verbose:
            print("  ✅ KnowledgeBase (almacenamiento)")

        if self.verbose:
            print("\n✨ Aurora Pipeline listo\n")

    def process_input(
        self,
        data_A: List[List[Trit]],
        data_B: List[List[Trit]],
        data_C: List[List[Trit]]
    ) -> Tuple[FractalTensor, FractalTensor, FractalTensor]:
        """Convierte datos crudos en FractalTensors"""
        def ensure_27(data: List[List[Trit]]) -> List[List[Trit]]:
            data = list(data)
            while len(data) < 27:
                data.append([0, 0, 0])
            return data[:27]

        data_A = ensure_27(data_A)
        data_B = ensure_27(data_B)
        data_C = ensure_27(data_C)

        tensor_A = FractalTensor(
            nivel_27=data_A,
            nivel_9=data_A[:9],
            nivel_3=data_A[:3]
        ).normalize()

        tensor_B = FractalTensor(
            nivel_27=data_B,
            nivel_9=data_B[:9],
            nivel_3=data_B[:3]
        ).normalize()

        tensor_C = FractalTensor(
            nivel_27=data_C,
            nivel_9=data_C[:9],
            nivel_3=data_C[:3]
        ).normalize()

        return tensor_A, tensor_B, tensor_C

    def run_cycle(
        self,
        data_A: List[List[Trit]],
        data_B: List[List[Trit]],
        data_C: List[List[Trit]],
        tag: str = "default"
    ) -> Dict[str, Any]:
        """Ejecuta ciclo completo: Ingesta → Síntesis → Aprendizaje → Storage"""
        if self.verbose:
            print(f"🔄 Ejecutando ciclo (tag: {tag})...")

        # 1. Procesar
        tensor_A, tensor_B, tensor_C = self.process_input(data_A, data_B, data_C)
        if self.verbose:
            print("  ✓ Inputs → FractalTensors")

        # 2. Síntesis + Armonización
        result = self.fractal_evolver.synthesize_with_harmony(
            tensor_A, tensor_B, tensor_C,
            apply_harmony=self.enable_harmony
        )
        if self.verbose:
            print("  ✓ Síntesis fractal ejecutada")
            if result["harmony_applied"]:
                print(f"    🔧 Harmonizer ({len(result['harmony_audit'])} pasos)")
                if result["harmony_escalated"]:
                    print("    ⚠️  Escalado a arquetipo")

        # 3. Storage
        key = f"{tag}_{hash((str(data_A), str(data_B), str(data_C)))}"
        self.kb.store(key, result, tag)
        if self.verbose:
            print("  ✓ Almacenado en KB")

        # 4. Stats
        if self.verbose:
            stats = self.kb.get_stats()
            print(f"\n📊 Stats: {stats['total_stored']} almacenados, "
                  f"{stats['total_harmonized']} armonizados, "
                  f"{stats['total_escalated']} escalados")

        return result

    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas completas del sistema"""
        return {
            "kb": self.kb.get_stats(),
            "harmony_enabled": self.enable_harmony
        }
