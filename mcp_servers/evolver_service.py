"""
MCP Service 5: evolver_service
Aprende arquetipos, relaciones y dinámicas del historial fractalizado
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from genesis_core import TurnRecord, CoherenceMetrics


class EvolverService:
    """
    Maestro de arquetipos: aprende patrones universales
    Separa: Archetype, Relator, Dynamics
    Timeout: 2s por batch
    """
    
    def __init__(self):
        self.timeout = 2.0
        self.archetypes = {}  # {pattern_key: {count, first_seen, last_seen, space_ids}}
        self.relations = []   # [{src, dst, type, strength}]
        self.dynamics = []    # [{timestamp, delta_Cdyn, trend}]
        self.update_count = 0
    
    def extract_archetype(self, turn: TurnRecord) -> Optional[str]:
        """
        Extrae patrón arquetípico desde un turno
        Usa Ms como firma del arquetipo
        """
        if turn.transcend is None:
            return None
        
        # Patrón = Ms serializado
        pattern_key = tuple(turn.transcend.Ms)
        return str(pattern_key)
    
    def update_archetypes(self, history_batch: List[Dict]) -> Dict:
        """
        Actualiza arquetipos con un batch de turnos
        
        Archetype = patrón común en distintos espacios lógicos
        """
        new_patterns = {}
        
        for turn_data in history_batch:
            if turn_data.get("transcend") is None:
                continue
            
            # Extraer patrón Ms
            ms = turn_data["transcend"]["Ms"]
            pattern_key = str(tuple(ms))
            space_id = turn_data.get("space_id", "default")
            
            # Actualizar contadores
            if pattern_key not in self.archetypes:
                self.archetypes[pattern_key] = {
                    "count": 0,
                    "first_seen": turn_data.get("timestamp", time.time()),
                    "last_seen": turn_data.get("timestamp", time.time()),
                    "space_ids": set(),
                    "Ms": ms
                }
            
            self.archetypes[pattern_key]["count"] += 1
            self.archetypes[pattern_key]["last_seen"] = turn_data.get("timestamp", time.time())
            self.archetypes[pattern_key]["space_ids"].add(space_id)
            
            if pattern_key not in new_patterns:
                new_patterns[pattern_key] = 0
            new_patterns[pattern_key] += 1
        
        # Identificar arquetipos universales (aparecen en múltiples espacios)
        universal_archetypes = {
            k: v for k, v in self.archetypes.items()
            if len(v["space_ids"]) >= 2  # Al menos 2 espacios
        }
        
        return {
            "new_patterns": len(new_patterns),
            "total_archetypes": len(self.archetypes),
            "universal_archetypes": len(universal_archetypes),
            "top_patterns": sorted(
                new_patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
    
    def extract_relations(self, history_batch: List[Dict]) -> Dict:
        """
        Relator: mapea relaciones fractales entre tensores
        
        Relación = transición entre tensores consecutivos
        """
        new_relations = []
        
        for i in range(len(history_batch) - 1):
            turn_current = history_batch[i]
            turn_next = history_batch[i + 1]
            
            if turn_current.get("user_ffe") and turn_next.get("user_ffe"):
                # Relación temporal: tensor(t) → tensor(t+1)
                relation = {
                    "src": turn_current["turn_id"],
                    "dst": turn_next["turn_id"],
                    "type": "temporal_sequence",
                    "strength": 1.0,
                    "timestamp": turn_current.get("timestamp", time.time())
                }
                new_relations.append(relation)
                self.relations.append(relation)
        
        return {
            "new_relations": len(new_relations),
            "total_relations": len(self.relations)
        }
    
    def update_dynamics(self, history_batch: List[Dict]) -> Dict:
        """
        Dynamics: cómo cambian las métricas de coherencia en el tiempo
        
        Detecta tendencias y estabilidad
        """
        c_dyn_values = []
        timestamps = []
        
        for turn_data in history_batch:
            coherence = turn_data.get("coherence")
            if coherence and "C_dyn" in coherence:
                c_dyn_values.append(coherence["C_dyn"])
                timestamps.append(turn_data.get("timestamp", time.time()))
        
        if len(c_dyn_values) < 2:
            return {
                "status": "insufficient_data",
                "min_required": 2
            }
        
        # Calcular delta promedio
        deltas = [c_dyn_values[i+1] - c_dyn_values[i] for i in range(len(c_dyn_values) - 1)]
        avg_delta = sum(deltas) / len(deltas)
        
        # Tendencia: mejorando/estable/degradando
        if avg_delta > 0.05:
            trend = "improving"
        elif avg_delta < -0.05:
            trend = "degrading"
        else:
            trend = "stable"
        
        # Guardar dinámica
        dynamic_entry = {
            "timestamp": timestamps[-1],
            "delta_Cdyn": avg_delta,
            "trend": trend,
            "n_samples": len(c_dyn_values)
        }
        self.dynamics.append(dynamic_entry)
        
        return {
            "delta_Cdyn": avg_delta,
            "trend": trend,
            "stability": 1.0 - abs(avg_delta),  # 1.0 = muy estable
            "total_dynamics": len(self.dynamics)
        }
    
    def update(self, history_batch: List[Dict]) -> Dict:
        """
        Endpoint MCP principal: actualiza arquetipos, relaciones, dinámicas
        
        Contract:
        Input: {"history_batch": [TurnRecord.to_dict(), ...]}
        Output: {
            "archetypes": {...},
            "relations": {...},
            "dynamics": {...},
            "status": str
        }
        """
        try:
            archetypes_result = self.update_archetypes(history_batch)
            relations_result = self.extract_relations(history_batch)
            dynamics_result = self.update_dynamics(history_batch)
            
            self.update_count += 1
            
            return {
                "archetypes": archetypes_result,
                "relations": relations_result,
                "dynamics": dynamics_result,
                "update_count": self.update_count,
                "status": "ok",
                "service": "evolver_v1"
            }
            
        except Exception as e:
            return {
                "archetypes": {},
                "relations": {},
                "dynamics": {},
                "status": "error",
                "error": str(e),
                "service": "evolver_v1"
            }
    
    def get_stats(self) -> Dict:
        """Estadísticas del Evolver"""
        return {
            "total_archetypes": len(self.archetypes),
            "total_relations": len(self.relations),
            "total_dynamics": len(self.dynamics),
            "update_count": self.update_count,
            "top_archetypes": sorted(
                [(k, v["count"]) for k, v in self.archetypes.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("EVOLVER SERVICE - Test")
    print("=" * 60)
    
    service = EvolverService()
    
    # Test 1: Update con batch simple
    print("\n[TEST 1] Update con batch de turnos...")
    history_batch = [
        {
            "turn_id": f"turn_{i}",
            "transcend": {
                "Ms": [0, 1, 0] if i % 2 == 0 else [1, 0, 1],
                "Ss": [1, 1, 0],
                "MetaM": [[1, 0, 1]] * 4
            },
            "space_id": "space_A" if i < 5 else "space_B",
            "coherence": {
                "C_meta": 0.95,
                "C_ext": 0.92,
                "C_dyn": 0.90 + i * 0.01
            },
            "timestamp": time.time() + i
        }
        for i in range(10)
    ]
    
    result = service.update(history_batch)
    print(f"✓ Status: {result['status']}")
    print(f"✓ Arquetipos nuevos: {result['archetypes']['new_patterns']}")
    print(f"✓ Total arquetipos: {result['archetypes']['total_archetypes']}")
    print(f"✓ Arquetipos universales: {result['archetypes']['universal_archetypes']}")
    print(f"✓ Relaciones nuevas: {result['relations']['new_relations']}")
    print(f"✓ Dinámica: trend={result['dynamics']['trend']}, delta={result['dynamics']['delta_Cdyn']:.4f}")
    
    # Test 2: Top patterns
    print("\n[TEST 2] Top patterns...")
    for pattern, count in result['archetypes']['top_patterns']:
        print(f"✓ {pattern}: {count} apariciones")
    
    # Test 3: Estadísticas
    print("\n[TEST 3] Estadísticas del Evolver...")
    stats = service.get_stats()
    print(f"✓ Total arquetipos: {stats['total_archetypes']}")
    print(f"✓ Total relaciones: {stats['total_relations']}")
    print(f"✓ Total dinámicas: {stats['total_dynamics']}")
    print(f"✓ Updates realizados: {stats['update_count']}")
    
    # Test 4: Arquetipos universales
    print("\n[TEST 4] Verificación de arquetipos universales...")
    universal = result['archetypes']['universal_archetypes']
    print(f"✓ Arquetipos en múltiples espacios: {universal}")
    assert universal >= 1, "Debe haber al menos 1 arquetipo universal"
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 60)
