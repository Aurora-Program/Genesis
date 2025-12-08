"""
Sequence Encoder - Procesador de texto largo para Aurora
=========================================================

PROBLEMA: 
- Encoder actual procesa texto corto → 1 tensor
- Aurora necesita procesar conversaciones/párrafos → secuencia de tensores

SOLUCIÓN:
- Segmentar texto largo en unidades semánticas
- Cada segmento → tensor FFE con contexto
- Detectar polisemia (misma palabra, múltiples significados)
- Generar secuencia para alimentar Evolver

ARQUITECTURA:
texto_largo → [segmento_1, segmento_2, ..., segmento_n]
           ↓
  LLM Semantic Encoder (con contexto)
           ↓
  [tensor_1, tensor_2, ..., tensor_n]
           ↓
  Evolver (aprende arquetipos, relaciones, dinámicas)
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.llm_semantic_encoder import LLMSemanticEncoder, SemanticMapping
from core.fractal_tensor import FractalTensor


@dataclass
class SemanticSegment:
    """Segmento semántico de texto con contexto"""
    text: str
    start_pos: int
    end_pos: int
    segment_type: str  # "sentence", "clause", "phrase", "token"
    context_before: str
    context_after: str
    polysemy_detected: bool = False
    alternative_meanings: List[str] = None
    
    def __post_init__(self):
        if self.alternative_meanings is None:
            self.alternative_meanings = []


@dataclass
class TensorSequence:
    """Secuencia de tensores FFE con metadata temporal"""
    tensors: List[SemanticMapping]
    original_text: str
    segments: List[SemanticSegment]
    polysemy_count: int
    total_tokens: int
    
    def get_tensor_at(self, position: int) -> Optional[SemanticMapping]:
        """Obtiene tensor en posición específica"""
        if 0 <= position < len(self.tensors):
            return self.tensors[position]
        return None
    
    def get_context_window(self, center: int, window: int = 2) -> List[SemanticMapping]:
        """Obtiene ventana de contexto alrededor de posición"""
        start = max(0, center - window)
        end = min(len(self.tensors), center + window + 1)
        return self.tensors[start:end]


class SequenceEncoder:
    """
    Encoder de secuencias para texto largo.
    
    Funcionalidades:
    1. Segmentación semántica inteligente
    2. Detección de polisemia con contexto
    3. Generación de secuencias FFE
    4. Preservación de contexto entre segmentos
    
    Uso:
        encoder = SequenceEncoder(llm_encoder)
        sequence = encoder.encode_text_long(texto_largo)
        # sequence.tensors → lista de tensores FFE
        # Pasar a Evolver para aprendizaje
    """
    
    def __init__(
        self,
        llm_encoder: LLMSemanticEncoder,
        segmentation_strategy: str = "semantic",  # "semantic", "sentence", "fixed_length"
        min_segment_length: int = 10,
        max_segment_length: int = 200,
        context_window: int = 50,  # chars de contexto antes/después
        detect_polysemy: bool = True
    ):
        self.llm_encoder = llm_encoder
        self.segmentation_strategy = segmentation_strategy
        self.min_segment_length = min_segment_length
        self.max_segment_length = max_segment_length
        self.context_window = context_window
        self.detect_polysemy = detect_polysemy
    
    def encode_text_long(self, text: str, depth: int = 1) -> TensorSequence:
        """
        Procesa texto largo y genera secuencia de tensores FFE.
        
        Flujo:
        1. Segmentar texto en unidades semánticas
        2. Para cada segmento:
           - Extraer contexto antes/después
           - Detectar polisemia si está habilitado
           - Generar tensor(es) FFE con contexto
        3. Construir TensorSequence completa
        
        Args:
            text: Texto largo (párrafo, conversación, documento)
            depth: Profundidad de análisis semántico (1-3)
        
        Returns:
            TensorSequence con todos los tensores + metadata
        """
        print(f"📝 Procesando texto largo ({len(text)} chars)...")
        
        # 1. Segmentar
        segments = self._segment_text(text)
        print(f"   → {len(segments)} segmentos semánticos detectados")
        
        # 2. Detectar polisemia en segmentos
        if self.detect_polysemy:
            segments = self._detect_polysemy_in_segments(segments, text)
            polysemy_count = sum(1 for s in segments if s.polysemy_detected)
            print(f"   → {polysemy_count} casos de polisemia detectados")
        else:
            polysemy_count = 0
        
        # 3. Generar tensores para cada segmento
        tensors = []
        for i, segment in enumerate(segments):
            # Construir texto enriquecido con contexto
            text_with_context = self._build_contextualized_text(segment)
            
            # Encode con LLM
            mapping = self.llm_encoder.encode(text_with_context, depth=depth)
            
            # Agregar metadata del segmento
            mapping.segment_info = {
                "position": i,
                "type": segment.segment_type,
                "has_polysemy": segment.polysemy_detected,
                "alternatives": segment.alternative_meanings
            }
            
            tensors.append(mapping)
            
            if (i + 1) % 10 == 0:
                print(f"   → Procesados {i + 1}/{len(segments)} segmentos...")
        
        print(f"✅ Secuencia completa: {len(tensors)} tensores FFE generados")
        
        # 4. Construir TensorSequence
        return TensorSequence(
            tensors=tensors,
            original_text=text,
            segments=segments,
            polysemy_count=polysemy_count,
            total_tokens=self._count_tokens(text)
        )
    
    def _segment_text(self, text: str) -> List[SemanticSegment]:
        """
        Segmenta texto en unidades semánticas.
        
        Estrategias:
        - "semantic": Cláusulas semánticamente coherentes
        - "sentence": Por oraciones
        - "fixed_length": Ventanas fijas
        """
        if self.segmentation_strategy == "sentence":
            return self._segment_by_sentences(text)
        elif self.segmentation_strategy == "fixed_length":
            return self._segment_fixed_length(text)
        else:  # semantic (default)
            return self._segment_semantic(text)
    
    def _segment_by_sentences(self, text: str) -> List[SemanticSegment]:
        """Segmenta por oraciones usando puntuación"""
        # Regex para detectar fin de oración
        sentence_endings = r'[.!?]+\s+'
        sentences = re.split(sentence_endings, text)
        
        segments = []
        pos = 0
        for sentence in sentences:
            if len(sentence.strip()) < self.min_segment_length:
                continue
            
            # Limitar longitud máxima
            if len(sentence) > self.max_segment_length:
                # Split en sub-oraciones
                sub_segments = self._split_long_sentence(sentence, pos)
                segments.extend(sub_segments)
                pos += len(sentence) + 2  # +2 por ". "
            else:
                segment = SemanticSegment(
                    text=sentence.strip(),
                    start_pos=pos,
                    end_pos=pos + len(sentence),
                    segment_type="sentence",
                    context_before=text[max(0, pos - self.context_window):pos],
                    context_after=text[pos + len(sentence):pos + len(sentence) + self.context_window]
                )
                segments.append(segment)
                pos += len(sentence) + 2
        
        return segments
    
    def _segment_semantic(self, text: str) -> List[SemanticSegment]:
        """
        Segmentación semántica inteligente.
        
        Detecta:
        - Cambios de tema
        - Cláusulas independientes
        - Puntos de coherencia semántica
        """
        # V1: Usar oraciones + análisis de cohesión
        # TODO v2: Usar embeddings para detectar cambios semánticos
        
        # Por ahora, usar sentence + análisis de conectores
        sentence_segments = self._segment_by_sentences(text)
        
        # Fusionar oraciones cortas relacionadas
        merged_segments = []
        buffer = None
        
        for segment in sentence_segments:
            if buffer is None:
                buffer = segment
            elif self._are_semantically_related(buffer.text, segment.text):
                # Fusionar
                buffer.text = buffer.text + " " + segment.text
                buffer.end_pos = segment.end_pos
                buffer.context_after = segment.context_after
            else:
                merged_segments.append(buffer)
                buffer = segment
        
        if buffer:
            merged_segments.append(buffer)
        
        return merged_segments
    
    def _segment_fixed_length(self, text: str) -> List[SemanticSegment]:
        """Segmenta en ventanas de longitud fija"""
        segments = []
        pos = 0
        
        while pos < len(text):
            end = min(pos + self.max_segment_length, len(text))
            
            # Ajustar al final de palabra más cercano
            if end < len(text):
                while end > pos and not text[end].isspace():
                    end -= 1
            
            segment_text = text[pos:end].strip()
            
            if len(segment_text) >= self.min_segment_length:
                segment = SemanticSegment(
                    text=segment_text,
                    start_pos=pos,
                    end_pos=end,
                    segment_type="fixed_window",
                    context_before=text[max(0, pos - self.context_window):pos],
                    context_after=text[end:end + self.context_window]
                )
                segments.append(segment)
            
            pos = end + 1
        
        return segments
    
    def _split_long_sentence(self, sentence: str, start_pos: int) -> List[SemanticSegment]:
        """Split de oraciones muy largas en sub-cláusulas"""
        # Buscar conectores para split natural
        connectors = [', ', '; ', ' y ', ' pero ', ' porque ', ' aunque ']
        
        best_split = None
        best_balance = float('inf')
        
        for conn in connectors:
            if conn in sentence:
                parts = sentence.split(conn, 1)
                balance = abs(len(parts[0]) - len(parts[1]))
                if balance < best_balance:
                    best_balance = balance
                    best_split = parts
        
        if best_split and len(best_split[0]) >= self.min_segment_length:
            # Split recursivo
            return (
                self._split_long_sentence(best_split[0], start_pos) +
                self._split_long_sentence(best_split[1], start_pos + len(best_split[0]))
            )
        else:
            # No se puede split más, retornar como está
            return [SemanticSegment(
                text=sentence[:self.max_segment_length],
                start_pos=start_pos,
                end_pos=start_pos + min(len(sentence), self.max_segment_length),
                segment_type="clause",
                context_before="",
                context_after=""
            )]
    
    def _detect_polysemy_in_segments(
        self,
        segments: List[SemanticSegment],
        full_text: str
    ) -> List[SemanticSegment]:
        """
        Detecta palabras polisémicas y sus significados según contexto.
        
        Ejemplo:
        "El banco está cerrado" vs "Me senté en el banco"
        → Detecta 2 significados de "banco"
        """
        # Palabras polisémicas comunes en español
        polysemous_words = {
            "banco": ["institución financiera", "asiento"],
            "gato": ["animal", "herramienta mecánica"],
            "vela": ["náutica", "iluminación"],
            "clase": ["categoría", "lección educativa"],
            "planta": ["vegetal", "piso de edificio", "parte del pie"],
            "copa": ["recipiente", "competición deportiva", "parte del árbol"],
            "capital": ["ciudad principal", "dinero", "letra mayúscula"],
            "ratón": ["animal", "dispositivo informático"],
            "red": ["malla", "internet", "conjunto organizado"],
            "orden": ["mandato", "organización", "secuencia"],
            "corriente": ["flujo agua/electricidad", "común", "tendencia"],
            "cabo": ["cuerda", "militar", "accidente geográfico"]
        }
        
        for segment in segments:
            words = segment.text.lower().split()
            
            for word in words:
                # Limpiar puntuación
                clean_word = re.sub(r'[^\w\s]', '', word)
                
                if clean_word in polysemous_words:
                    segment.polysemy_detected = True
                    segment.alternative_meanings = polysemous_words[clean_word]
                    break
        
        return segments
    
    def _build_contextualized_text(self, segment: SemanticSegment) -> str:
        """
        Construye texto enriquecido con contexto para el LLM.
        
        Formato:
        [CONTEXTO PREVIO: ...] 
        TEXTO PRINCIPAL: ...
        [CONTEXTO SIGUIENTE: ...]
        """
        parts = []
        
        if segment.context_before:
            parts.append(f"[Contexto previo: {segment.context_before.strip()}]")
        
        parts.append(segment.text)
        
        if segment.context_after:
            parts.append(f"[Contexto siguiente: {segment.context_after.strip()}]")
        
        return " ".join(parts)
    
    def _are_semantically_related(self, text1: str, text2: str) -> bool:
        """
        Heurística simple para detectar relación semántica.
        TODO v2: Usar cosine similarity de embeddings
        """
        # Conectores que indican continuidad
        continuity_markers = [
            "además", "también", "asimismo", "por otro lado",
            "sin embargo", "pero", "aunque", "no obstante",
            "por lo tanto", "entonces", "así que", "de modo que"
        ]
        
        text2_lower = text2.lower()
        for marker in continuity_markers:
            if text2_lower.startswith(marker):
                return True
        
        # Si text2 es muy corto, probablemente continúa text1
        if len(text2) < 50:
            return True
        
        return False
    
    def _count_tokens(self, text: str) -> int:
        """Cuenta tokens aproximados (palabras)"""
        return len(text.split())


# ============================================================================
# DEMO Y TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SEQUENCE ENCODER - Demo con texto largo")
    print("=" * 70 + "\n")
    
    # Texto largo de ejemplo
    texto_largo = """
    La inteligencia artificial ha transformado profundamente nuestra sociedad.
    Los sistemas de aprendizaje automático procesan cantidades masivas de datos
    para extraer patrones y generar predicciones. Sin embargo, estos avances
    plantean importantes desafíos éticos.
    
    Aurora representa un nuevo paradigma en IA. A diferencia de los modelos
    tradicionales que operan con vectores continuos, Aurora utiliza tensores
    fractales discretos. Esta arquitectura permite una representación más
    compacta y semánticamente rica del conocimiento.
    
    El banco de datos almacena millones de transacciones diarias. Los clientes
    pueden consultar su cuenta desde cualquier dispositivo. El banco también
    ofrece servicios de inversión y préstamos hipotecarios.
    
    Me senté en el banco del parque a contemplar el atardecer. El banco de
    madera estaba desgastado por el tiempo. Junto al banco había una fuente
    con agua cristalina.
    """
    
    # Crear encoder (en demo mode, sin API real)
    from pipeline.llm_semantic_encoder import LLMSemanticEncoder
    
    llm_encoder = LLMSemanticEncoder(demo_mode=True)
    sequence_encoder = SequenceEncoder(
        llm_encoder=llm_encoder,
        segmentation_strategy="semantic",
        detect_polysemy=True
    )
    
    # Procesar texto largo
    print("🔄 Procesando texto largo...\n")
    sequence = sequence_encoder.encode_text_long(texto_largo, depth=1)
    
    # Mostrar resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    print(f"\n📝 Texto original: {len(sequence.original_text)} caracteres")
    print(f"🔢 Total tokens: {sequence.total_tokens}")
    print(f"📦 Segmentos procesados: {len(sequence.segments)}")
    print(f"🎯 Tensores FFE generados: {len(sequence.tensors)}")
    print(f"🔀 Casos de polisemia: {sequence.polysemy_count}")
    
    # Mostrar primeros 5 segmentos
    print("\n" + "=" * 70)
    print("🔍 PRIMEROS 5 SEGMENTOS")
    print("=" * 70)
    for i, segment in enumerate(sequence.segments[:5]):
        print(f"\n[Segmento {i + 1}]")
        print(f"  Texto: {segment.text}")
        print(f"  Tipo: {segment.segment_type}")
        print(f"  Posición: {segment.start_pos}-{segment.end_pos}")
        if segment.polysemy_detected:
            print(f"  ⚠️ Polisemia detectada: {segment.alternative_meanings}")
        
        # Mostrar tensor asociado
        tensor_mapping = sequence.tensors[i]
        print(f"  Tensor FFE: {tensor_mapping.tensor.nivel_3}")
        print(f"  Related: {tensor_mapping.related_content[:2]}")
    
    # Ejemplo de ventana de contexto
    print("\n" + "=" * 70)
    print("🪟 VENTANA DE CONTEXTO (tensor 2 ± 2)")
    print("=" * 70)
    context_window = sequence.get_context_window(center=2, window=2)
    for i, mapping in enumerate(context_window):
        segment_info = mapping.segment_info if hasattr(mapping, 'segment_info') else {}
        pos = segment_info.get('position', '?')
        print(f"\n  Posición {pos}: {sequence.segments[pos].text[:60]}...")
    
    print("\n" + "=" * 70)
    print("✅ Demo completada")
    print("=" * 70)
    print("\n💡 SIGUIENTE PASO:")
    print("   Pasar sequence.tensors a Evolver para aprender:")
    print("   - Arquetipos (patrones recurrentes)")
    print("   - Relaciones (conexiones entre tensores)")
    print("   - Dinámicas (evolución temporal)")
