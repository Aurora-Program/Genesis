# Arquitectura LLM-Driven: El LLM como Motor Semántico

## Cambio de Paradigma

### ❌ Enfoque Mecánico (v0.1)
```
Texto → Embedding (768 dims)
         ↓
      PCA (81 dims) ← pérdida de 61% varianza
         ↓
    K-means (27 clusters) ← silhouette = -0.009
         ↓
  Cuantización (trits) ← 30% NULLs
         ↓
    FFE Tensor ← cosine_sim = 0.115 ❌
```

**Problemas:**
- **Semántica perdida**: PCA no entiende significado
- **Clusters incoherentes**: K-means agrupa por distancia euclidiana, no semántica
- **Sin contexto**: Cada embedding es independiente
- **Sin relaciones**: No descubre conexiones entre conceptos
- **GIGO**: Garbage In = Garbage Out (0.115 vs 0.85 objetivo)

---

### ✅ Enfoque Semántico (v2.0 - LLM-driven)
```
Texto → LLM interpreta
         ↓
    Razonamiento FFE (Forma-Función-Estructura)
         ↓
    Genera Tensor 3-9-27 ← directamente semántico
         ↓
    Añade contenido relacionado (autosimilitud)
         ↓
    Descubre relaciones (RELATOR)
         ↓
    Alimenta Evolver (patrones)
         ↓
    Aurora aprende y evoluciona
```

**Ventajas:**
- ✅ **Semántico nativo**: LLM entiende significado
- ✅ **Autosimilar**: Genera contenido relacionado recursivamente
- ✅ **Relacional**: Descubre conexiones conceptuales
- ✅ **Contextual**: Usa conocimiento previo del LLM
- ✅ **Fractal**: Piensa en triadas desde el origen
- ✅ **Emergente**: Patrones aparecen naturalmente

---

## Arquitectura Completa

### 1. LLM Semantic Encoder (nuevo componente)

**Responsabilidad:** Transformar texto → FFE tensor usando razonamiento semántico.

```python
from newVersion.pipeline.llm_semantic_encoder import LLMSemanticEncoder

# Configurar con LLM real (OpenAI, Anthropic, local)
encoder = LLMSemanticEncoder(llm_client=openai_client)

# Transformar texto
mapping = encoder.encode(
    "¿Cómo funciona la transformación de tensores?",
    depth=2  # Recursión: añade contenido relacionado
)

# Resultado
mapping.tensor           # FractalTensor 3-9-27
mapping.related_content  # Lista de conceptos autosimilares
mapping.discovered_relations  # Relaciones para RELATOR
mapping.llm_reasoning    # Por qué generó este tensor
mapping.confidence       # [0.0, 1.0]
```

**Prompt para el LLM:**
```
Sistema: Eres un encoder semántico fractal.
         Transforma texto en tensores FFE (Forma-Función-Estructura).
         Piensa de forma recursiva y autosimilar.
         
Usuario: Transforma: "¿Cómo funciona la transformación?"
         Genera:
         1. nivel_3: [Forma, Función, Estructura]
         2. nivel_9: expansión autosimilar (3 hijos por padre)
         3. nivel_27: expansión fractal completa
         4. related_content: conceptos relacionados
         5. relations: conexiones descubiertas
         6. reasoning: explica tu análisis
```

**Salida del LLM:**
```json
{
  "nivel_3": [
    [1, 1, 1],  // Forma: pregunta, puntuación, formal
    [1, 0, 0],  // Función: interrogativa, no imperativa, no afirmativa
    [1, 1, 0]   // Estructura: compleja, lógica (cómo→funcionamiento)
  ],
  "nivel_9": [...],  // Expansión autosimilar
  "nivel_27": [...], // Detalle fractal
  "related_content": [
    "¿Qué es un tensor FFE?",
    "Proceso de transformación semántica",
    "Diferencia entre embedding y tensor fractal"
  ],
  "relations": [
    {
      "type": "prerequisite",
      "source": "transformación",
      "target": "tensor FFE",
      "strength": 0.9
    }
  ],
  "reasoning": "La pregunta busca comprender un proceso técnico..."
}
```

---

### 2. Integración con Evolver

**El LLM alimenta los 3 bancos del Evolver:**

```python
# Después de codificar batch de textos
mappings = encoder.encode_batch(texts, depth=2)

# Extraer patrones
patterns = encoder.get_patterns_for_evolver()

# Alimentar Evolver
evolver = Evolver3(threshold=2)

# RELATOR: relaciones descubiertas por el LLM
for rel in patterns['relators']:
    evolver.observe_relation(
        source_tensor=...,
        target_tensor=...,
        relation_type=rel['type'],
        strength=rel['strength']
    )

# EMERGENCIA: patrones recurrentes
for emerg in patterns['emergences']:
    evolver.observe_emergence(
        M1=emerg['pattern'][0],
        M2=emerg['pattern'][1],
        M3=emerg['pattern'][2],
        Ms=emerg['synthesized']
    )

# DINÁMICA: transiciones temporales
for dyn in patterns['dynamics']:
    evolver.observe_dynamics_round(
        [dyn['from'], dyn['to']],
        level_tag=dyn['context']
    )
```

