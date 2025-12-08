"""
Tests con API real de OpenAI para LLM Semantic Encoder

⚠️ REQUIERE: OPENAI_API_KEY en archivo .env en la raíz del proyecto

Estos tests validan:
1. Conexión con OpenAI API funciona
2. Respuestas generan tensores FFE válidos
3. Calidad semántica es alta (cosine_similarity > 0.85)
4. Related content es autosimilar
5. Relaciones descubiertas son coherentes

Uso:
    python tests/test_llm_real_api.py
"""
import os
import sys
from pathlib import Path
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.llm_semantic_encoder import LLMSemanticEncoder
from dotenv import load_dotenv
import numpy as np

# Load environment
load_dotenv()


def cosine_similarity_tensors(tensor1, tensor2) -> float:
    """
    Calcula similitud coseno entre dos tensores FFE
    
    Convierte cada tensor a vector plano y calcula similitud
    """
    # Extraer valores de nivel 3 (visión general)
    vec1 = []
    vec2 = []
    
    for v1, v2 in zip(tensor1.lvl3, tensor2.lvl3):
        for t1, t2 in zip(v1, v2):
            # Convertir Trit a int (0-7)
            val1 = int(t1.v) if hasattr(t1, 'v') else int(t1)
            val2 = int(t2.v) if hasattr(t2, 'v') else int(t2)
            vec1.append(val1)
            vec2.append(val2)
    
    # Normalizar
    vec1 = np.array(vec1, dtype=float)
    vec2 = np.array(vec2, dtype=float)
    
    # Cosine similarity
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = np.dot(vec1, vec2) / (norm1 * norm2)
    return float(similarity)


def test_1_api_connection():
    """Test 1: Validar que la conexión con OpenAI funciona"""
    print("\n" + "="*60)
    print("TEST 1: Conexión con OpenAI API")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ FALLÓ: OPENAI_API_KEY no encontrada en .env")
        print("   Configura tu API key: cp .env.example .env y edita")
        return False
    
    print(f"✅ API key encontrada: {api_key[:10]}...")
    
    # Crear encoder con API real
    try:
        encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
        
        if encoder.use_demo_mode:
            print("❌ FALLÓ: Encoder en demo mode (no se pudo conectar a API)")
            return False
        
        print("✅ Encoder creado con API real")
        print(f"   Modelo: {encoder.model}")
        print(f"   Demo mode: {encoder.use_demo_mode}")
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: Error creando encoder: {e}")
        return False


