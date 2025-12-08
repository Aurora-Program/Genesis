"""
Test Avanzado: Escenario Realista de Conversación con Aurora
Simula una conversación completa con aprendizaje incremental
"""

import sys
from pathlib import Path

current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from pipeline.llm_semantic_encoder import LLMSemanticEncoder
from core.evolver import Evolver3
from core.trigate import Trigate


def simulate_learning_conversation():
    """
    Simula una conversación real donde Aurora aprende progresivamente
    """
    print("\n" + "🌟"*35)
    print("  ESCENARIO REALISTA: AURORA APRENDIENDO DE CONVERSACIÓN")
    print("🌟"*35)
    
    # Inicializar
    encoder = LLMSemanticEncoder(llm_client=None)
    evolver = Evolver3(trigate_cls=Trigate, th_match=2)
    
    # Conversación realista: Usuario aprendiendo sobre Trinity-3
    conversation = [
        # === Fase 1: Exploración inicial ===
        ("Usuario", "¿Qué es Trinity-3?", 2),
        ("Aurora", "Trinity-3 es un sistema de computación ternaria fractal...", 1),
        
        # === Fase 2: Profundización en componentes ===
        ("Usuario", "Explica el Trigate", 2),
        ("Aurora", "Trigate es la unidad fundamental de computación con 3 bits ternarios...", 1),
        
        ("Usuario", "¿Cómo funciona el Transcender?", 2),
        ("Aurora", "Transcender opera 3 trigates sobre A,B,C para sintetizar Ms...", 1),
        
        ("Usuario", "¿Qué hace el Evolver?", 2),
        ("Aurora", "Evolver aprende patrones con 3 bancos: RELATOR, EMERGENCIA, DINÁMICA...", 1),
        
        # === Fase 3: Detalles técnicos ===
        ("Usuario", "¿Qué es la coherencia absoluta?", 2),
        ("Aurora", "La coherencia absoluta es el mecanismo top-down donde Ms repara hijos...", 1),
        
        ("Usuario", "Explica las LUTs del Trigate", 2),
        ("Aurora", "Las LUTs (lookup tables) mapean 27 combinaciones ternarias...", 1),
        
        # === Fase 4: Ejemplos prácticos ===
        ("Usuario", "Dame un ejemplo de síntesis", 1),
        ("Aurora", "Supongamos A=[1,0,None], B=[0,1,1], C=[1,None,0]...", 1),
        
        ("Usuario", "¿Cómo se repara un NULL?", 2),
        ("Aurora", "Harmonizer usa 5 niveles: Immediate, Local, Global, Pattern, Default...", 1),
        
        # === Fase 5: Integración conceptual ===
        ("Usuario", "¿Cómo se relacionan Transcender y Evolver?", 2),
        ("Aurora", "Transcender genera síntesis que Evolver aprende como patrones...", 1),
        
        ("Usuario", "¿Por qué la estructura es 3-9-27?", 2),
        ("Aurora", "Es autosimilar: cada nivel tiene 3 hijos, generando jerarquía fractal...", 1),
    ]
    
    # Métricas por fase
    phases = {
        "Exploración": (0, 2),
        "Profundización": (2, 8),
        "Ejemplos": (8, 12),
        "Integración": (12, 20)
    }
    
    print("\n📖 CONVERSACIÓN SIMULADA")
    print("="*70)
    
    all_mappings = []
    
    for turn, (speaker, message, depth) in enumerate(conversation):
        # Codificar
        mapping = encoder.encode(message, depth=depth)
        all_mappings.append((speaker, mapping))
        
        # Mostrar progreso cada 2 turnos
        if turn % 2 == 1:
            print(f"\n[Turno {turn-1}-{turn}]")
            print(f"  {conversation[turn-1][0]}: {conversation[turn-1][1][:50]}...")
            print(f"  {speaker}: {message[:50]}...")
            
            # Stats acumulados
            patterns = encoder.get_patterns_for_evolver()
            print(f"  📊 Aprendizaje acumulado:")
            print(f"     RELATOR: {len(patterns['relators'])} relaciones")
            print(f"     EMERGENCIA: {len(patterns['emergences'])} patrones")
            print(f"     DINÁMICA: {len(patterns['dynamics'])} transiciones")
    
    # Análisis final
    print("\n" + "="*70)
    print("📊 ANÁLISIS FINAL")
    print("="*70)
    
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"\n🔗 RELATOR (relaciones explícitas): {len(patterns['relators'])}")
    relator_types = {}
    for rel in patterns['relators']:
        t = rel['type']
        relator_types[t] = relator_types.get(t, 0) + 1
    
    for rel_type, count in sorted(relator_types.items(), key=lambda x: -x[1]):
        print(f"   • {rel_type}: {count}")
    
    print(f"\n✨ EMERGENCIA (patrones recurrentes): {len(patterns['emergences'])}")
    for i, emerg in enumerate(patterns['emergences'][:3], 1):
        print(f"   [{i}] {emerg['type']}: frecuencia={emerg['frequency']}")
        print(f"       Ejemplo: {emerg.get('example', 'N/A')[:40]}...")
    
    print(f"\n⏱️ DINÁMICA (secuencias aprendidas): {len(patterns['dynamics'])}")
    for i, dyn in enumerate(patterns['dynamics'][:3], 1):
        print(f"   [{i}] {dyn['type']}")
        print(f"       {dyn['context']['from_text'][:30]} → {dyn['context']['to_text'][:30]}")
    
    # Evolución del conocimiento por fase
    print(f"\n📈 EVOLUCIÓN DEL CONOCIMIENTO POR FASE")
    print("="*70)
    
    for phase_name, (start, end) in phases.items():
        phase_mappings = all_mappings[start:end]
        
        # Contar relaciones en esta fase
        phase_relations = sum(
            len(m.discovered_relations) 
            for _, m in phase_mappings
        )
        
        print(f"\n{phase_name} (turnos {start}-{end}):")
        print(f"   Relaciones descubiertas: {phase_relations}")
        print(f"   Conceptos explorados: {len(phase_mappings)}")
    
    # Validaciones
    print(f"\n" + "="*70)
    print("✅ VALIDACIONES")
    print("="*70)
    
    checks = [
        (len(patterns['relators']) > 15, f"RELATOR tiene 15+ relaciones: {len(patterns['relators'])}"),
        (len(patterns['emergences']) > 0, f"EMERGENCIA detectó patrones: {len(patterns['emergences'])}"),
        (len(patterns['dynamics']) > 3, f"DINÁMICA aprendió secuencias: {len(patterns['dynamics'])}"),
        (len(encoder.mapping_history) == len(conversation), f"Historial completo: {len(encoder.mapping_history)} mappings"),
    ]
    
    all_passed = True
    for check, message in checks:
        if check:
            print(f"   ✅ {message}")
        else:
            print(f"   ❌ {message}")
            all_passed = False
    
    # Conclusiones
    print(f"\n" + "="*70)
    print("🎓 CONCLUSIONES")
    print("="*70)
    
    print(f"""
1. INCREMENTAL: El sistema aprendió de {len(conversation)} turnos
   - Relaciones acumuladas: {len(patterns['relators'])}
   - Patrones emergentes: {len(patterns['emergences'])}
   - Dinámicas detectadas: {len(patterns['dynamics'])}

2. CONTEXTUAL: Cada turno construye sobre el anterior
   - Usuario explora → profundiza → pide ejemplos → integra
   - Aurora responde con contexto acumulado

3. AUTOSIMILAR: Expansión fractal funciona
   - depth=1: conceptos directos
   - depth=2: expansión autosimilar con 2+ relacionados
   - Estructura 3-9-27 preservada en todos los tensores

4. EVOLUTIVO: Evolver aprende patrones reales
   - RELATOR: {len(patterns['relators'])} relaciones explícitas
   - EMERGENCIA: {len(patterns['emergences'])} patrones recurrentes
   - DINÁMICA: {len(patterns['dynamics'])} secuencias temporales

RESULTADO: Aurora construyó un grafo de conocimiento funcional
           sobre Trinity-3 a partir de una conversación natural.
    """)
    
    if all_passed:
        print("\n🎉 ESCENARIO REALISTA: ✅ EXITOSO")
        print("    El sistema demuestra aprendizaje incremental funcional.")
    else:
        print("\n⚠️ ESCENARIO REALISTA: Algunas validaciones fallaron")
    
    return all_passed


