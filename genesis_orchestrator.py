"""
Genesis Orchestrator: Orquestador del pipeline MCP completo
Integra los 5 microservicios: probe_llm → ffe_encoder → transcender → ffe_store → evolver
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import time

# Add mcp_servers to path
sys.path.insert(0, str(Path(__file__).parent / "mcp_servers"))
sys.path.insert(0, str(Path(__file__).parent))

from mcp_servers.probe_llm_service import ProbeLLMService
from mcp_servers.ffe_encoder_service import FFEEncoderService
from mcp_servers.transcender_service import TranscenderService
from mcp_servers.ffe_store import FFEStore
from mcp_servers.evolver_service import EvolverService
from genesis_core import TurnRecord, FFETensor, CoherenceMetrics


class GenesisOrchestrator:
    """
    Orquestador principal del Proyecto Genesis
    Coordina el flujo: texto → embedding → FFE → síntesis → KB → evolución
    """
    
    def __init__(self, db_path: str = "data/genesis_kb.db"):
        # Inicializar servicios
        self.probe_llm = ProbeLLMService()
        self.ffe_encoder = FFEEncoderService()
        self.transcender = TranscenderService()
        self.ffe_store = FFEStore(db_path)
        self.evolver = EvolverService()
        
        # Contadores
        self.turn_count = 0
        self.session_id = f"session_{int(time.time())}"
    
    def text_to_ffe(self, text: str) -> Optional[Dict]:
        """
        Pipeline: texto → embedding → FFE
        
        Returns: {"ffe_tensor": {...}, "metadata": {...}}
        """
        # Paso 1: Probe LLM
        probe_result = self.probe_llm.probe(text)
        if probe_result["status"] != "ok":
            return None
        
        # Paso 2: FFE Encoder
        encode_result = self.ffe_encoder.encode(probe_result["embedding"])
        if encode_result["status"] != "ok":
            return None
        
        return {
            "ffe_tensor": encode_result["ffe_tensor"],
            "metadata": probe_result["metadata"]
        }
    
    def process_conversation_turn(
        self,
        user_text: str,
        model_text: str,
        space_id: str = "default"
    ) -> Dict:
        """
        Procesa un turno completo de conversación fractalizada
        
        Flujo:
        1. Texto → FFE (user y model)
        2. Síntesis emergente (Transcender)
        3. Almacenamiento (FFE Store)
        4. Evolución (Evolver)
        5. Métricas de coherencia
        
        Returns: TurnRecord completo con todas las etapas
        """
        start_time = time.time()
        
        # Paso 1: Convertir textos a FFE
        user_ffe_data = self.text_to_ffe(user_text)
        model_ffe_data = self.text_to_ffe(model_text)
        
        if not user_ffe_data or not model_ffe_data:
            return {
                "status": "error",
                "error": "Failed to encode text to FFE",
                "turn_count": self.turn_count
            }
        
        # Paso 2: Síntesis emergente
        synthesis_result = self.transcender.synthesize_conversation(
            user_ffe_data["ffe_tensor"],
            model_ffe_data["ffe_tensor"]
        )
        
        if synthesis_result["status"] != "ok":
            return {
                "status": "error",
                "error": "Synthesis failed",
                "turn_count": self.turn_count
            }
        
        # Paso 3: Calcular coherencia extendida
        # C_ext = mock (en producción usar Extender real)
        c_ext = 0.95  # Placeholder
        # C_dyn = basado en historial (mock por ahora)
        c_dyn = 0.92 + (self.turn_count % 10) * 0.01
        
        coherence = CoherenceMetrics(
            C_meta=synthesis_result["C_meta"],
            C_ext=c_ext,
            C_dyn=c_dyn
        )
        
        # Paso 4: Crear TurnRecord
        turn_record = TurnRecord(
            user_ffe=FFETensor.from_flat(user_ffe_data["ffe_tensor"]["flat"]),
            model_ffe=FFETensor.from_flat(model_ffe_data["ffe_tensor"]["flat"]),
            transcend=None,  # Simplificado por ahora
            space_id=space_id,
            coherence=coherence
        )
        
        # Paso 5: Almacenar en KB
        turn_dict = turn_record.to_dict()
        turn_dict["transcend"] = {
            "Ms": synthesis_result["Ms"],
            "Ss": synthesis_result["Ss"],
            "MetaM": synthesis_result["MetaM"]
        }
        turn_dict["user_text"] = user_text
        turn_dict["model_text"] = model_text
        
        tensor_id = self.ffe_store.store_tensor(
            turn_dict,
            synthesis_result,
            {"session_id": self.session_id, "turn": self.turn_count}
        )
        
        # Paso 6: Evolución (cada 5 turnos)
        evolution_result = None
        if self.turn_count % 5 == 0 and self.turn_count > 0:
            recent_turns = self.ffe_store.query_recent(10)
            if recent_turns:
                evolution_result = self.evolver.update([t for t in recent_turns])
        
        self.turn_count += 1
        elapsed = time.time() - start_time
        
        return {
            "status": "ok",
            "turn_id": turn_record.turn_id,
            "tensor_id": tensor_id,
            "space_id": space_id,
            "synthesis": {
                "Ms": synthesis_result["Ms"],
                "Ss": synthesis_result["Ss"],
                "hash": synthesis_result["hash"]
            },
            "coherence": {
                "C_meta": coherence.C_meta,
                "C_ext": coherence.C_ext,
                "C_dyn": coherence.C_dyn,
                "is_coherent": coherence.is_coherent()
            },
            "evolution": evolution_result,
            "turn_count": self.turn_count,
            "elapsed_ms": int(elapsed * 1000),
            "session_id": self.session_id
        }
    
    def get_stats(self) -> Dict:
        """Estadísticas globales del sistema"""
        kb_stats = self.ffe_store.get_stats()
        evolver_stats = self.evolver.get_stats()
        
        return {
            "session_id": self.session_id,
            "turn_count": self.turn_count,
            "kb": kb_stats,
            "evolver": evolver_stats,
            "services": {
                "probe_llm": "active",
                "ffe_encoder": "active",
                "transcender": f"active ({self.transcender.synthesis_count} synthesis)",
                "ffe_store": "active",
                "evolver": f"active ({self.evolver.update_count} updates)"
            }
        }


# ============================================================================
# DEMO COMPLETA
# ============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                  🌌 GENESIS ORCHESTRATOR - DEMO COMPLETA 🌌                   ║
║                                                                               ║
║              Pipeline MCP Modular: 5 Servicios Integrados                    ║
║                    probe_llm → ffe_encoder → transcender                      ║
║                         → ffe_store → evolver                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar orquestador
    orchestrator = GenesisOrchestrator("data/demo_genesis_kb.db")
    
    # Conversaciones de prueba
    conversations = [
        {
            "user": "¿Qué es la justicia?",
            "model": "La justicia es el equilibrio entre derechos y deberes en una sociedad.",
            "space": "filosofia_etica"
        },
        {
            "user": "¿Y cómo se relaciona con la verdad?",
            "model": "La verdad es la correspondencia entre el pensamiento y la realidad.",
            "space": "filosofia_etica"
        },
        {
            "user": "¿Puede existir justicia sin verdad?",
            "model": "La justicia sin verdad se convierte en arbitrariedad.",
            "space": "filosofia_etica"
        },
        {
            "user": "Explica la física cuántica",
            "model": "La física cuántica estudia el comportamiento de partículas subatómicas.",
            "space": "ciencia_fisica"
        },
        {
            "user": "¿Qué es la superposición cuántica?",
            "model": "Es el principio por el cual una partícula puede estar en múltiples estados simultáneamente.",
            "space": "ciencia_fisica"
        },
        {
            "user": "¿Cómo funciona el amor?",
            "model": "El amor es una combinación de química cerebral y construcción social.",
            "space": "psicologia"
        },
    ]
    
    print("=== PROCESANDO CONVERSACIONES ===\n")
    
    for i, conv in enumerate(conversations, 1):
        print(f"--- Turno {i} [{conv['space']}] ---")
        print(f"Usuario: {conv['user']}")
        print(f"Modelo:  {conv['model']}")
        
        result = orchestrator.process_conversation_turn(
            conv['user'],
            conv['model'],
            conv['space']
        )
        
        if result["status"] == "ok":
            print(f"✓ Turn ID: {result['turn_id'][:8]}...")
            print(f"✓ Tensor ID: {result['tensor_id']}")
            print(f"✓ Ms emergente: {result['synthesis']['Ms']}")
            print(f"✓ Hash: {result['synthesis']['hash']}")
            print(f"✓ Coherencia: C_meta={result['coherence']['C_meta']:.2f}, "
                  f"C_ext={result['coherence']['C_ext']:.2f}, "
                  f"C_dyn={result['coherence']['C_dyn']:.2f}")
            print(f"✓ Es coherente: {result['coherence']['is_coherent']}")
            
            if result["evolution"]:
                evo = result['evolution']
                trend = evo.get('dynamics', {}).get('trend', 'unknown')
                print(f"✓ Evolución: {evo['archetypes']['total_archetypes']} arquetipos, trend={trend}")
            
            print(f"✓ Tiempo: {result['elapsed_ms']}ms")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        print()
    
    # Estadísticas finales
    print("\n" + "=" * 80)
    print("=== ESTADÍSTICAS FINALES ===")
    print("=" * 80 + "\n")
    
    stats = orchestrator.get_stats()
    print(f"Session ID: {stats['session_id']}")
    print(f"Total turnos procesados: {stats['turn_count']}")
    print(f"\nKnowledge Base:")
    print(f"  • Total tensores: {stats['kb']['total_tensors']}")
    print(f"  • Total arquetipos: {stats['kb']['total_archetypes']}")
    print(f"\nEvolver:")
    print(f"  • Arquetipos detectados: {stats['evolver']['total_archetypes']}")
    print(f"  • Relaciones mapeadas: {stats['evolver']['total_relations']}")
    print(f"  • Dinámicas registradas: {stats['evolver']['total_dynamics']}")
    print(f"\nServicios activos:")
    for service, status in stats['services'].items():
        print(f"  • {service}: {status}")
    
    print(f"\nTop arquetipos:")
    for pattern, count in stats['evolver']['top_archetypes'][:3]:
        print(f"  • {pattern}: {count} apariciones")
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("""
🎯 Siguiente paso: Ejecutar con API real de embeddings
   python genesis_orchestrator.py

📊 Ver estadísticas: orchestrator.get_stats()
🗄️ Explorar KB: data/demo_genesis_kb.db
📈 Métricas: C_meta (unicidad), C_ext (reconstrucción), C_dyn (estabilidad)
    """)
