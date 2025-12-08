# 🎯 Proyecto Genesis - Roadmap Refocused

## Análisis Crítico del Problema

> **"El motor es inútil si la información no puede entrar y salir correctamente"**

### El Cuello de Botella: FFE Encoder

```
Embeddings (LLM)          Tensores FFE (Aurora)
[1024 dims float]    →    [117 bits discrete]
Continuo                  Discreto
Alta dimensión            Jerárquico (3-9-27)
Sin estructura            Forma-Función-Estructura
```

**Riesgo GIGO**: Si el traductor falla → Transcender sintetiza ruido → Evolver aprende basura.

---

## 🔴 FASE 1: FFE ENCODER (80% del esfuerzo)

### Objetivo
Demostrar que `embedding → FFE → embedding'` preserva significado.

### Diseño del Encoder

#### 1.1 Estrategia de Cuantización
```python
# Embedding (ej: 768 dims) → 27 vectores de 3 bits
# Necesitamos reducir: 768 dims continuas → 81 bits discretos (27×3)

class FFEEncoder:
    """
    Transforma embeddings continuos en Tensores FFE discretos.
    
    Estrategia:
      1. PCA/Autoencoder: 768 → 81 dims principales
      2. Clustering: Agrupar en 27 clusters (uno por vector del tensor)
      3. Cuantización ternaria: Cada cluster → [F, Fu, E] ∈ {0,1,NULL}
      4. Mapeo semántico: Asignar significado a cada dimensión FFE
    """
```

#### 1.2 Validaciones Críticas
```python
class FFEValidator:
    """
    Valida que el encoding preserva significado.
    
    Tests:
      1. Reconstrucción: embedding → FFE → embedding' 
         → cosine_sim(embedding, embedding') > 0.85
      
      2. Semántica: Palabras similares → FFE similares
         → "gato" ≈ "felino" en espacio FFE
      
      3. Composición: FFE(A) + FFE(B) → FFE(C) coherente
         → "rey" - "hombre" + "mujer" ≈ "reina"
      
      4. Transcender consistency: Mismos inputs → mismo Ms
    """
```

#### 1.3 Catálogo Semántico
```yaml
# ffe_semantic_map.yaml
# Define qué significa cada dimensión FFE

nivel_27:  # 27 vectores de nivel base
  vector_0:  # Primer vector [F, Fu, E]
    F:  # Forma (bit 0)
      domain: "sintaxis"
      meaning: "estructura gramatical"
      values:
        0: "simple"
        1: "compleja"
        null: "indefinida"
    
    Fu: # Función (bit 1)
      domain: "semántica"
      meaning: "rol funcional"
      values:
        0: "entidad"
        1: "acción"
        null: "relación"
    
    E:  # Estructura (bit 2)
      domain: "pragmática"
      meaning: "contexto uso"
      values:
        0: "concreto"
        1: "abstracto"
        null: "metafórico"
```

### 1.4 Pipeline de Desarrollo

```
Semana 1-2: Prototipo Básico
├── PCA/Clustering simple
├── Cuantización ternaria naive
└── Test reconstrucción básica

Semana 3-4: Refinamiento
├── Ajuste de clustering (K-means → HDBSCAN)
├── Cuantización adaptativa por contexto
└── Tests semánticos (similitud, composición)

Semana 5-6: Integración con Transcender
├── Validar que Transcender produce Ms coherentes
├── Analizar score y reconstruction_ok
└── Ajustar encoding según feedback del Transcender

Semana 7-8: Validación Exhaustiva
├── Dataset benchmark (ej: 1000 frases diversas)
├── Métricas de calidad (precision, recall, F1)
└── Documentación completa del mapeo semántico
```

---

## 🟡 FASE 2: OBSERVACIÓN (Read-Only)

### Objetivo
Escuchar conversaciones LLM sin influir. Validar que Evolver aprende patrones coherentes.

### Implementación

```python
class ObservationPipeline:
    """
    Pipeline read-only: Solo observa y aprende.
    NO modifica las respuestas del LLM.
    """
    
    def observe_conversation(self, user_input: str, llm_response: str):
        # 1. Encode
        ffe_input = self.encoder.encode(user_input)
        ffe_output = self.encoder.encode(llm_response)
        
        # 2. Transcender (sintetizar relación input→output)
        result = self.transcender.solve(
            ffe_input.nivel_3[0],
            ffe_input.nivel_3[1], 
            ffe_output.nivel_3[0]
        )
        
        # 3. Evolver (aprender patrones)
        self.evolver.observe_transcender(result)
        
        # 4. Análisis (sin modificar respuesta)
        self.analyze_patterns()
    
    def analyze_patterns(self):
        """
        Reporta lo que el Evolver está aprendiendo.
        ¿Los arquetipos tienen sentido?
        """
        top_archetypes = self.evolver.emergence_top(k=10)
        top_dynamics = self.evolver.dynamics_top(k=10)
        
        # Decodificar a lenguaje natural
        for arch in top_archetypes:
            meaning = self.decoder.decode_pattern(arch['proto'])
            print(f"Arquetipo: {meaning} (peso: {arch['w']})")
```