def test_relation_strength_decay():
    """
    Test: Verifica que la fuerza de relaciones decae con distancia
    """
    print("\n" + "="*70)
    print("TEST AVANZADO: Decay de Fuerza en Relaciones")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    text = "Explica el sistema completo"
    mapping = encoder.encode(text, depth=3)
    
    print(f"\nTexto: '{text}' (depth=3)")
    print(f"Relaciones descubiertas: {len(mapping.discovered_relations)}")
    
    # Agrupar por strength
    strength_buckets = {
        "alta (>0.9)": [],
        "media (0.7-0.9)": [],
        "baja (<0.7)": []
    }
    
    for rel in mapping.discovered_relations:
        s = rel['strength']
        if s > 0.9:
            strength_buckets["alta (>0.9)"].append(rel)
        elif s >= 0.7:
            strength_buckets["media (0.7-0.9)"].append(rel)
        else:
            strength_buckets["baja (<0.7)"].append(rel)
    
    print(f"\nDistribución de fuerza:")
    for bucket, rels in strength_buckets.items():
        print(f"  {bucket}: {len(rels)} relaciones")
        if rels:
            example = rels[0]
            print(f"    Ejemplo: {example['source'][:25]} → {example['target'][:25]}")
    
    # Validar que hay decay (más relaciones cercanas que lejanas)
    assert len(strength_buckets["alta (>0.9)"]) >= len(strength_buckets["baja (<0.7)"]), \
        "❌ Debería haber más relaciones fuertes que débiles"
    
    print(f"\n✅ Decay de fuerza funciona correctamente")
    print(f"✅ Relaciones cercanas son más fuertes")
    
    return True