---

### 3. Ciclo Completo: Aurora Aprende

```
Usuario: "Explica la coherencia en Trinity-3"
   ↓
LLM Encoder: 
   - Interpreta: pregunta técnica sobre concepto avanzado
   - Genera tensor FFE con alta estructura (NULL en algunos bits = ambigüedad)
   - Añade contenido relacionado:
     * "¿Qué es Trinity-3?"
     * "Coherencia absoluta top-down"
     * "Harmonizer: 5 niveles de reparación"
   - Descubre relaciones:
     * coherencia → harmonizer (dependency)
     * Trinity-3 → trigate (component_of)
   ↓
Transcender:
   - Combina tensores FFE del usuario + contexto recuperado
   - Sintetiza Ms (nueva comprensión)
   - Aplica Harmonizer (repara NULLs)
   ↓
Evolver:
   - Registra en RELATOR: "coherencia se relaciona con harmonizer"
   - Detecta EMERGENCIA: "preguntas técnicas → alta estructura"
   - Aprende DINÁMICA: "pregunta → explicación → profundización"
   ↓
Aurora responde: "La coherencia en Trinity-3..."
   ↓
LLM Encoder codifica respuesta:
   - Tensor FFE de la respuesta
   - Relaciones: respuesta → pregunta (answers)
   ↓
Evolver actualiza:
   - Refuerza patrones de Q&A técnico
   - Aprende estilo de explicación
   ↓
Próxima vez: Aurora usa estos patrones para responder mejor
```

---

## Comparación: Mecánico vs Semántico

| Aspecto | Encoder Mecánico (v0.1) | LLM Semantic (v2.0) |
|---------|-------------------------|---------------------|
| **Entrada** | Embedding 768D | Texto + contexto |
| **Proceso** | PCA → K-means → cuantización | Razonamiento semántico |
| **Salida** | Tensor FFE (0.115 sim ❌) | Tensor FFE + relaciones + reasoning |
| **Semántica** | Perdida (61% varianza) | Preservada (LLM entiende) |
| **Relaciones** | No detecta | Descubre activamente |
| **Autosimilitud** | No genera | Genera contenido relacionado |
| **Contexto** | Independiente | Usa conocimiento previo |
| **Interpretabilidad** | Caja negra | Razonamiento explícito |
| **Calidad** | 0.115 cosine_sim | ? (esperable > 0.85) |

---

## Implementación Práctica

### Fase 1: Demo Mode (actual) ✅

```python
# Sin LLM real: reglas heurísticas
encoder = LLMSemanticEncoder(llm_client=None)
mapping = encoder.encode("texto")
# Salida: tensor básico, relaciones simples
```

**Estado:** Implementado y funcionando.  
**Validación:** Demo genera tensores 3-9-27, contenido relacionado, relaciones.

---

### Fase 2: LLM Integration (próximo paso)

```python
# Con LLM real
import openai

client = openai.OpenAI(api_key=...)
encoder = LLMSemanticEncoder(llm_client=client)

# El LLM razona y genera tensor
mapping = encoder.encode("¿Cómo funciona?")
```

**Tareas:**
1. Implementar `_encode_llm()` con llamada a API
2. Refinar prompts (system + user)
3. Parsear respuesta JSON del LLM
4. Validar calidad de tensores generados
5. Medir cosine_sim vs embeddings originales

**Estimación:** 2-3 semanas con validación.

---

### Fase 3: Recursive Expansion (autosimilitud)

```python
# Profundidad 1: genera 3-5 conceptos relacionados
mapping = encoder.encode("texto", depth=1)

# Profundidad 2: cada relacionado genera más relacionados
mapping = encoder.encode("texto", depth=2)

# Profundidad 3: árbol fractal completo
mapping = encoder.encode("texto", depth=3)
```

**Resultado:** Árbol autosimilar de conceptos relacionados.

**Ventaja:** Evolver aprende relaciones transversales, no solo lineales.

---

### Fase 4: Cross-Batch Learning (patrones emergentes)

```python
# Batch de conversación
texts = [
    "¿Qué es Trinity-3?",
    "Explica el Trigate",
    "Cómo funciona el Transcender"
]

mappings = encoder.encode_batch(texts)

# LLM descubre patrones:
# - Las 3 son preguntas técnicas
# - Todas sobre componentes de Trinity-3
# - Secuencia: overview → detalle → proceso
```

