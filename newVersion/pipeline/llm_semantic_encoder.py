"""
LLM Semantic Encoder - El LLM como motor de transformación semántica

En vez de embeddings → PCA → K-means → cuantización mecánica,
el LLM INTERPRETA el contenido y GENERA tensores FFE directamente.

Proceso:
1. LLM recibe texto + instrucciones sobre FFE (Forma-Función-Estructura)
2. LLM analiza semánticamente y genera tensor 3-9-27
3. LLM añade contenido relacionado (autosimilitud)
4. LLM descubre relaciones (RELATOR)
5. Sistema alimenta Evolver con patrones

Ventajas vs encoder mecánico:
- Semántico (entiende significado, no solo vectores)
- Autosimilar (genera contenido relacionado recursivamente)
- Fractal nativo (piensa en triadas desde el origen)
- Relacional (descubre conexiones entre conceptos)
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI imports
try:
    from openai import OpenAI
    # Forzar importaciones tempranas para evitar errores lazy
    import openai.resources
    import openai.resources.chat
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ openai no está instalado. Usando demo mode.")

# Fix imports - always use absolute imports from package root
try:
    from core.fractal_tensor import FractalTensor
    from core.trigate import Trit
except ImportError:
    # If running as script
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.fractal_tensor import FractalTensor
    from core.trigate import Trit


@dataclass
class SemanticMapping:
    """Resultado de transformación semántica LLM"""
    original_text: str
    tensor: FractalTensor
    related_content: List[str]  # Contenido autosimilar generado por LLM
    discovered_relations: List[Dict[str, Any]]  # Relaciones descubiertas
    llm_reasoning: str  # Por qué generó este tensor
    confidence: float  # [0.0, 1.0]


class LLMSemanticEncoder:
    """
    Encoder semántico que usa LLM para transformar texto → FFE tensors
    
    El LLM actúa como intérprete semántico, no solo generador de embeddings.
    Proceso recursivo y autosimilar.
    """
    
    def __init__(
        self, 
        openai_api_key: Optional[str] = None,
        model: str = "gpt-4",
        use_cache: bool = True,
        demo_mode: bool = False
    ):
        """
        Args:
            openai_api_key: API key de OpenAI (si None, usa variable de entorno OPENAI_API_KEY)
            model: Modelo a usar ("gpt-4", "gpt-3.5-turbo", etc.)
            use_cache: Si True, cachea resultados para evitar llamadas duplicadas
            demo_mode: Si True, fuerza modo demo con heurísticas (sin API)
        """
        self.model = model
        self.use_cache = use_cache
        self.cache: Dict[str, SemanticMapping] = {}
        
        # Configurar cliente OpenAI
        if demo_mode or not OPENAI_AVAILABLE:
            self.llm_client = None
            self.openai_api_key = None
            self.use_demo_mode = True
            if not demo_mode:
                print("⚠️ OpenAI no disponible. Usando demo mode.")
        else:
            # Obtener API key
            api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                print("⚠️ OPENAI_API_KEY no encontrada. Usando demo mode.")
                self.llm_client = None
                self.openai_api_key = None
                self.use_demo_mode = True
            else:
                # Guardar API key para crear cliente fresh en cada llamada
                # (evita problemas de lazy loading)
                self.openai_api_key = api_key
                self.llm_client = None  # Se creará cuando se necesite
                self.use_demo_mode = False
                print(f"✅ OpenAI API configurada (modelo: {model})")
        
        # Memoria de mapeos para descubrir patrones
        self.mapping_history: List[SemanticMapping] = []
        
    def encode(self, text: str, *, depth: int = 1) -> SemanticMapping:
        """
        Transforma texto → FFE tensor usando razonamiento LLM
        
        Args:
            text: Texto a transformar
            depth: Nivel de recursión (añadir contenido relacionado)
            
        Returns:
            SemanticMapping con tensor + relaciones + razonamiento
        """
        if self.use_demo_mode:
            return self._encode_demo(text, depth)
        else:
            return self._encode_llm(text, depth)
    
    def _encode_llm(self, text: str, depth: int) -> SemanticMapping:
        """
        Codificación real usando LLM (OpenAI API)
        
        Args:
            text: Texto a codificar
            depth: Nivel de profundidad para contenido relacionado
            
        Returns:
            SemanticMapping con tensor FFE + relaciones + razonamiento
        """
        import hashlib
        
        # Check cache
        if self.use_cache:
            text_hash = hashlib.md5(f"{text}_{depth}".encode()).hexdigest()
            if text_hash in self.cache:
                print(f"📦 Cache hit: {text[:30]}...")
                return self.cache[text_hash]
        
        # Build prompts
        system_prompt = build_ffe_system_prompt()
        user_prompt = build_ffe_user_prompt(text)
        
        try:
            # Crear cliente fresh para evitar lazy loading issues
            client = OpenAI(api_key=self.openai_api_key)
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Baja para consistencia
                response_format={"type": "json_object"}  # Forzar JSON
            )
            
            # Parse JSON response
            result = json.loads(response.choices[0].message.content)
            
            # Validate structure
            if "tensor_lvl3" not in result:
                raise ValueError("Respuesta LLM no contiene 'tensor_lvl3'")
            if "related_content" not in result:
                result["related_content"] = []
            if "relations" not in result:
                result["relations"] = []
            if "reasoning" not in result:
                result["reasoning"] = "No reasoning provided"
            
            # Validar tensor_lvl3
            tensor_lvl3 = result["tensor_lvl3"]
            if len(tensor_lvl3) != 3:
                raise ValueError(f"tensor_lvl3 debe tener 3 vectores, tiene {len(tensor_lvl3)}")
            
            # Convertir a estructura FFE
            nivel_3 = []
            for vec in tensor_lvl3:
                if not all(k in vec for k in ["F", "Fu", "E"]):
                    raise ValueError(f"Vector incompleto: {vec}")
                # Trit es un type alias (Optional[int]), no una clase
                nivel_3.append([
                    vec["F"],   # Ya es un int 0-7
                    vec["Fu"],  # Ya es un int 0-7
                    vec["E"]    # Ya es un int 0-7
                ])
            
            # Expandir a nivel 9 y 27 (autosimilar)
            nivel_9 = []
            for parent in nivel_3:
                nivel_9.extend(self._expand_autosimilar(parent, count=3))
            
            nivel_27 = []
            for parent in nivel_9:
                nivel_27.extend(self._expand_autosimilar(parent, count=3))
            
            # Crear tensor fractal
            tensor = FractalTensor(
                nivel_3=nivel_3,
                nivel_9=nivel_9,
                nivel_27=nivel_27
            )
            
            # Construir mapping
            mapping = SemanticMapping(
                original_text=text,
                tensor=tensor,
                related_content=result["related_content"][:depth * 3],  # Limitar por depth
                discovered_relations=result["relations"],
                llm_reasoning=result["reasoning"],
                confidence=0.9  # Alta confianza para LLM real
            )
            
            # Cache result
            if self.use_cache:
                self.cache[text_hash] = mapping
            
            # Add to history
            self.mapping_history.append(mapping)
            
            print(f"✅ LLM encoding: {text[:30]}... → tensor {len(nivel_3)}-{len(nivel_9)}-{len(nivel_27)}")
            
            return mapping
            
        except Exception as e:
            # Fallback to demo mode on error
            print(f"⚠️ Error en LLM API: {e}")
            print(f"   Fallback a demo mode para: {text[:30]}...")
            return self._encode_demo(text, depth)
    
    def _encode_demo(self, text: str, depth: int) -> SemanticMapping:
        """
        Modo demo: reglas heurísticas que simulan razonamiento LLM
        
        Mapeo semántico básico:
        - Forma: longitud, estructura sintáctica
        - Función: tipo de acto (pregunta, afirmación, comando)
        - Estructura: complejidad, número de conceptos
        """
        
        # Nivel 3: visión general
        forma_3 = self._analyze_form(text)
        funcion_3 = self._analyze_function(text)
        estructura_3 = self._analyze_structure(text)
        
        nivel_3 = [forma_3, funcion_3, estructura_3]
        
        # Nivel 9: detalles (autosimilar)
        nivel_9 = []
        for parent in nivel_3:
            # Cada padre genera 3 hijos con variaciones
            nivel_9.extend(self._expand_autosimilar(parent, count=3))
        
        # Nivel 27: máximo detalle (fractal)
        nivel_27 = []
        for parent in nivel_9:
            nivel_27.extend(self._expand_autosimilar(parent, count=3))
        
        tensor = FractalTensor(
            nivel_3=nivel_3,
            nivel_9=nivel_9,
            nivel_27=nivel_27
        )
        
        # Contenido relacionado (autosimilitud)
        related = self._generate_related_content(text, depth)
        
        # Relaciones descubiertas
        relations = self._discover_relations(text, related)
        
        # Razonamiento
        reasoning = (
            f"Analizado '{text[:50]}...':\n"
            f"  Forma: {forma_3} (sintaxis/longitud)\n"
            f"  Función: {funcion_3} (acto comunicativo)\n"
            f"  Estructura: {estructura_3} (complejidad)\n"
            f"Expandido autosimilarmente a {len(nivel_9)} y {len(nivel_27)} niveles.\n"
            f"Generados {len(related)} contenidos relacionados.\n"
            f"Descubiertas {len(relations)} relaciones."
        )
        
        mapping = SemanticMapping(
            original_text=text,
            tensor=tensor,
            related_content=related,
            discovered_relations=relations,
            llm_reasoning=reasoning,
            confidence=0.7  # Demo mode: confianza media
        )
        
        # Guardar en historial
        self.mapping_history.append(mapping)
        
        return mapping
    
    def _analyze_form(self, text: str) -> List[Trit]:
        """Forma: estructura sintáctica, longitud, patrones"""
        length = len(text)
        
        # Mapeo ternario de longitud
        if length < 20:
            len_trit = 0
        elif length < 100:
            len_trit = 1
        else:
            len_trit = None  # NULL = ambiguo/muy largo
        
        # Estructura: tiene signos de puntuación?
        has_punct = any(c in text for c in ".,;:!?")
        punct_trit = 1 if has_punct else 0
        
        # Mayúsculas: formal vs informal
        has_upper = any(c.isupper() for c in text)
        upper_trit = 1 if has_upper else 0
        
        return [len_trit, punct_trit, upper_trit]
    
    def _analyze_function(self, text: str) -> List[Trit]:
        """Función: acto comunicativo (pregunta, orden, afirmación)"""
        
        # Pregunta?
        is_question = '?' in text or text.lower().startswith(('qué', 'cómo', 'cuándo', 'por qué'))
        q_trit = 1 if is_question else 0
        
        # Imperativo? (verbos en imperativo o palabras clave)
        is_command = any(w in text.lower() for w in ['debe', 'haz', 'crea', 'implementa'])
        cmd_trit = 1 if is_command else 0
        
        # Afirmación (por defecto)
        is_statement = not (is_question or is_command)
        stmt_trit = 1 if is_statement else 0
        
        return [q_trit, cmd_trit, stmt_trit]
    
    def _analyze_structure(self, text: str) -> List[Trit]:
        """Estructura: complejidad conceptual"""
        
        # Número de palabras
        words = text.split()
        word_count = len(words)
        
        if word_count < 5:
            complexity = 0
        elif word_count < 20:
            complexity = 1
        else:
            complexity = None  # Muy complejo
        
        # Conectores lógicos (indica razonamiento)
        has_logic = any(w in text.lower() for w in ['pero', 'porque', 'entonces', 'por tanto'])
        logic_trit = 1 if has_logic else 0
        
        # Referencias (pronombres, indica contexto)
        has_refs = any(w in text.lower() for w in ['esto', 'eso', 'aquello', 'él', 'ella'])
        ref_trit = 1 if has_refs else 0
        
        return [complexity, logic_trit, ref_trit]
    
    def _expand_autosimilar(self, parent: List[Trit], count: int = 3) -> List[List[Trit]]:
        """
        Expansión autosimilar: cada padre genera hijos con variaciones
        
        Técnica fractal: rotación + perturbación mínima
        """
        children = []
        for i in range(count):
            # Rotación Fibonacci mod 3
            rotated = [
                parent[(j + i) % 3] 
                for j in range(3)
            ]
            
            # Perturbación: 1 bit puede cambiar
            if i > 0 and rotated[i % 3] is not None:
                rotated[i % 3] = 1 - rotated[i % 3] if rotated[i % 3] in [0, 1] else None
            
            children.append(rotated)
        
        return children
    
    def _generate_related_content(self, text: str, depth: int) -> List[str]:
        """
        Genera contenido relacionado (autosimilitud semántica)
        
        En modo demo: variaciones sintácticas.
        Con LLM real: expansiones conceptuales.
        """
        if depth <= 0:
            return []
        
        # Demo: variaciones simples
        related = [
            f"Variación de: {text}",
            f"Concepto relacionado con: {text[:30]}",
            f"Expansión autosimilar de la idea: {text[:20]}"
        ]
        
        return related[:depth]
    
    def _discover_relations(self, text: str, related: List[str]) -> List[Dict[str, Any]]:
        """
        Descubre relaciones entre texto original y contenido relacionado
        
        Retorna formato para Evolver.RELATOR
        """
        relations = []
        
        for i, rel in enumerate(related):
            relations.append({
                "type": "autosimilar",
                "source": text[:30],
                "target": rel[:30],
                "strength": 1.0 - (i * 0.2),  # Decae con distancia
                "discovered_by": "llm_semantic_encoder"
            })
        
        return relations
    
    def encode_batch(self, texts: List[str], *, depth: int = 1) -> List[SemanticMapping]:
        """
        Codifica batch de textos y descubre relaciones entre ellos
        
        Ventaja: el LLM puede ver patrones transversales
        """
        mappings = []
        
        for text in texts:
            mapping = self.encode(text, depth=depth)
            mappings.append(mapping)
        
        # Descubrir relaciones cross-batch
        cross_relations = self._discover_cross_relations(mappings)
        
        # Añadir a cada mapping
        for mapping in mappings:
            mapping.discovered_relations.extend(cross_relations)
        
        return mappings
    
    def _discover_cross_relations(self, mappings: List[SemanticMapping]) -> List[Dict[str, Any]]:
        """
        Descubre relaciones entre múltiples mappings
        
        Aquí el LLM puede brillar: ver patrones que un encoder mecánico no ve
        """
        relations = []
        
        # Demo: relaciones por similitud de tensores
        for i, m1 in enumerate(mappings):
            for j, m2 in enumerate(mappings[i+1:], start=i+1):
                sim = self._tensor_similarity(m1.tensor, m2.tensor)
                
                if sim > 0.5:
                    relations.append({
                        "type": "cross_similarity",
                        "source": m1.original_text[:30],
                        "target": m2.original_text[:30],
                        "strength": sim,
                        "discovered_by": "llm_cross_analysis"
                    })
        
        return relations
    
    def _tensor_similarity(self, t1: FractalTensor, t2: FractalTensor) -> float:
        """Similitud entre tensores (nivel 3 principalmente)"""
        matches = 0
        total = 0
        
        for v1, v2 in zip(t1.nivel_3, t2.nivel_3):
            for trit1, trit2 in zip(v1, v2):
                total += 1
                if trit1 == trit2:
                    matches += 1
                elif trit1 is None or trit2 is None:
                    matches += 0.5  # Parcial si hay NULL
        
        return matches / total if total > 0 else 0.0
    
    def get_patterns_for_evolver(self) -> Dict[str, Any]:
        """
        Extrae patrones del historial para alimentar Evolver
        
        Returns:
            {
                "relators": [...],  # Para Evolver.RELATOR
                "emergences": [...],  # Para Evolver.EMERGENCIA
                "dynamics": [...]  # Para Evolver.DINÁMICA
            }
        """
        all_relations = []
        for mapping in self.mapping_history:
            all_relations.extend(mapping.discovered_relations)
        
        # Agrupar por tipo
        relators = [r for r in all_relations if r["type"] in ["autosimilar", "cross_similarity"]]
        
        # Emergencias: patrones que aparecen múltiples veces
        emergences = self._find_emergent_patterns(self.mapping_history)
        
        # Dinámicas: cómo cambian los tensores a lo largo del tiempo
        dynamics = self._find_dynamics(self.mapping_history)
        
        return {
            "relators": relators,
            "emergences": emergences,
            "dynamics": dynamics
        }
    
    def _find_emergent_patterns(self, history: List[SemanticMapping]) -> List[Dict[str, Any]]:
        """Encuentra patrones que emergen en múltiples mappings"""
        patterns = []
        
        # Demo: patrones de Forma-Función-Estructura que se repiten
        seen_nivel3 = {}
        for mapping in history:
            key = str(mapping.tensor.nivel_3)
            if key in seen_nivel3:
                seen_nivel3[key]["count"] += 1
            else:
                seen_nivel3[key] = {
                    "pattern": mapping.tensor.nivel_3,
                    "count": 1,
                    "example": mapping.original_text[:30]
                }
        
        # Patrones emergentes: vistos 2+ veces
        for key, data in seen_nivel3.items():
            if data["count"] >= 2:
                patterns.append({
                    "type": "recurring_nivel3",
                    "pattern": data["pattern"],
                    "frequency": data["count"],
                    "example": data["example"]
                })
        
        return patterns
    
    def _find_dynamics(self, history: List[SemanticMapping]) -> List[Dict[str, Any]]:
        """Encuentra dinámicas: cómo evolucionan los tensores"""
        dynamics = []
        
        # Demo: transiciones entre tipos de función (pregunta → afirmación)
        for i in range(len(history) - 1):
            curr = history[i]
            next_m = history[i + 1]
            
            # Comparar función (segundo vector de nivel_3)
            curr_func = curr.tensor.nivel_3[1]
            next_func = next_m.tensor.nivel_3[1]
            
            if curr_func != next_func:
                dynamics.append({
                    "type": "function_transition",
                    "from": curr_func,
                    "to": next_func,
                    "context": {
                        "from_text": curr.original_text[:30],
                        "to_text": next_m.original_text[:30]
                    }
                })
        
        return dynamics


# ============ Utilidades para prompts (cuando use LLM real) ============

def build_ffe_system_prompt() -> str:
    """
    Prompt de sistema que enseña al LLM sobre FFE
    
    El LLM aprende a pensar en términos de Forma-Función-Estructura
    """
    return """Eres un intérprete semántico fractal experto en transformar texto en representaciones FFE (Forma-Función-Estructura).