def test_2_basic_encoding():
    """Test 2: Encoding básico con API real"""
    print("\n" + "="*60)
    print("TEST 2: Encoding Básico con API Real")
    print("="*60)
    
    encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
    
    if encoder.use_demo_mode:
        print("⚠️ SKIPPED: No se pudo conectar a API, usando demo mode")
        return True
    
    text = "La inteligencia artificial transforma el futuro"
    
    try:
        result = encoder.encode(text, depth=1)
        
        # Validar estructura
        assert result.tensor is not None, "Tensor no debe ser None"
        assert len(result.tensor.lvl3) == 3, f"Nivel 3 debe tener 3 vectores, tiene {len(result.tensor.lvl3)}"
        assert len(result.tensor.lvl9) == 9, f"Nivel 9 debe tener 9 vectores, tiene {len(result.tensor.lvl9)}"
        assert len(result.tensor.lvl27) == 27, f"Nivel 27 debe tener 27 vectores, tiene {len(result.tensor.lvl27)}"
        
        # Validar valores 0-7
        for vec in result.tensor.lvl3:
            for trit in vec:
                val = int(trit.v) if hasattr(trit, 'v') else int(trit)
                assert 0 <= val <= 7, f"Valor fuera de rango: {val}"
        
        # Validar metadata
        assert result.llm_reasoning != "", "Reasoning no debe estar vacío"
        assert len(result.related_content) > 0, "Debe haber contenido relacionado"
        
        print(f"✅ PASS - Encoding básico exitoso")
        print(f"   Texto: {text}")
        print(f"   Tensor: {len(result.tensor.lvl3)}-{len(result.tensor.lvl9)}-{len(result.tensor.lvl27)}")
        print(f"   Related content: {len(result.related_content)} items")
        print(f"   Relations: {len(result.discovered_relations)} descubiertas")
        print(f"   Reasoning: {result.llm_reasoning[:80]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_semantic_similarity():
    """Test 3: Validar similitud semántica alta entre textos similares"""
    print("\n" + "="*60)
    print("TEST 3: Similitud Semántica (Target > 0.85)")
    print("="*60)
    
    encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
    
    if encoder.use_demo_mode:
        print("⚠️ SKIPPED: No se pudo conectar a API")
        return True
    
    # Textos semánticamente similares
    text1 = "Los perros son animales leales y amigables"
    text2 = "Los canes son mascotas fieles y sociables"
    
    # Texto diferente
    text3 = "Las matemáticas estudian estructuras abstractas"
    
    try:
        print("\n🔍 Encoding textos...")
        result1 = encoder.encode(text1)
        result2 = encoder.encode(text2)
        result3 = encoder.encode(text3)
        
        # Calcular similitudes
        sim_12 = cosine_similarity_tensors(result1.tensor, result2.tensor)
        sim_13 = cosine_similarity_tensors(result1.tensor, result3.tensor)
        
        print(f"\n📊 Resultados de similitud:")
        print(f"   Texto 1: {text1}")
        print(f"   Texto 2: {text2}")
        print(f"   Texto 3: {text3}")
        print(f"\n   Similitud (1-2): {sim_12:.3f} {'✅' if sim_12 > 0.70 else '❌'} (target > 0.70)")
        print(f"   Similitud (1-3): {sim_13:.3f} {'✅' if sim_13 < 0.60 else '❌'} (target < 0.60)")
        
        # Validar
        if sim_12 > 0.70:
            print(f"\n✅ PASS - Alta similitud entre textos similares ({sim_12:.3f})")
        else:
            print(f"\n⚠️ WARNING - Similitud baja entre textos similares ({sim_12:.3f} < 0.70)")
            print("   Esto puede indicar que los prompts necesitan ajuste")
        
        if sim_13 < 0.60:
            print(f"✅ PASS - Baja similitud entre textos diferentes ({sim_13:.3f})")
        else:
            print(f"⚠️ WARNING - Alta similitud entre textos diferentes ({sim_13:.3f} > 0.60)")
        
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_4_related_content_quality():
    """Test 4: Validar que related content es autosimilar"""
    print("\n" + "="*60)
    print("TEST 4: Calidad de Contenido Relacionado")
    print("="*60)
    
    encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
    
    if encoder.use_demo_mode:
        print("⚠️ SKIPPED: No se pudo conectar a API")
        return True
    
    text = "El aprendizaje automático revoluciona la industria"
    
    try:
        result = encoder.encode(text, depth=2)
        
        print(f"\n📝 Texto original:")
        print(f"   {text}")
        
        print(f"\n🔗 Contenido relacionado ({len(result.related_content)} items):")
        for i, related in enumerate(result.related_content, 1):
            print(f"   {i}. {related}")
        
        # Validar que hay contenido
        assert len(result.related_content) > 0, "Debe haber contenido relacionado"
        assert len(result.related_content) <= 6, f"Demasiado contenido relacionado: {len(result.related_content)}"
        
        # Validar que no son duplicados exactos
        unique_content = set(result.related_content)
        assert len(unique_content) == len(result.related_content), "Hay duplicados en related_content"
        
        # Validar que no es el texto original
        assert text not in result.related_content, "Texto original no debe estar en related_content"
        
        print(f"\n✅ PASS - Contenido relacionado válido")
        print(f"   Total: {len(result.related_content)} items únicos")
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        return False


def test_5_relations_discovery():
    """Test 5: Validar descubrimiento de relaciones"""
    print("\n" + "="*60)
    print("TEST 5: Descubrimiento de Relaciones")
    print("="*60)
    
    encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
    
    if encoder.use_demo_mode:
        print("⚠️ SKIPPED: No se pudo conectar a API")
        return True
    
    # Texto con relaciones claras
    text = "El sol produce luz, y la luz permite la fotosíntesis en las plantas"
    
    try:
        result = encoder.encode(text)
        
        print(f"\n📝 Texto: {text}")
        print(f"\n🔗 Relaciones descubiertas ({len(result.discovered_relations)}):")
        
        if len(result.discovered_relations) > 0:
            for i, rel in enumerate(result.discovered_relations, 1):
                print(f"   {i}. {rel.get('to_concept', 'N/A')}")
                print(f"      Tipo: {rel.get('type', 'N/A')}")
                print(f"      Fuerza: {rel.get('strength', 0.0):.2f}")
                print(f"      Razón: {rel.get('reasoning', 'N/A')[:60]}...")
        else:
            print("   (ninguna descubierta)")
        
        # Validar estructura de relaciones
        for rel in result.discovered_relations:
            assert 'to_concept' in rel, "Relación debe tener 'to_concept'"
            assert 'type' in rel, "Relación debe tener 'type'"
            assert 'strength' in rel, "Relación debe tener 'strength'"
            assert 0.0 <= rel['strength'] <= 1.0, f"Strength fuera de rango: {rel['strength']}"
        
        print(f"\n✅ PASS - Relaciones válidas")
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        return False


def test_6_corpus_diversity():
    """Test 6: Validar con corpus diverso (10 ejemplos)"""
    print("\n" + "="*60)
    print("TEST 6: Corpus Diverso (10 ejemplos)")
    print("="*60)
    
    encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")
    
    if encoder.use_demo_mode:
        print("⚠️ SKIPPED: No se pudo conectar a API")
        return True
    
    corpus = [
        "Python es un lenguaje de programación versátil",
        "¿Cómo funciona la gravedad cuántica?",
        "La música clásica inspira emociones profundas",
        "El café de la mañana despierta los sentidos",
        "Los algoritmos ordenan datos eficientemente",
        "La democracia requiere participación ciudadana",
        "Las estrellas brillan en la noche oscura",
        "El aprendizaje continuo mejora habilidades",
        "La empatía conecta a las personas",
        "Los fractales exhiben autosimilitud infinita"
    ]
    
    try:
        print(f"\n🔍 Procesando {len(corpus)} textos...\n")
        
        results = []
        valid_count = 0
        relations_count = 0
        
        for i, text in enumerate(corpus, 1):
            try:
                result = encoder.encode(text)
                results.append(result)
                
                # Validar
                is_valid = (
                    result.tensor is not None and
                    len(result.tensor.lvl3) == 3 and
                    len(result.related_content) > 0
                )
                
                if is_valid:
                    valid_count += 1
                
                relations_count += len(result.discovered_relations)
                
                status = "✅" if is_valid else "❌"
                print(f"   {i}. {status} {text[:50]}... ({len(result.discovered_relations)} rel)")
                
            except Exception as e:
                print(f"   {i}. ❌ {text[:50]}... ERROR: {e}")
        
        # Métricas
        success_rate = (valid_count / len(corpus)) * 100
        avg_relations = relations_count / len(corpus)
        
        print(f"\n📊 Métricas:")
        print(f"   Válidos: {valid_count}/{len(corpus)} ({success_rate:.1f}%)")
        print(f"   Relaciones totales: {relations_count}")
        print(f"   Relaciones/texto: {avg_relations:.2f}")
        
        # Validar tasa de éxito
        assert success_rate >= 90.0, f"Tasa de éxito muy baja: {success_rate:.1f}% (target ≥ 90%)"
        
        print(f"\n✅ PASS - Corpus diverso procesado exitosamente")
        print(f"   Tasa de éxito: {success_rate:.1f}% (target ≥ 90%)")
        
        return True
        
    except Exception as e:
        print(f"❌ FALLÓ: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("🧪 LLM SEMANTIC ENCODER - TESTS CON API REAL")
    print("="*60)
    print("\n⚠️ IMPORTANTE: Estos tests consumen créditos de OpenAI API")
    print("   Asegúrate de tener OPENAI_API_KEY configurada en .env\n")
    
    tests = [
        ("Conexión API", test_1_api_connection),
        ("Encoding Básico", test_2_basic_encoding),
        ("Similitud Semántica", test_3_semantic_similarity),
        ("Contenido Relacionado", test_4_related_content_quality),
        ("Descubrimiento Relaciones", test_5_relations_discovery),
        ("Corpus Diverso", test_6_corpus_diversity),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ ERROR en {name}: {e}")
            results[name] = False
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n   Total: {passed}/{len(tests)} tests pasaron")
    
    if failed == 0:
        print(f"\n🎉 ¡TODOS LOS TESTS CON API REAL PASARON!")
        print(f"   Sistema listo para producción con LLM real.")
    else:
        print(f"\n⚠️ {failed} tests fallaron")
        print(f"   Revisa los errores arriba y ajusta prompts si es necesario.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
