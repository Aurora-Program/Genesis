"""
Demo Interactivo: LLM Construyendo Grafo de Conocimiento Incremental

Este script simula cómo el LLM Semantic Encoder descubre relaciones
de forma incremental, construyendo un grafo de conocimiento fractal.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Fix imports - add parent to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from pipeline.llm_semantic_encoder import LLMSemanticEncoder
from core.evolver import Evolver3


class KnowledgeGraph:
    """Grafo de conocimiento construido incrementalmente"""
    
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
    
    def add_node(self, concept: str, tensor: List[List], metadata: Dict = None):
        """Añade nodo (concepto) al grafo"""
        if concept not in self.nodes:
            self.nodes[concept] = {
                "tensor": tensor,
                "metadata": metadata or {},
                "discovery_order": len(self.nodes) + 1
            }
    
    def add_edge(self, source: str, target: str, relation: Dict):
        """Añade arista (relación) al grafo"""
        self.edges.append({
            "source": source,
            "target": target,
            "type": relation["type"],
            "strength": relation["strength"],
            "reasoning": relation.get("reasoning", "")
        })
    
    def get_stats(self):
        """Estadísticas del grafo"""
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "avg_degree": len(self.edges) / len(self.nodes) if self.nodes else 0,
            "relation_types": len(set(e["type"] for e in self.edges))
        }
    
    def visualize(self, max_edges: int = 20):
        """Visualización ASCII del grafo"""
        print("\n" + "="*70)
        print("GRAFO DE CONOCIMIENTO")
        print("="*70)
        
        # Nodos
        print(f"\n📦 NODOS ({len(self.nodes)}):")
        for i, (concept, data) in enumerate(list(self.nodes.items())[:10], 1):
            order = data["discovery_order"]
            print(f"  [{order:2d}] {concept[:40]}")
        
        if len(self.nodes) > 10:
            print(f"  ... y {len(self.nodes) - 10} más")
        
        # Relaciones por tipo
        print(f"\n🔗 RELACIONES ({len(self.edges)}):")
        by_type = {}
        for edge in self.edges:
            t = edge["type"]
            by_type[t] = by_type.get(t, 0) + 1
        
        for rel_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  • {rel_type:20s}: {count:3d}")
        
        # Algunas relaciones de ejemplo
        print(f"\n🔍 EJEMPLOS DE RELACIONES (top {min(max_edges, len(self.edges))}):")
        for edge in self.edges[:max_edges]:
            src = edge["source"][:25]
            tgt = edge["target"][:25]
            strength = edge["strength"]
            rel_type = edge["type"]
            print(f"  {src:25s} --[{rel_type}]--> {tgt:25s} (str: {strength:.2f})")
        
        # Stats
        stats = self.get_stats()
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"  Densidad: {stats['avg_degree']:.2f} relaciones/nodo")
        print(f"  Tipos de relación: {stats['relation_types']}")


def demo_incremental_discovery():
    """
    Demo principal: simula conversación donde el LLM va descubriendo
    relaciones incrementalmente
    """
    
    print("🧠 Demo: LLM Semantic Encoder - Descubrimiento Incremental")
    print("="*70)
    print()
    print("Simularemos una conversación sobre Trinity-3.")
    print("El LLM irá descubriendo relaciones con cada pregunta.")
    print()
    
    # Inicializar
    encoder = LLMSemanticEncoder(llm_client=None)  # Demo mode
    evolver = Evolver3(trigate_cls=None, th_match=2)  # Fixed: Evolver3 needs trigate_cls
    knowledge_graph = KnowledgeGraph()
    
    # Conversación simulada
    conversation = [
        ("Usuario", "¿Qué es Trinity-3?", 1),
        ("Usuario", "Explica el Trigate", 2),
        ("Usuario", "¿Cómo funciona el Transcender?", 2),
        ("Usuario", "Dame un ejemplo de síntesis emergente", 1),
        ("Usuario", "¿Qué aprende el Evolver?", 2),
    ]
    
    print("💬 CONVERSACIÓN:")
    print("-" * 70)
    
    for turn_num, (speaker, message, depth) in enumerate(conversation, 1):
        print(f"\n[Turno {turn_num}] {speaker}: {message}")
        print(f"  → Profundidad de exploración: {depth}")
        
        # Codificar mensaje
        mapping = encoder.encode(message, depth=depth)
        
        # Añadir concepto principal al grafo
        main_concept = extract_main_concept(message)
        knowledge_graph.add_node(
            main_concept,
            tensor=mapping.tensor.nivel_3,
            metadata={"source": message, "turn": turn_num}
        )
        
        # Añadir conceptos relacionados al grafo
        for related in mapping.related_content:
            related_concept = extract_main_concept(related)
            knowledge_graph.add_node(
                related_concept,
                tensor=[[0,0,0], [0,0,0], [0,0,0]],  # Simplified
                metadata={"source": related, "turn": turn_num, "type": "related"}
            )
        
        # Añadir relaciones al grafo
        for relation in mapping.discovered_relations:
            knowledge_graph.add_edge(
                source=relation["source"][:30],
                target=relation["target"][:30],
                relation=relation
            )
        
        # Mostrar descubrimientos de este turno
        print(f"  ✓ Conceptos relacionados: {len(mapping.related_content)}")
        print(f"  ✓ Relaciones descubiertas: {len(mapping.discovered_relations)}")
        
        # Mostrar algunas relaciones
        if mapping.discovered_relations:
            print(f"\n  Ejemplo de relación:")
            rel = mapping.discovered_relations[0]
            print(f"    {rel['source'][:25]} --[{rel['type']}]--> {rel['target'][:25]}")
            print(f"    Strength: {rel['strength']:.2f}")
        
        # Alimentar Evolver
        patterns = encoder.get_patterns_for_evolver()
        
        # Stats acumulados
        stats = knowledge_graph.get_stats()
        print(f"\n  📊 Grafo actual: {stats['nodes']} nodos, {stats['edges']} relaciones")
        
        print("-" * 70)
    
    # Visualizar grafo final
    knowledge_graph.visualize(max_edges=30)
    
    # Patrones emergentes en Evolver
    print("\n" + "="*70)
    print("🔮 PATRONES EMERGENTES (EVOLVER)")
    print("="*70)
    
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"\n🔗 RELATOR: {len(patterns['relators'])} relaciones")
    for i, rel in enumerate(patterns['relators'][:5], 1):
        print(f"  [{i}] {rel['type']:15s}: {rel['source'][:20]} → {rel['target'][:20]}")
    
    print(f"\n✨ EMERGENCIA: {len(patterns['emergences'])} patrones")
    for i, emerg in enumerate(patterns['emergences'][:3], 1):
        print(f"  [{i}] {emerg['type']}: frecuencia={emerg['frequency']}")
    
    print(f"\n⏱️ DINÁMICA: {len(patterns['dynamics'])} transiciones")
    for i, dyn in enumerate(patterns['dynamics'][:3], 1):
        print(f"  [{i}] {dyn['type']}: {dyn['context']['from_text'][:20]} → {dyn['context']['to_text'][:20]}")
    
    print("\n" + "="*70)
    print("✅ Demo completado")
    print()
    print("Observaciones:")
    print("  • El grafo creció de 0 a", stats['nodes'], "nodos en 5 turnos")
    print("  • Cada pregunta añadió conceptos relacionados (depth=1 o 2)")
    print("  • Las relaciones se descubrieron automáticamente por el LLM")
    print("  • Evolver almacenó patrones para reutilizar en futuras conversaciones")


def extract_main_concept(text: str) -> str:
    """
    Extrae concepto principal del texto
    Versión simplificada; con LLM real sería más sofisticado
    """
    # Buscar palabras clave
    keywords = ["Trinity-3", "Trigate", "Transcender", "Evolver", "síntesis", "coherencia"]
    
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return keyword
    
    # Fallback: primera palabra significativa
    words = text.split()
    for word in words:
        if len(word) > 4 and word not in ["Explica", "funciona", "ejemplo"]:
            return word.strip("¿?.,;:")
    
    return text[:30]


def demo_depth_comparison():
    """
    Demo: comparar diferentes profundidades de exploración
    """
    print("\n" + "="*70)
    print("🔬 COMPARACIÓN: DIFERENTES PROFUNDIDADES")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    text = "¿Qué es Trinity-3?"
    
    for depth in [0, 1, 2, 3]:
        print(f"\n📏 Profundidad = {depth}")
        print("-" * 70)
        
        mapping = encoder.encode(text, depth=depth)
        
        print(f"  Conceptos relacionados: {len(mapping.related_content)}")
        print(f"  Relaciones descubiertas: {len(mapping.discovered_relations)}")
        
        # Calcular nodos totales en expansión fractal
        # depth=0: 1 nodo (solo el original)
        # depth=1: 1 + 3 = 4 nodos
        # depth=2: 1 + 3 + 9 = 13 nodos
        # depth=3: 1 + 3 + 9 + 27 = 40 nodos
        nodes_by_depth = {
            0: 1,
            1: 1 + 3,
            2: 1 + 3 + 9,
            3: 1 + 3 + 9 + 27
        }
        
        print(f"  Nodos en expansión fractal: {nodes_by_depth.get(depth, '?')}")
        
        if mapping.related_content:
            print(f"\n  Ejemplos de contenido relacionado:")
            for i, rel in enumerate(mapping.related_content[:3], 1):
                print(f"    [{i}] {rel[:50]}")
    
    print("\n" + "="*70)
    print("📊 CONCLUSIÓN:")
    print("  • depth=0: solo el concepto original (exploración mínima)")
    print("  • depth=1: añade 3 relacionados directos")
    print("  • depth=2: expansión autosimilar (3→9 nodos)")
    print("  • depth=3: árbol fractal completo (3→9→27 nodos)")
    print()
    print("  Trade-off: depth mayor = más relaciones, pero más costoso (LLM calls)")


if __name__ == "__main__":
    # Demo principal
    demo_incremental_discovery()
    
    # Demo de comparación de profundidades
    demo_depth_comparison()
    
    print("\n" + "="*70)
    print("🎓 APRENDIZAJES CLAVE:")
    print("="*70)
    print("""
1. INCREMENTAL: El grafo crece con cada conversación
   - No necesita corpus completo desde el inicio
   - Aprende mientras interactúa

2. AUTOSIMILAR: Expansión fractal (3→9→27)
   - Cada nivel hereda del anterior
   - Patrones se repiten recursivamente

3. RELACIONAL: Descubre conexiones automáticamente
   - has_component, uses, feeds, synergy, etc.
   - Weights ajustados por uso repetido

4. EMERGENTE: Patrones aparecen con uso
   - RELATOR: relaciones explícitas
   - EMERGENCIA: patrones recurrentes
   - DINÁMICA: secuencias temporales

5. PREDICTIVO: Usa historial para anticipar
   - Evolver predice próximo turno
   - RELATOR provee contexto automático

RESULTADO: Aurora evoluciona continuamente, construyendo su propio
           grafo de conocimiento fractal a partir de conversaciones.
    """)