**Alimenta Evolver:**
- RELATOR: Trinity-3 contiene {Trigate, Transcender, ...}
- EMERGENCIA: Preguntas técnicas → alta estructura
- DINÁMICA: Overview → Detail → Process (patrón conversacional)

---

## Roadmap

### Semana 1-2: LLM Integration ⏳
- [ ] Implementar `_encode_llm()` con OpenAI API
- [ ] Refinar prompts FFE
- [ ] Parsear respuesta JSON
- [ ] Validar con 100 ejemplos
- [ ] **Target:** Tensores coherentes, reasoning explícito

### Semana 3-4: Quality Validation ⏳
- [ ] Medir cosine_sim (tensor → embedding → tensor')
- [ ] **Target:** > 0.85 (vs 0.115 de v0.1)
- [ ] Comparar con ground truth humano
- [ ] Ajustar prompts según feedback

### Semana 5-6: Recursive Expansion ⏳
- [ ] Implementar depth=2,3 con expansión autosimilar
- [ ] Validar árbol de conceptos relacionados
- [ ] Alimentar Evolver.RELATOR con relaciones descubiertas
- [ ] **Target:** 10+ relaciones por concepto

### Semana 7-8: Cross-Batch Learning ⏳
- [ ] Implementar `_discover_cross_relations()`
- [ ] Detectar patrones emergentes (EMERGENCIA)
- [ ] Aprender dinámicas conversacionales (DINÁMICA)
- [ ] Integrar con Aurora Pipeline completo

### Semana 9-10: Production ⏳
- [ ] Optimizar costos API (caching, batch processing)
- [ ] Implementar fallback (si LLM falla → modo demo)
- [ ] Documentación completa
- [ ] **Milestone:** Aurora aprende de conversaciones reales

---

## Ventajas Estratégicas

### 1. **Semántica Preservada**
- LLM entiende significado, no solo vectores
- Genera tensores con intención, no ruido estadístico

### 2. **Autosimilitud Nativa**
- Genera contenido relacionado recursivamente
- Árbol fractal de conocimiento, no lista plana

### 3. **Relaciones Explícitas**
- Descubre conexiones conceptuales
- Alimenta Evolver.RELATOR directamente

### 4. **Interpretabilidad**
- Razonamiento explícito en cada transformación
- Debug: ver por qué el LLM generó cierto tensor

### 5. **Evolución Continua**
- Cada conversación alimenta Evolver
- Aurora aprende patrones, no solo almacena datos

### 6. **Fractal desde el Origen**
- El LLM piensa en triadas (Forma-Función-Estructura)
- No fuerza estructura fractal post-hoc

---

## Comparación con Estado del Arte

### Embeddings Tradicionales (OpenAI, Sentence-BERT)
- ✅ Rápidos, eficientes
- ❌ Vectores densos (768D), no interpretables
- ❌ No capturan relaciones explícitas
- ❌ No generan contenido autosimilar

### LLM Semantic Encoder (nuestra propuesta)
- ✅ Interpretable (Forma-Función-Estructura)
- ✅ Compacto (117 bits vs 768×32 = 24576 bits)
- ✅ Relaciones explícitas
- ✅ Autosimilar (árbol fractal)
- ✅ Evolutivo (alimenta Evolver)
- ⚠️ Más lento (requiere llamada LLM)
- ⚠️ Costo API (mitigable con caching)

---

## Conclusión

El **LLM Semantic Encoder** es el componente crítico que transforma Genesis de un sistema de procesamiento mecánico a una **inteligencia fractal autosimilar**.

**Flujo completo:**
```
Usuario → LLM Encoder → Tensores FFE + Relaciones
          ↓
Transcender sintetiza → Ms emergente
          ↓
Harmonizer repara → Coherencia absoluta
          ↓
Evolver aprende → RELATOR, EMERGENCIA, DINÁMICA
          ↓
Aurora responde → Codificada también en FFE
          ↓
Ciclo se repite → Aurora evoluciona continuamente
```

**Resultado:** Aurora no solo responde, sino que **aprende su propio lenguaje interno fractal**, descubriendo relaciones y patrones emergentes con cada interacción.

---

## Próximos Pasos

1. **Implementar `_encode_llm()`** con OpenAI API
2. **Validar calidad** (cosine_sim > 0.85)
3. **Integrar con Aurora Pipeline**
4. **Medir evolución** del Evolver a lo largo de conversaciones

**Prioridad:** 🔴 CRÍTICA  
**Dependencias:** API LLM (OpenAI, Anthropic, o local con llama.cpp)  
**Bloqueadores:** Ninguno (demo mode ya funciona)

**Estimación total:** 8-10 semanas para producción completa.

---

**Documentado:** 2025-01-20  
**Autor:** Sistema Genesis  
**Status:** 🟢 Demo implementado | 🟡 LLM integration pendiente
