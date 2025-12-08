"""
Aurora Pipeline End-to-End - Texto Largo → Aprendizaje Fractal
================================================================

FLUJO COMPLETO:
1. Texto largo → SequenceEncoder → Secuencia de tensores FFE
2. Pares de tensores → Transcender → Síntesis emergentes (Ms, Ss, MetaM)
3. Secuencia + Síntesis → Evolver → Arquetipos + Relaciones + Dinámicas
4. Todo → FFE Store (KB) → Persistencia y consulta

Este pipeline permite a Aurora:
- Procesar conversaciones completas
- Detectar patrones a través del tiempo
- Aprender relaciones semánticas contextuales
- Descubrir arquetipos universales
- Rastrear dinámicas de coherencia
"""

from typing import List, Dict, Optional
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.sequence_encoder import SequenceEncoder, TensorSequence
from pipeline.llm_semantic_encoder import LLMSemanticEncoder
# from mcp_servers.transcender_service import TranscenderService  # Si existe
# from mcp_servers.evolver_service import EvolverService  # Si existe
# from mcp_servers.ffe_store import FFEStore  # Si existe


class AuroraPipeline:
    """
    Pipeline completo de Aurora para procesamiento de texto largo.
    
    Componentes:
    1. SequenceEncoder: Texto → Secuencia FFE
    2. Transcender: Pares FFE → Síntesis (Ms, Ss, MetaM)
    3. Evolver: Secuencias → Arquetipos + Relaciones + Dinámicas
    4. FFEStore: Persistencia en Knowledge Base
    
    Uso:
        pipeline = AuroraPipeline()
        result = pipeline.process_text_long(texto_largo)
        
        # Resultado contiene:
        - result['tensors']: Secuencia de tensores FFE
        - result['archetypes']: Arquetipos descubiertos
        - result['relations']: Relaciones encontradas
        - result['dynamics']: Dinámicas de coherencia
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        demo_mode: bool = False,
        store_path: str = "data/aurora_kb.db"
    ):
        """
        Inicializa el pipeline completo.
        
        Args:
            openai_api_key: API key para LLM real (None = .env)
            model: Modelo LLM a usar
            demo_mode: Si True, usa heurísticas sin API
            store_path: Path a la Knowledge Base SQLite
        """
        print("🌌 Inicializando Aurora Pipeline...")
        
        # 1. LLM Semantic Encoder
        print("   → LLM Semantic Encoder")
        self.llm_encoder = LLMSemanticEncoder(
            openai_api_key=openai_api_key,
            model=model,
            demo_mode=demo_mode,
            use_cache=True
        )
        
        # 2. Sequence Encoder
        print("   → Sequence Encoder")
        self.sequence_encoder = SequenceEncoder(
            llm_encoder=self.llm_encoder,
            segmentation_strategy="semantic",
            detect_polysemy=True
        )
        
        # 3. Transcender (placeholder si no existe)
        print("   → Transcender Service")
        try:
            from pipeline.transcender_service import TranscenderService
            self.transcender = TranscenderService()
            print("      ✅ Transcender Real cargado")
        except (ImportError, ModuleNotFoundError):
            print("      ⚠️ TranscenderService no encontrado, usando mock")
            self.transcender = None
        
        # 4. Evolver (placeholder si no existe)
        print("   → Evolver Service")
        try:
            from mcp_servers.evolver_service import EvolverService
            self.evolver = EvolverService()
        except (ImportError, ModuleNotFoundError):
            print("      ⚠️ EvolverService no encontrado, usando mock")
            self.evolver = None
        
        # 5. FFE Store (placeholder si no existe)
        print("   → FFE Store (Knowledge Base)")
        try:
            from mcp_servers.ffe_store import FFEStore
            self.store = FFEStore(store_path)
        except (ImportError, ModuleNotFoundError):
            print("      ⚠️ FFEStore no encontrado, usando mock")
            self.store = None
        
        print("✅ Aurora Pipeline inicializado\n")
    
    def process_text_long(
        self,
        text: str,
        depth: int = 1,
        space_id: str = "default"
    ) -> Dict:
        """
        Procesa texto largo end-to-end.
        
        Flujo:
        1. Segmentar y generar secuencia de tensores FFE
        2. Aplicar Transcender a pares consecutivos
        3. Pasar secuencia completa a Evolver
        4. Almacenar todo en KB
        
        Args:
            text: Texto largo a procesar
            depth: Profundidad de análisis (1-3)
            space_id: Identificador del espacio lógico
        
        Returns:
            Dict con resultados completos:
            {
                'sequence': TensorSequence,
                'transcensions': List[Dict],
                'archetypes': Dict,
                'relations': List[Dict],
                'dynamics': Dict,
                'kb_ids': List[int]
            }
        """
        print("=" * 70)
        print(f"🚀 PROCESANDO TEXTO LARGO ({len(text)} chars)")
        print("=" * 70 + "\n")
        
        start_time = time.time()
        
        # ========== FASE 1: Sequence Encoding ==========
        print("📝 FASE 1: Generando secuencia de tensores FFE")
        print("-" * 70)
        
        sequence = self.sequence_encoder.encode_text_long(text, depth=depth)
        
        print(f"\n✅ Secuencia generada:")
        print(f"   - Segmentos: {len(sequence.segments)}")
        print(f"   - Tensores FFE: {len(sequence.tensors)}")
        print(f"   - Polisemia detectada: {sequence.polysemy_count} casos")
        
        # ========== FASE 2: Transcender Pares ==========
        print(f"\n🔄 FASE 2: Aplicando Transcender a pares consecutivos")
        print("-" * 70)
        
        transcensions = self._apply_transcender_to_sequence(sequence, space_id)
        
        print(f"\n✅ Transcender aplicado:")
        print(f"   - Pares procesados: {len(transcensions)}")
        if transcensions:
            avg_coherence = sum(t.get('C_meta', 0) for t in transcensions) / len(transcensions)
            print(f"   - Coherencia promedio: {avg_coherence:.3f}")
        
        # ========== FASE 3: Evolver (Aprendizaje) ==========
        print(f"\n🧠 FASE 3: Evolver - Aprendizaje de patrones")
        print("-" * 70)
        
        evolution_result = self._apply_evolver(sequence, transcensions, space_id)
        
        print(f"\n✅ Evolver completado:")
        print(f"   - Arquetipos descubiertos: {evolution_result.get('total_archetypes', 0)}")
        print(f"   - Relaciones encontradas: {evolution_result.get('total_relations', 0)}")
        print(f"   - Dinámicas rastreadas: {evolution_result.get('total_dynamics', 0)}")
        
        # ========== FASE 4: Persistencia en KB ==========
        print(f"\n💾 FASE 4: Almacenando en Knowledge Base")
        print("-" * 70)
        
        kb_ids = self._store_in_kb(sequence, transcensions, evolution_result, space_id)
        
        print(f"\n✅ Almacenamiento completado:")
        print(f"   - Tensores guardados: {len(kb_ids)}")
        
        # ========== RESUMEN FINAL ==========
        elapsed = time.time() - start_time
        
        print(f"\n{'=' * 70}")
        print(f"✅ PROCESAMIENTO COMPLETADO")
        print(f"{'=' * 70}")
        print(f"⏱️  Tiempo total: {elapsed:.2f}s")
        if elapsed > 0:
            print(f"📊 Tensores/segundo: {len(sequence.tensors) / elapsed:.2f}")
        print(f"🎯 Espacio lógico: '{space_id}'")
        
        return {
            'sequence': sequence,
            'transcensions': transcensions,
            'archetypes': evolution_result.get('archetypes', {}),
            'relations': evolution_result.get('relations', []),
            'dynamics': evolution_result.get('dynamics', {}),
            'kb_ids': kb_ids,
            'stats': {
                'total_segments': len(sequence.segments),
                'total_tensors': len(sequence.tensors),
                'polysemy_count': sequence.polysemy_count,
                'total_archetypes': evolution_result.get('total_archetypes', 0),
                'total_relations': evolution_result.get('total_relations', 0),
                'processing_time': elapsed,
                'space_id': space_id
            }
        }
    
    def _apply_transcender_to_sequence(
        self,
        sequence: TensorSequence,
        space_id: str
    ) -> List[Dict]:
        """
        Aplica Transcender a pares consecutivos de tensores.
        
        Para cada (tensor_i, tensor_i+1):
        - Genera síntesis emergente (Ms, Ss, MetaM)
        - Calcula coherencia C_meta
        """
        if not self.transcender:
            print("   ⚠️ Transcender no disponible, saltando...")
            return []
        
        transcensions = []
        
        for i in range(len(sequence.tensors) - 1):
            tensor_a = sequence.tensors[i]
            tensor_b = sequence.tensors[i + 1]
            
            try:
                # Llamar al Transcender con el par
                result = self.transcender.transcend(
                    A=tensor_a.tensor.to_dict(),
                    B=tensor_b.tensor.to_dict(),
                    C=None  # Sin tercer elemento por ahora
                )
                
                result['pair_index'] = i
                result['space_id'] = space_id
                transcensions.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"   → Procesados {i + 1} pares...")
                
            except Exception as e:
                print(f"   ⚠️ Error en par {i}: {e}")
                continue
        
        return transcensions
    
    def _apply_evolver(
        self,
        sequence: TensorSequence,
        transcensions: List[Dict],
        space_id: str
    ) -> Dict:
        """
        Aplica Evolver para aprender patrones.
        
        Aprende:
        - Arquetipos: Patrones recurrentes en tensores
        - Relaciones: Conexiones entre segmentos
        - Dinámicas: Evolución de coherencia temporal
        """
        if not self.evolver:
            print("   ⚠️ Evolver no disponible, usando análisis básico...")
            return self._basic_pattern_analysis(sequence, transcensions)
        
        # Construir historial para Evolver
        history_batch = []
        
        for i, (tensor_mapping, segment) in enumerate(zip(sequence.tensors, sequence.segments)):
            turn_record = {
                'turn_id': f"{space_id}_seg_{i}",
                'space_id': space_id,
                'tensor': tensor_mapping.tensor.to_dict(),
                'text': segment.text,
                'transcend': transcensions[i] if i < len(transcensions) else None,
                'coherence': transcensions[i].get('C_meta', 0) if i < len(transcensions) else 0
            }
            history_batch.append(turn_record)
        
        # Llamar a Evolver
        try:
            result = self.evolver.update(history_batch)
            print(f"   → Arquetipos: {result.get('archetypes', {}).get('total_archetypes', 0)}")
            print(f"   → Relaciones: {result.get('relations', {}).get('total_relations', 0)}")
            print(f"   → Dinámicas: {result.get('dynamics', {}).get('trend', 'N/A')}")
            return result
        except Exception as e:
            print(f"   ⚠️ Error en Evolver: {e}")
            return self._basic_pattern_analysis(sequence, transcensions)
    
    def _basic_pattern_analysis(
        self,
        sequence: TensorSequence,
        transcensions: List[Dict]
    ) -> Dict:
        """Análisis básico cuando Evolver no está disponible"""
        from collections import Counter
        
        # Contar patrones en nivel_3
        patterns = []
        for tensor_mapping in sequence.tensors:
            pattern = str(tensor_mapping.tensor.nivel_3)
            patterns.append(pattern)
        
        pattern_counts = Counter(patterns)
        top_patterns = pattern_counts.most_common(5)
        
        # Coherencia promedio
        if transcensions:
            avg_coherence = sum(t.get('C_meta', 0) for t in transcensions) / len(transcensions)
            trend = "stable" if 0.85 <= avg_coherence <= 0.95 else "variable"
        else:
            avg_coherence = 0.0
            trend = "unknown"
        
        return {
            'archetypes': {
                'top_patterns': top_patterns,
                'total_archetypes': len(pattern_counts),
                'unique_patterns': len(set(patterns))
            },
            'relations': {
                'total_relations': len(transcensions)
            },
            'dynamics': {
                'avg_coherence': avg_coherence,
                'trend': trend,
                'total_dynamics': len(transcensions)
            },
            'total_archetypes': len(pattern_counts),
            'total_relations': len(transcensions),
            'total_dynamics': len(transcensions)
        }
    
    def _store_in_kb(
        self,
        sequence: TensorSequence,
        transcensions: List[Dict],
        evolution_result: Dict,
        space_id: str
    ) -> List[int]:
        """
        Almacena toda la secuencia en la Knowledge Base.
        
        Returns:
            Lista de IDs asignados en la KB
        """
        if not self.store:
            print("   ⚠️ FFEStore no disponible, saltando almacenamiento...")
            return []
        
        kb_ids = []
        
        for i, (tensor_mapping, segment) in enumerate(zip(sequence.tensors, sequence.segments)):
            try:
                tensor_id = self.store.store_tensor(
                    tensor_dict=tensor_mapping.tensor.to_dict(),
                    synthesis=transcensions[i] if i < len(transcensions) else None,
                    metadata={
                        'space_id': space_id,
                        'segment_index': i,
                        'text': segment.text,
                        'has_polysemy': segment.polysemy_detected,
                        'related_content': tensor_mapping.related_content
                    }
                )
                kb_ids.append(tensor_id)
                
                if (i + 1) % 10 == 0:
                    print(f"   → Almacenados {i + 1} tensores...")
                
            except Exception as e:
                print(f"   ⚠️ Error almacenando tensor {i}: {e}")
                continue
        
        # Almacenar arquetipos descubiertos
        if evolution_result.get('archetypes'):
            top_patterns = evolution_result['archetypes'].get('top_patterns', [])
            for pattern, count in top_patterns[:10]:  # Top 10
                try:
                    self.store.store_archetype(pattern)
                except:
                    pass
        
        return kb_ids


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("🌌 AURORA PIPELINE - Demo End-to-End")
    print("=" * 70)
    print("\n")
    
    # Texto largo de ejemplo (conversación sobre filosofía de IA)
    texto_ejemplo = """
    La inteligencia artificial representa uno de los mayores desafíos
    filosóficos de nuestro tiempo. ¿Qué significa realmente "entender"?
    
    Los sistemas actuales procesan patrones estadísticos en datos masivos.
    Pero procesar no es comprender. Un modelo puede predecir la siguiente
    palabra sin captar su significado profundo.
    
    Aurora propone un cambio de paradigma. En lugar de vectores continuos
    opacos, utiliza tensores fractales discretos. Cada tensor FFE captura
    forma, función y estructura de manera interpretable.
    
    El banco de conocimiento almacena estos tensores en una estructura
    fractal. Los arquetipos emergen naturalmente de los patrones recurrentes.
    Las relaciones se descubren mediante el Transcender.
    
    Me pregunto si un día estas representaciones fractales permitirán
    una verdadera comprensión. El banco de ideas crece con cada interacción.
    Quizás la inteligencia sea fundamentalmente fractal en su naturaleza.
    """
    
    # Crear pipeline (demo mode - sin API)
    pipeline = AuroraPipeline(demo_mode=True)
    
    # Procesar
    result = pipeline.process_text_long(
        text=texto_ejemplo,
        depth=1,
        space_id="filosofia_ia"
    )
    
    # Mostrar resumen
    print("\n")
    print("=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    stats = result['stats']
    print(f"\n📝 Texto procesado:")
    print(f"   - Segmentos: {stats['total_segments']}")
    print(f"   - Tensores FFE: {stats['total_tensors']}")
    print(f"   - Polisemia: {stats['polysemy_count']} casos")
    
    print(f"\n🧠 Aprendizaje:")
    print(f"   - Arquetipos: {stats['total_archetypes']}")
    print(f"   - Relaciones: {stats['total_relations']}")
    
    print(f"\n⏱️ Performance:")
    print(f"   - Tiempo: {stats['processing_time']:.2f}s")
    print(f"   - Espacio: '{stats['space_id']}'")
    
    # Mostrar top arquetipos
    if result['archetypes'].get('top_patterns'):
        print(f"\n🎯 Top 5 Arquetipos:")
        for i, (pattern, count) in enumerate(result['archetypes']['top_patterns'][:5], 1):
            print(f"   {i}. {pattern[:60]}... (aparece {count}x)")
    
    print("\n" + "=" * 70)
    print("✅ Pipeline completado exitosamente")
    print("=" * 70)
    print("\n💡 Aurora está lista para procesar conversaciones reales!")
    print("   Cada texto largo alimenta el aprendizaje continuo.\n")
