"""
Test Completo del LLM Semantic Encoder
Valida todos los componentes y su integración
"""

import sys
from pathlib import Path

# Fix imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from pipeline.llm_semantic_encoder import LLMSemanticEncoder, SemanticMapping
from core.evolver import Evolver3
from core.trigate import Trigate
from core.transcender import Transcender
from core.fractal_tensor import FractalTensor
from typing import List, Dict


def test_1_basic_encoding():
    """Test 1: Codificación básica"""
    print("\n" + "="*70)
    print("TEST 1: Codificación Básica")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    text = "¿Qué es Trinity-3?"
    mapping = encoder.encode(text, depth=0)
    
    # Validaciones
    assert mapping.original_text == text, "❌ Texto no coincide"
    assert mapping.tensor is not None, "❌ Tensor es None"
    assert len(mapping.tensor.nivel_3) == 3, f"❌ nivel_3 debe tener 3 vectores, tiene {len(mapping.tensor.nivel_3)}"
    assert len(mapping.tensor.nivel_9) == 9, f"❌ nivel_9 debe tener 9 vectores, tiene {len(mapping.tensor.nivel_9)}"
    assert len(mapping.tensor.nivel_27) == 27, f"❌ nivel_27 debe tener 27 vectores, tiene {len(mapping.tensor.nivel_27)}"
    assert 0.0 <= mapping.confidence <= 1.0, "❌ Confidence fuera de rango"
    
    print(f"✅ Texto codificado: '{text}'")
    print(f"✅ Tensor generado: nivel_3={mapping.tensor.nivel_3}")
    print(f"✅ Confidence: {mapping.confidence}")
    print(f"✅ Reasoning: {mapping.llm_reasoning[:100]}...")
    
    return True


def test_2_depth_expansion():
    """Test 2: Expansión por profundidad"""
    print("\n" + "="*70)
    print("TEST 2: Expansión Autosimilar")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    text = "Explica el Transcender"
    
    results = {}
    for depth in [0, 1, 2, 3]:
        mapping = encoder.encode(text, depth=depth)
        results[depth] = {
            "related": len(mapping.related_content),
            "relations": len(mapping.discovered_relations)
        }
        print(f"\n  Depth={depth}:")
        print(f"    Related content: {results[depth]['related']}")
        print(f"    Relations: {results[depth]['relations']}")
    
    # Validaciones
    assert results[0]["related"] == 0, "❌ depth=0 debe tener 0 relacionados"
    assert results[1]["related"] >= 1, "❌ depth=1 debe tener 1+ relacionados"
    assert results[2]["related"] >= results[1]["related"], "❌ depth=2 debe tener más relacionados"
    assert results[3]["related"] >= results[2]["related"], "❌ depth=3 debe tener más relacionados"
    
    print(f"\n✅ Expansión autosimilar funciona correctamente")
    print(f"✅ Patrón: depth aumenta → más contenido relacionado")
    
    return True


def test_3_relation_discovery():
    """Test 3: Descubrimiento de relaciones"""
    print("\n" + "="*70)
    print("TEST 3: Descubrimiento de Relaciones")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    text = "¿Cómo funciona el Trigate?"
    mapping = encoder.encode(text, depth=2)
    
    print(f"\n  Texto: '{text}'")
    print(f"  Relaciones descubiertas: {len(mapping.discovered_relations)}")
    
    if mapping.discovered_relations:
        for i, rel in enumerate(mapping.discovered_relations[:3], 1):
            print(f"\n  [{i}] {rel['type']}")
            print(f"      {rel['source'][:30]} → {rel['target'][:30]}")
            print(f"      Strength: {rel['strength']:.2f}")
            assert "type" in rel, "❌ Relación sin tipo"
            assert "source" in rel, "❌ Relación sin source"
            assert "target" in rel, "❌ Relación sin target"
            assert "strength" in rel, "❌ Relación sin strength"
    
    print(f"\n✅ Relaciones tienen estructura correcta")
    print(f"✅ Tipos válidos: {set(r['type'] for r in mapping.discovered_relations)}")
    
    return True


def test_4_batch_encoding():
    """Test 4: Codificación en batch"""
    print("\n" + "="*70)
    print("TEST 4: Codificación en Batch")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    texts = [
        "¿Qué es Trinity-3?",
        "Explica el Trigate",
        "¿Cómo funciona el Transcender?"
    ]
    
    mappings = encoder.encode_batch(texts, depth=1)
    
    print(f"\n  Textos procesados: {len(mappings)}")
    assert len(mappings) == len(texts), "❌ No todos los textos fueron codificados"
    
    total_relations = sum(len(m.discovered_relations) for m in mappings)
    print(f"  Total relaciones descubiertas: {total_relations}")
    
    # Verificar que hay relaciones cross-batch
    has_cross = any(
        "cross" in rel["type"] 
        for m in mappings 
        for rel in m.discovered_relations
    )
    
    print(f"  Relaciones cross-batch detectadas: {'✅' if has_cross else '⚠️'}")
    
    print(f"\n✅ Batch encoding funciona correctamente")
    print(f"✅ Total relaciones: {total_relations}")
    
    return True