### Validación de Aprendizaje

```python
class LearningValidator:
    """
    Valida que el Evolver aprende coherentemente.
    """
    
    def test_archetype_coherence(self):
        """
        Test: ¿Los arquetipos capturan patrones reales?
        
        Ejemplo: Si el LLM responde muchas veces con estructura
        "pregunta → definición → ejemplo", el Evolver debería
        detectar un arquetipo de "patrón explicativo".
        """
        
    def test_dynamic_prediction(self):
        """
        Test: ¿Las dinámicas predicen transiciones?
        
        Ejemplo: Dado un FFE(input), ¿el Evolver puede predecir
        el FFE(output) esperado basándose en dinámicas aprendidas?
        """
```

---

## 🟢 FASE 3: BUCLE DE INFLUENCIA (Read-Write)

### Objetivo
Cerrar el bucle: Patrones aprendidos → Influyen en respuestas.

### Diseño del Bucle

```python
class InfluencePipeline:
    """
    Pipeline completo: Aprende Y modifica respuestas.
    """
    
    def generate_with_influence(self, user_input: str) -> str:
        # 1. Encode input
        ffe_input = self.encoder.encode(user_input)
        
        # 2. Consultar Evolver: ¿Qué patrones son relevantes?
        relevant_archetypes = self.evolver.query_relevant(ffe_input)
        relevant_dynamics = self.evolver.query_dynamics(ffe_input)
        
        # 3. Extender: Generar "contexto fractal"
        context_ffe = self.extender.extend_from_patterns(
            relevant_archetypes, 
            relevant_dynamics
        )
        
        # 4. Decode contexto → texto natural
        context_text = self.decoder.decode_tensor(context_ffe)
        
        # 5. Modificar prompt del LLM
        enhanced_prompt = f"""
        [CONTEXTO FRACTAL APRENDIDO]:
        {context_text}
        
        [PREGUNTA USUARIO]:
        {user_input}
        """
        
        # 6. LLM genera respuesta con contexto
        llm_response = self.llm.generate(enhanced_prompt)
        
        # 7. Observar para seguir aprendiendo
        self.observe_conversation(user_input, llm_response)
        
        return llm_response
```

### Modos de Influencia

```python
class InfluenceMode(Enum):
    """Diferentes estrategias de influencia"""
    
    CONTEXT_INJECTION = "inject"      # Añadir contexto al prompt
    RESPONSE_FILTERING = "filter"     # Filtrar entre N respuestas
    GUIDED_GENERATION = "guide"       # Guiar tokens probabilísticamente
    RECONSTRUCTION = "reconstruct"    # Reconstruir desde FFE directamente
```

---

## 📊 Métricas de Éxito por Fase

### Fase 1: FFE Encoder
- ✅ Reconstrucción: cosine_sim > 0.85
- ✅ Semántica: top-10 vecinos preservados 80%+
- ✅ Composición: analogías correctas 70%+
- ✅ Transcender: score promedio < 5 NULLs

### Fase 2: Observación
- ✅ Arquetipos coherentes: 5+ patrones interpretables
- ✅ Dinámicas predictivas: accuracy > 60% en predicción
- ✅ Estabilidad: patrones consistentes tras 100+ conversaciones

### Fase 3: Influencia
- ✅ Mejora medible: respuestas con influencia > sin influencia (eval humana)
- ✅ Coherencia: respuestas influidas mantienen calidad LLM
- ✅ Emergencia: patrones nuevos aparecen (no pre-programados)

---

## 🚧 Implementación Actual

### ✅ Completado
- Core Trinity-3 (Trigate, Transcender, Evolver, Extender, Harmonizer)
- Pipeline básico operacional
- 4 demos funcionando

### 🔴 SIGUIENTE (Prioridad Absoluta)
**Semana 1-2**: Implementar FFE Encoder v0.1
- Prototipo con PCA + K-means
- Test de reconstrucción básica
- Integración con pipeline existente

---

## 💡 Principios Rectores

1. **Validar antes de integrar**: No avanzar a Fase 2 sin validar Fase 1
2. **Métricas objetivas**: Cada fase tiene KPIs claros
3. **Incremental**: Empezar simple, refinar con feedback
4. **GIGO awareness**: La calidad del encoder determina todo lo demás

---

**Última actualización**: 2025-10-20  
**Fase actual**: Transición de Fase 0 → Fase 1  
**Enfoque**: 80% FFE Encoder, 20% todo lo demás
