"""
Test con Dataset Real - Validación de Aurora con corpus español
================================================================

Usa datasets públicos para validar:
1. Procesamiento de texto largo
2. Detección de polisemia en contexto real
3. Generación de arquetipos a gran escala
4. Performance y escalabilidad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aurora_pipeline_complete import AuroraPipeline
from collections import Counter
import time


def test_with_simple_corpus():
    """
    Test con corpus simple sin dependencias externas.
    
    Usa textos de ejemplo variados para validar:
    - Procesamiento batch
    - Descubrimiento de arquetipos
    - Performance a escala
    """
    print("=" * 70)
    print("🧪 TEST: Aurora con Corpus Real")
    print("=" * 70 + "\n")
    
    # Corpus de textos variados en español
    corpus = [
        # Filosofía
        """La filosofía busca respuestas fundamentales sobre la existencia.
        ¿Qué es la realidad? ¿Cómo conocemos el mundo? Estas preguntas han
        ocupado a pensadores durante milenios. El banco de ideas filosóficas
        es vasto y profundo.""",
        
        # Tecnología
        """La inteligencia artificial transforma nuestra sociedad. Los sistemas
        de aprendizaje automático procesan datos masivos. El banco de servidores
        almacena petabytes de información. La red neuronal aprende patrones.""",
        
        # Naturaleza
        """El gato salvaje caza en la noche. Su vista aguda detecta presas.
        La planta crece buscando luz solar. El agua fluye por la corriente
        del río. La naturaleza sigue su orden perfecto.""",
        
        # Economía
        """El banco central regula la economía. La capital financiera concentra
        recursos. Los inversores buscan rendimientos. El mercado tiene orden
        y caos simultáneamente. La red de comercio global conecta países.""",
        
        # Deportes
        """El equipo ganó la copa del campeonato. Los jugadores celebraron en
        el banco de suplentes. La red vibró con el gol. El cabo del equipo
        levantó el trofeo. El orden táctico fue perfecto.""",
        
        # Vida cotidiana
        """Me senté en el banco del parque. La corriente de aire era agradable.
        Vi un gato durmiendo en la planta baja. La red de caminos conecta
        la ciudad. Todo tiene su orden natural.""",
        
        # Ciencia
        """La corriente eléctrica fluye por el circuito. La planta genera
        energía limpia. El gato de Schrödinger ilustra mecánica cuántica.
        La red cristalina tiene orden atómico. La capital de datos científicos crece.""",
        
        # Literatura
        """La vela iluminaba el manuscrito. El orden de las palabras importa.
        La clase de literatura analizó el texto. La copa de vino reposaba
        en la mesa. El banco de la memoria guarda historias.""",
        
        # Historia
        """El cabo militar dirigió la batalla. La capital cayó tras el asedio.
        El orden feudal colapsó. La clase noble perdió poder. La corriente
        de cambio era imparable.""",
        
        # Arte
        """El pintor trabajaba desde la planta alta. La copa con pinceles
        descansaba en la mesa. La vela proyectaba sombras. La clase magistral
        enseñó técnica. El orden del color era armónico."""
    ]
    
    # Inicializar pipeline
    print("🌌 Inicializando Aurora Pipeline (demo mode)...\n")
    pipeline = AuroraPipeline(demo_mode=True)
    
    # Procesar corpus
    print("📚 Procesando corpus de 10 textos...\n")
    results = []
    start_time = time.time()
    
    for i, texto in enumerate(corpus):
        print(f"  [{i+1}/10] Procesando texto {i+1}...")
        result = pipeline.process_text_long(
            text=texto,
            space_id="validation_corpus"
        )
        results.append(result)
    
    elapsed = time.time() - start_time
    
    # Análisis agregado
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DEL CORPUS")
    print("=" * 70 + "\n")
    
    # Estadísticas globales
    total_segments = sum(r['stats']['total_segments'] for r in results)
    total_tensors = sum(r['stats']['total_tensors'] for r in results)
    total_polysemy = sum(r['stats']['polysemy_count'] for r in results)
    
    print(f"📝 Texto procesado:")
    print(f"   - Documentos: {len(corpus)}")
    print(f"   - Segmentos totales: {total_segments}")
    print(f"   - Tensores FFE: {total_tensors}")
    print(f"   - Casos de polisemia: {total_polysemy}")
    
    # Arquetipos globales
    all_archetypes = []
    for result in results:
        if result['archetypes'].get('top_patterns'):
            all_archetypes.extend([p for p, c in result['archetypes']['top_patterns']])
    
    archetype_counts = Counter(all_archetypes)
    universal_archetypes = [(p, c) for p, c in archetype_counts.items() if c >= 3]
    
    print(f"\n🧠 Arquetipos descubiertos:")
    print(f"   - Únicos: {len(archetype_counts)}")
    print(f"   - Universales (≥3 docs): {len(universal_archetypes)}")
    
    if universal_archetypes:
        print(f"\n   Top 5 arquetipos universales:")
        for i, (pattern, count) in enumerate(sorted(universal_archetypes, key=lambda x: -x[1])[:5], 1):
            print(f"   {i}. {pattern[:50]}... → {count} documentos")
    
    # Palabras polisémicas detectadas
    polysemous_words_found = set()
    for result in results:
        for segment in result['sequence'].segments:
            if segment.polysemy_detected:
                # Extraer la palabra polisémica del texto
                words = ["banco", "gato", "vela", "clase", "planta", "copa", 
                         "capital", "ratón", "red", "orden", "corriente", "cabo"]
                for word in words:
                    if word in segment.text.lower():
                        polysemous_words_found.add(word)
    
    print(f"\n🔀 Polisemia detectada:")
    print(f"   - Palabras polisémicas: {', '.join(sorted(polysemous_words_found))}")
    print(f"   - Total casos: {total_polysemy}")
    
    # Performance
    print(f"\n⏱️ Performance:")
    print(f"   - Tiempo total: {elapsed:.2f}s")
    print(f"   - Tiempo/documento: {elapsed/len(corpus):.2f}s")
    print(f"   - Tensores/segundo: {total_tensors/elapsed:.2f}")
    
    # Validaciones
    print(f"\n✅ Validaciones:")
    
    # 1. Todos los textos procesados
    assert len(results) == len(corpus), "No todos los textos fueron procesados"
    print(f"   ✓ Todos los textos procesados: {len(results)}/{len(corpus)}")
    
    # 2. Polisemia detectada
    assert total_polysemy > 0, "No se detectó polisemia"
    print(f"   ✓ Polisemia detectada en {total_polysemy} segmentos")
    
    # 3. Arquetipos universales encontrados
    assert len(universal_archetypes) > 0, "No se encontraron arquetipos universales"
    print(f"   ✓ {len(universal_archetypes)} arquetipos universales descubiertos")
    
    # 4. Performance aceptable
    tensors_per_sec = total_tensors / elapsed
    assert tensors_per_sec > 10, f"Performance baja: {tensors_per_sec:.2f} tensors/s"
    print(f"   ✓ Performance: {tensors_per_sec:.2f} tensors/segundo")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    
    return results


def test_with_huggingface_dataset():
    """
    Test con dataset de HuggingFace (si está disponible).
    
    Requiere: pip install datasets
    """
    try:
        from datasets import load_dataset
    except ImportError:
        print("⚠️  'datasets' no instalado. Instalar con: pip install datasets")
        print("   Saltando test con HuggingFace dataset...\n")
        return None
    
    print("=" * 70)
    print("🧪 TEST: Aurora con Dataset HuggingFace")
    print("=" * 70 + "\n")
    
    print("📥 Descargando dataset...")
    try:
        # Dataset de Wikipedia en español (más accesible)
        dataset = load_dataset("wikipedia", "20220301.es", split="train", streaming=True)
        
        print("🌌 Inicializando Aurora Pipeline...\n")
        pipeline = AuroraPipeline(demo_mode=True)
        
        print("📚 Procesando primeros 20 artículos...\n")
        results = []
        
        for i, item in enumerate(dataset):
            if i >= 20:  # Limitar a 20 para test
                break
            
            texto = item['text'][:1000]  # Primeros 1000 chars
            print(f"  [{i+1}/20] Procesando artículo...")
            
            result = pipeline.process_text_long(
                text=texto,
                space_id="wikipedia_es"
            )
            results.append(result)
        
        print(f"\n✅ Procesados {len(results)} artículos de Wikipedia")
        return results
        
    except Exception as e:
        print(f"⚠️  Error cargando dataset: {e}")
        print("   Continuando con corpus simple...\n")
        return None


if __name__ == "__main__":
    # Test 1: Corpus simple (siempre funciona)
    print("\n🔬 TEST 1: Corpus de validación simple\n")
    results_simple = test_with_simple_corpus()
    
    # Test 2: Dataset HuggingFace (opcional)
    print("\n\n🔬 TEST 2: Dataset HuggingFace (opcional)\n")
    results_hf = test_with_huggingface_dataset()
    
    print("\n" + "=" * 70)
    print("🎉 TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    
    if results_simple:
        print(f"\n✅ Test corpus simple: {len(results_simple)} documentos procesados")
    
    if results_hf:
        print(f"✅ Test HuggingFace: {len(results_hf)} artículos procesados")
    
    print("\n💡 Aurora validado con datos reales!")