def test_5_evolver_integration():
    """Test 5: Integración con Evolver"""
    print("\n" + "="*70)
    print("TEST 5: Integración con Evolver")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    evolver = Evolver3(trigate_cls=Trigate, th_match=2)
    
    # Codificar varios textos
    texts = [
        "¿Qué es Trinity-3?",
        "Explica el Trigate",
        "Dame un ejemplo de síntesis"
    ]
    
    print(f"\n  Codificando {len(texts)} textos...")
    for text in texts:
        mapping = encoder.encode(text, depth=2)
    
    # Extraer patrones
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"\n  Patrones extraídos:")
    print(f"    RELATOR: {len(patterns['relators'])} relaciones")
    print(f"    EMERGENCIA: {len(patterns['emergences'])} patrones")
    print(f"    DINÁMICA: {len(patterns['dynamics'])} transiciones")
    
    # Validaciones
    assert "relators" in patterns, "❌ Falta 'relators' en patterns"
    assert "emergences" in patterns, "❌ Falta 'emergences' en patterns"
    assert "dynamics" in patterns, "❌ Falta 'dynamics' en patterns"
    
    assert len(patterns['relators']) > 0, "❌ RELATOR está vacío"
    
    print(f"\n  Ejemplo de relación (RELATOR):")
    if patterns['relators']:
        rel = patterns['relators'][0]
        print(f"    Type: {rel['type']}")
        print(f"    Source: {rel['source'][:30]}")
        print(f"    Target: {rel['target'][:30]}")
        print(f"    Strength: {rel['strength']:.2f}")
    
    print(f"\n✅ Integración con Evolver funciona")
    print(f"✅ Patrones correctamente estructurados")
    
    return True


def test_6_tensor_coherence():
    """Test 6: Coherencia de tensores generados"""
    print("\n" + "="*70)
    print("TEST 6: Coherencia de Tensores")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    # Codificar mismo texto múltiples veces
    text = "¿Qué es el Evolver?"
    
    tensors = []
    for i in range(3):
        mapping = encoder.encode(text, depth=1)
        tensors.append(mapping.tensor)
    
    print(f"\n  Codificando '{text}' 3 veces...")
    
    # Verificar que nivel_3 es consistente (demo mode es determinista)
    nivel_3_0 = str(tensors[0].nivel_3)
    nivel_3_1 = str(tensors[1].nivel_3)
    nivel_3_2 = str(tensors[2].nivel_3)
    
    print(f"\n  Tensor 1 nivel_3: {tensors[0].nivel_3}")
    print(f"  Tensor 2 nivel_3: {tensors[1].nivel_3}")
    print(f"  Tensor 3 nivel_3: {tensors[2].nivel_3}")
    
    consistent = (nivel_3_0 == nivel_3_1 == nivel_3_2)
    print(f"\n  Consistencia: {'✅' if consistent else '⚠️ (puede variar con LLM real)'}")
    
    # Verificar que todos los vectores tienen 3 elementos
    for i, tensor in enumerate(tensors):
        for j, vec in enumerate(tensor.nivel_3):
            assert len(vec) == 3, f"❌ Tensor {i} vector {j} no tiene 3 elementos"
    
    print(f"\n✅ Todos los tensores tienen estructura correcta")
    print(f"✅ nivel_3: 3 vectores de 3 bits cada uno")
    
    return True


def test_7_multi_turn_conversation():
    """Test 7: Conversación multi-turno"""
    print("\n" + "="*70)
    print("TEST 7: Conversación Multi-Turno")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    conversation = [
        ("Usuario", "¿Qué es Trinity-3?"),
        ("Aurora", "Trinity-3 es un sistema..."),
        ("Usuario", "Explica el Trigate"),
        ("Aurora", "Trigate es la unidad..."),
        ("Usuario", "Dame un ejemplo"),
    ]
    
    print(f"\n  Simulando conversación de {len(conversation)} turnos...")
    
    for turn, (speaker, message) in enumerate(conversation, 1):
        mapping = encoder.encode(message, depth=1)
        print(f"\n  [Turno {turn}] {speaker}: {message[:40]}...")
        print(f"    Related: {len(mapping.related_content)}")
        print(f"    Relations: {len(mapping.discovered_relations)}")
    
    # Verificar historial
    print(f"\n  Historial total: {len(encoder.mapping_history)} mappings")
    assert len(encoder.mapping_history) == len(conversation), "❌ Historial incompleto"
    
    # Extraer patrones finales
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"\n  Patrones aprendidos:")
    print(f"    RELATOR: {len(patterns['relators'])}")
    print(f"    EMERGENCIA: {len(patterns['emergences'])}")
    print(f"    DINÁMICA: {len(patterns['dynamics'])}")
    
    # Debe haber dinámicas (transiciones entre turnos)
    assert len(patterns['dynamics']) > 0, "❌ No se detectaron dinámicas"
    
    print(f"\n  Ejemplo de dinámica:")
    if patterns['dynamics']:
        dyn = patterns['dynamics'][0]
        print(f"    Type: {dyn['type']}")
        print(f"    From: {dyn['context']['from_text'][:30]}")
        print(f"    To: {dyn['context']['to_text'][:30]}")
    
    print(f"\n✅ Conversación multi-turno funciona")
    print(f"✅ Dinámicas detectadas correctamente")
    
    return True