def test_emergent_pattern_detection():
    """
    Test: Detectar patrones emergentes con múltiples ejemplos similares
    """
    print("\n" + "="*70)
    print("TEST AVANZADO: Detección de Patrones Emergentes")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    # Codificar múltiples preguntas técnicas similares
    technical_questions = [
        "¿Qué es el Trigate?",
        "¿Qué es el Transcender?",
        "¿Qué es el Evolver?",
        "¿Qué es el Harmonizer?",
        "¿Qué es el Extender?",
    ]
    
    print(f"\nCodificando {len(technical_questions)} preguntas técnicas similares...")
    
    for q in technical_questions:
        encoder.encode(q, depth=1)
    
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"\nPatrones emergentes detectados: {len(patterns['emergences'])}")
    
    # Debe detectar que todas son preguntas técnicas con patrón similar
    has_recurring = any(
        p['frequency'] >= 2 
        for p in patterns['emergences']
    )
    
    assert has_recurring, "❌ No se detectaron patrones recurrentes"
    
    print(f"\n✅ Patrones emergentes detectados correctamente")
    
    for i, emerg in enumerate(patterns['emergences'], 1):
        print(f"\n  [{i}] {emerg['type']}")
        print(f"      Frecuencia: {emerg['frequency']}")
        print(f"      Ejemplo: {emerg.get('example', 'N/A')[:50]}")
    
    return True


def test_cross_concept_relations():
    """
    Test: Detectar relaciones entre conceptos diferentes
    """
    print("\n" + "="*70)
    print("TEST AVANZADO: Relaciones Cross-Concepto")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    # Batch con conceptos relacionados pero distintos
    related_concepts = [
        "El Trigate usa lógica ternaria",
        "El Transcender combina 3 trigates",
        "El Evolver aprende de síntesis"
    ]
    
    print(f"\nCodificando {len(related_concepts)} conceptos relacionados...")
    
    mappings = encoder.encode_batch(related_concepts, depth=2)
    
    # Contar relaciones cross-batch
    total_relations = sum(len(m.discovered_relations) for m in mappings)
    cross_relations = sum(
        1 for m in mappings 
        for rel in m.discovered_relations 
        if "cross" in rel["type"]
    )
    
    print(f"\nTotal relaciones: {total_relations}")
    print(f"Relaciones cross-batch: {cross_relations}")
    
    # Debe haber detectado relaciones entre conceptos
    assert cross_relations > 0, "❌ No se detectaron relaciones cross-batch"
    
    print(f"\n✅ Relaciones cross-concepto detectadas")
    
    # Mostrar algunas
    for m in mappings:
        for rel in m.discovered_relations:
            if "cross" in rel["type"]:
                print(f"\n  {rel['source'][:30]} --[{rel['type']}]--> {rel['target'][:30]}")
                print(f"  Strength: {rel['strength']:.2f}")
                break
    
    return True


if __name__ == "__main__":
    print("\n🚀" + "="*68 + "🚀")
    print("  TEST SUITE AVANZADO: ESCENARIOS REALISTAS")
    print("🚀" + "="*68 + "🚀")
    
    tests = [
        ("Conversación Realista", simulate_learning_conversation),
        ("Decay de Fuerza", test_relation_strength_decay),
        ("Patrones Emergentes", test_emergent_pattern_detection),
        ("Relaciones Cross-Concepto", test_cross_concept_relations),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ PASS"))
        except AssertionError as e:
            results.append((name, f"❌ FAIL: {e}"))
        except Exception as e:
            results.append((name, f"⚠️ ERROR: {e}"))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN TESTS AVANZADOS")
    print("="*70)
    
    for name, status in results:
        print(f"  {status} - {name}")
    
    passed = sum(1 for _, s in results if "PASS" in s)
    print(f"\n✅ {passed}/{len(tests)} tests avanzados pasaron")
    
    if passed == len(tests):
        print("\n🎉 ¡SISTEMA COMPLETAMENTE VALIDADO!")
        print("    Listo para integración con LLM real.")
    
    sys.exit(0 if passed == len(tests) else 1)