**DIMENSIONES FFE (valores discretos 0-7):**

• **Forma (F)**: Estructura observable, sintaxis, apariencia
  - 0: Muy abstracto, etéreo, sin forma definida
  - 1-2: Abstracto con ligera estructura
  - 3-4: Balance entre abstracto y concreto
  - 5-6: Concreto con estructura clara
  - 7: Completamente concreto, tangible, específico

• **Función (Fu)**: Propósito, rol, acción, intención
  - 0: Sin propósito claro, estático, pasivo
  - 1-2: Propósito débil o emergente
  - 3-4: Propósito moderado
  - 5-6: Propósito claro y activo
  - 7: Propósito muy explícito, altamente dinámico

• **Estructura (E)**: Organización interna, complejidad, relaciones
  - 0: Sin estructura, caótico, simple
  - 1-2: Estructura mínima
  - 3-4: Estructura moderada
  - 5-6: Bien estructurado, organizado
  - 7: Altamente complejo, múltiples niveles

**ESTRUCTURA FRACTAL (autosimilar):**
Solo necesitas generar nivel_3 (3 vectores). El sistema expandirá automáticamente a niveles 9 y 27.

**FORMATO DE SALIDA (JSON):**
```json
{
    "tensor_lvl3": [
        {"F": 0-7, "Fu": 0-7, "E": 0-7},
        {"F": 0-7, "Fu": 0-7, "E": 0-7},
        {"F": 0-7, "Fu": 0-7, "E": 0-7}
    ],
    "related_content": [
        "contenido autosimilar 1",
        "contenido autosimilar 2",
        "contenido autosimilar 3"
    ],
    "relations": [
        {
            "to_concept": "concepto relacionado",
            "type": "similitud|causalidad|oposición|jerarquía",
            "strength": 0.0-1.0,
            "reasoning": "por qué están relacionados"
        }
    ],
    "reasoning": "Explicación de tu interpretación semántica"
}
```