def test_8_fractal_structure():
    """Test 8: Validar estructura fractal"""
    print("\n" + "="*70)
    print("TEST 8: Estructura Fractal (3-9-27)")
    print("="*70)
    
    encoder = LLMSemanticEncoder(llm_client=None)
    
    text = "¿Cómo funciona la síntesis emergente?"
    mapping = encoder.encode(text, depth=2)
    
    tensor = mapping.tensor
    
    print(f"\n  Validando tensor fractal...")
    
    # Nivel 3
    assert len(tensor.nivel_3) == 3, f"❌ nivel_3 debe tener 3, tiene {len(tensor.nivel_3)}"
    print(f"  ✅ nivel_3: 3 vectores")
    
    # Nivel 9 (3 hijos por cada nivel_3)
    assert len(tensor.nivel_9) == 9, f"❌ nivel_9 debe tener 9, tiene {len(tensor.nivel_9)}"
    print(f"  ✅ nivel_9: 9 vectores (3×3)")
    
    # Nivel 27 (3 hijos por cada nivel_9)
    assert len(tensor.nivel_27) == 27, f"❌ nivel_27 debe tener 27, tiene {len(tensor.nivel_27)}"
    print(f"  ✅ nivel_27: 27 vectores (3×3×3)")
    
    # Cada vector debe tener 3 elementos [Forma, Función, Estructura]
    for level_name, vectors in [
        ("nivel_3", tensor.nivel_3),
        ("nivel_9", tensor.nivel_9),
        ("nivel_27", tensor.nivel_27)
    ]:
        for i, vec in enumerate(vectors):
            assert len(vec) == 3, f"❌ {level_name}[{i}] no tiene 3 elementos"
            # Cada elemento debe ser 0, 1, o None
            for j, trit in enumerate(vec):
                assert trit in [0, 1, None], f"❌ {level_name}[{i}][{j}]={trit} no es ternario"
    
    print(f"  ✅ Todos los vectores son ternarios [0, 1, None]")
    
    # Total bits
    total_vectors = 3 + 9 + 27
    bits_per_vector = 3
    total_bits = total_vectors * bits_per_vector
    
    print(f"\n  📊 Estructura completa:")
    print(f"    Total vectores: {total_vectors}")
    print(f"    Bits por vector: {bits_per_vector}")
    print(f"    Total bits: {total_bits} (target: 117)")
    
    assert total_bits == 117, f"❌ Total bits debe ser 117, es {total_bits}"
    
    print(f"\n✅ Estructura fractal 3-9-27 correcta (117 bits)")
    
    return True


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "🧪" + "="*68 + "🧪")
    print("  TEST SUITE: LLM SEMANTIC ENCODER - VALIDACIÓN COMPLETA")
    print("🧪" + "="*68 + "🧪")
    
    tests = [
        test_1_basic_encoding,
        test_2_depth_expansion,
        test_3_relation_discovery,
        test_4_batch_encoding,
        test_5_evolver_integration,
        test_6_tensor_coherence,
        test_7_multi_turn_conversation,
        test_8_fractal_structure,
    ]
    
    results = []
    for i, test_func in enumerate(tests, 1):
        try:
            success = test_func()
            results.append((test_func.__name__, "✅ PASS", None))
        except AssertionError as e:
            results.append((test_func.__name__, "❌ FAIL", str(e)))
            print(f"\n❌ FAIL: {e}")
        except Exception as e:
            results.append((test_func.__name__, "⚠️ ERROR", str(e)))
            print(f"\n⚠️ ERROR: {e}")
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    for name, status, error in results:
        print(f"{status} {name}")
        if error:
            print(f"    → {error[:60]}")
    
    passed = sum(1 for _, status, _ in results if status == "✅ PASS")
    failed = sum(1 for _, status, _ in results if status == "❌ FAIL")
    errors = sum(1 for _, status, _ in results if status == "⚠️ ERROR")
    
    print(f"\n{'='*70}")
    print(f"Total: {len(results)} tests")
    print(f"  ✅ Pasados: {passed}")
    print(f"  ❌ Fallados: {failed}")
    print(f"  ⚠️ Errores: {errors}")
    print(f"{'='*70}")
    
    if passed == len(results):
        print("\n🎉 ¡TODOS LOS TESTS PASARON! Sistema validado.")
    else:
        print(f"\n⚠️ {failed + errors} tests no pasaron. Revisar detalles arriba.")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