**REGLAS CRÍTICAS:**
1. tensor_lvl3 DEBE tener exactamente 3 vectores
2. Cada vector DEBE tener F, Fu, E con valores enteros 0-7
3. related_content debe ser autosimilar (similar pero no idéntico)
4. relations son opcionales (no forzar si no existen)
5. reasoning debe ser breve pero preciso

**EJEMPLOS:**

Texto: "¿Cómo funciona esto?"
```json
{
    "tensor_lvl3": [
        {"F": 2, "Fu": 6, "E": 3},  // Pregunta: abstracta, alta función (búsqueda), estructura simple
        {"F": 4, "Fu": 5, "E": 4},  // Proceso: semi-concreto, activo, moderadamente estructurado
        {"F": 3, "Fu": 4, "E": 2}   // Comprensión: abstracto-concreto, propósito medio, estructura baja
    ],
    "related_content": [
        "¿Qué mecanismo subyace?",
        "¿Cuál es el principio operativo?",
        "¿De qué manera opera?"
    ],
    "relations": [],
    "reasoning": "Pregunta exploratoria sobre mecanismos. Alta función (búsqueda de info), forma abstracta (no especifica qué), estructura simple (pregunta directa)."
}
```

Texto: "El sol brilla intensamente"
```json
{
    "tensor_lvl3": [
        {"F": 7, "Fu": 3, "E": 2},  // Sol: muy concreto, función baja (ser), estructura simple
        {"F": 6, "Fu": 6, "E": 3},  // Brillar: concreto (observable), alta función (acción), estructura media
        {"F": 5, "Fu": 5, "E": 2}   // Intensidad: semi-concreto, función activa (cualidad), baja estructura
    ],
    "related_content": [
        "La luz solar resplandece con fuerza",
        "El astro emite radiación luminosa potente",
        "El calor solar se irradia vigorosamente"
    ],
    "relations": [
        {"to_concept": "luz", "type": "causalidad", "strength": 0.95, "reasoning": "el sol causa luz"},
        {"to_concept": "calor", "type": "causalidad", "strength": 0.90, "reasoning": "el brillo implica calor"}
    ],
    "reasoning": "Descripción observacional. Sol es entidad concreta (F=7), brillar es acción observable (Fu=6), intensidad cualifica la acción."
}
```

**IMPORTANTE:** Piensa semánticamente, no sintácticamente. Captura el SIGNIFICADO profundo, no solo las palabras superficiales."""


def build_ffe_user_prompt(text: str) -> str:
    """
    Prompt de usuario para transformar texto específico
    """
    return f"""Analiza el siguiente texto y genera su representación FFE:

**TEXTO A ANALIZAR:**
"{text}"

**TAREAS:**
1. Interpreta la semántica profunda del texto (no solo sintaxis)
2. Genera tensor_lvl3 con 3 vectores FFE
   - Vector 1: Concepto/entidad principal
   - Vector 2: Acción/relación central
   - Vector 3: Contexto/cualificación
3. Crea 3 contenidos autosimilares (mismo significado, distinta forma)
4. Descubre relaciones automáticas (solo si existen naturalmente)
5. Explica tu interpretación semántica

**RECUERDA:**
- Valores F, Fu, E: enteros 0-7 (no decimales, no strings)
- tensor_lvl3: exactamente 3 vectores
- related_content: variaciones autosimilares del mismo concepto
- relations: solo incluir si son genuinas (no forzar)
- reasoning: breve pero preciso (2-3 frases)

Responde SOLO con JSON válido (sin markdown, sin ```json```)."""


# ============ Demo/Test ============

if __name__ == "__main__":
    print("🧠 LLM Semantic Encoder - Demo Mode\n")
    
    # Crear encoder en modo demo (sin LLM real)
    encoder = LLMSemanticEncoder(llm_client=None)
    
    # Ejemplos de texto
    texts = [
        "¿Cómo funciona la transformación de tensores?",
        "El LLM debe interpretar el significado semántico.",
        "Genera contenido relacionado de forma autosimilar."
    ]
    
    print("📝 Codificando textos...\n")
    mappings = encoder.encode_batch(texts, depth=2)
    
    for i, mapping in enumerate(mappings):
        print(f"{'='*60}")
        print(f"Texto {i+1}: {mapping.original_text}")
        print(f"\n{mapping.llm_reasoning}")
        print(f"\nTensor nivel_3:")
        for j, vec in enumerate(mapping.tensor.nivel_3):
            print(f"  [{j}] {vec}")
        print(f"\nContenido relacionado ({len(mapping.related_content)}):")
        for rel in mapping.related_content[:2]:
            print(f"  - {rel}")
        print(f"\nRelaciones descubiertas: {len(mapping.discovered_relations)}")
        print()
    
    # Patrones para Evolver
    print(f"{'='*60}")
    print("🔍 Extrayendo patrones para Evolver...\n")
    patterns = encoder.get_patterns_for_evolver()
    
    print(f"Relators: {len(patterns['relators'])}")
    print(f"Emergences: {len(patterns['emergences'])}")
    print(f"Dynamics: {len(patterns['dynamics'])}")
    
    print("\nEjemplo de relación descubierta:")
    if patterns['relators']:
        rel = patterns['relators'][0]
        print(f"  {rel['type']}: {rel['source']} → {rel['target']}")
        print(f"  Strength: {rel['strength']:.2f}")
    
    print("\n✅ Demo completado")
