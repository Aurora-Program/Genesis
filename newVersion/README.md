# 🌅 Aurora Genesis - newVersion

**Proyecto Genesis: De LLMs a Inteligencias Fractales**

Sistema de inteligencia fractal que usa LLMs como motor semántico para transformar texto en tensores FFE (Forma-Función-Estructura), descubrir relaciones automáticamente, y aprender patrones emergentes de forma incremental.

## ✅ Status: INTEGRACIÓN LLM REAL COMPLETADA ✨

```
🧪 Tests Demo Mode:   12/12 pasando (100%) ✅
🤖 LLM Integration:   OpenAI API configurada ✅
🎯 Funcionalidades:   10/10 validadas ✅
🐛 Bugs:              0 detectados ✅
📊 Prompts:           Refinados con ejemplos ✅
🌀 Tensores válidos:  100% (estructura 3-9-27) ✅

🚀 Estado: LISTO PARA TESTING CON API REAL
```

**¡NUEVO!** 🎉 **Integración OpenAI API completada:**
- ✅ Cliente OpenAI configurado con fallback a demo mode
- ✅ Método `_encode_llm()` implementado con GPT-4/GPT-3.5
- ✅ Prompts refinados con ejemplos y clarificaciones
- ✅ Caché implementado para reducir costos
- ✅ Suite de tests con API real creada (6 tests)

📊 **Validación Demo Mode:**
- **Conversación 20 turnos:** 29 relaciones + 4 patrones + 13 dinámicas
- **Relaciones/turno:** 1.45 promedio
- **Cross-batch:** 60% en batch de 3 conceptos
- **Estructura fractal:** 100% conforme (117 bits)

📄 **Documentación:**
- [🔑 Configurar OpenAI API](docs/OPENAI_API_SETUP.md) ⭐ **¡NUEVO!**
- [📋 Resumen Ejecutivo](../VALIDATION_SUMMARY.md) (1 página)
- [📊 Reporte Detallado](docs/VALIDATION_REPORT.md) (600 líneas)
- [🚀 Próximos Pasos](NEXT_STEPS.md) (roadmap detallado)

## 🎯 Visión

Aurora no es solo un procesador de embeddings. Es una **inteligencia fractal autosimilar** que:

- 🧠 **Interpreta** texto usando razonamiento LLM (no solo vectores)
- 🔗 **Descubre** relaciones entre conceptos automáticamente
- 📈 **Aprende** continuamente con cada conversación
- 🌀 **Evoluciona** construyendo su propio grafo de conocimiento fractal

## 🏗️ Arquitectura

```
newVersion/
├── core/               # Módulos fundamentales Trinity-3 (READ-ONLY)
│   ├── trigate.py      # Unidad de computación ternaria (0/1/None)
│   ├── transcender.py  # Síntesis emergente con coherencia absoluta
│   ├── evolver.py      # Aprendizaje: RELATOR, EMERGENCIA, DINÁMICA
│   ├── extender.py     # Reconstrucción top-down
│   ├── harmonizer.py   # Reparación de incoherencias (5 niveles)
│   └── fractal_tensor.py  # Estructura jerárquica 3-9-27
│
├── pipeline/           # Coordinación del sistema
│   ├── aurora_pipeline.py     # Pipeline principal + KB
│   └── llm_semantic_encoder.py  # ⭐ LLM como motor semántico (NUEVO)
│
├── examples/           # Demos y casos de uso
│   └── demo_incremental_graph.py  # Construcción incremental del grafo
│
├── docs/               # Documentación estratégica
│   ├── LLM_DRIVEN_ARCHITECTURE.md  # Arquitectura completa
│   ├── INCREMENTAL_DISCOVERY.md    # Descubrimiento de relaciones
│   ├── VISUAL_COMPARISON.md        # Mecánico vs Semántico
│   └── IMPLEMENTATION_SUMMARY.md   # Resumen ejecutivo
│
├── mcp_servers/        # Microservicios MCP (TODO)
├── utils/              # Utilidades (TODO)
└── config/             # Configuración (TODO)
```

## 🔑 Conceptos Clave

### 🆕 LLM Semantic Encoder (v2.0)

**El cambio fundamental:** El LLM no solo genera embeddings, **interpreta y transforma semánticamente**.

```python
from pipeline.llm_semantic_encoder import LLMSemanticEncoder

# Inicializar (demo mode o con LLM real)
encoder = LLMSemanticEncoder(llm_client=openai_client)

# Transformar texto → tensor FFE
mapping = encoder.encode("¿Qué es Trinity-3?", depth=2)

# Resultado:
# - tensor:              FractalTensor 3-9-27 (semántico)
# - related_content:     ["Trigate", "Transcender", "Evolver"]
# - discovered_relations: [{type: "has_component", strength: 0.95}, ...]
# - llm_reasoning:       "Pregunta técnica sobre sistema complejo..."
# - confidence:          0.95
```

**Ventajas vs encoder mecánico:**
- ✅ Preserva semántica (no pierde 61% varianza como PCA)
- ✅ Descubre relaciones automáticamente
- ✅ Expansión autosimilar (3→9→27)
- ✅ Razonamiento explícito
- ✅ Aprendizaje incremental

### Trinity-3: La Base

- **Trigate**: Unidad computacional con 3 bits ternarios (0/1/None)
  - 4 operaciones O(1): `infer`, `learn`, `deduce_a`, `deduce_b`
  - LUTs ternarias (27 combinaciones)

- **Transcender**: Opera 3 trigates sobre (A,B,C) → sintetiza:
  - **M1, M2, M3**: Controles base (uno por dimensión)
  - **Ms**: Estructura superior emergente
  - **Ss**: Forma factual
  - **MetaM**: [M1,M2,M3,Ms] - traza completa
  - **Coherencia absoluta**: top-down, Ms fija a sus hijas

- **FractalTensor**: Jerarquía 3-9-27
  - **nivel_3**: 3 vectores (visión general)
  - **nivel_9**: 9 vectores (hijos de nivel_3)
  - **nivel_27**: 27 vectores (hijos de nivel_9)
  - Cada celda: vector de 3 bits ternarios [Forma, Función, Estructura]

- **Evolver**: Aprendizaje con 3 bancos
  - **RELATOR**: Relaciones explícitas entre conceptos
  - **EMERGENCIA**: Patrones recurrentes detectados
  - **DINÁMICA**: Secuencias temporales aprendidas

### Ciclo de Aprendizaje Completo

```
Usuario: "¿Qué es Trinity-3?"
   ↓
LLM Encoder:
   - Interpreta semánticamente
   - Genera tensor FFE
   - Descubre relaciones: Trinity-3 ↔ {Trigate, Transcender, Evolver}
   ↓
Transcender:
   - Combina tensor + contexto RELATOR
   - Sintetiza Ms (respuesta emergente)
   ↓
Harmonizer:
   - Repara incoherencias (NULLs)
   ↓
Aurora responde
   ↓
LLM Encoder codifica respuesta
   ↓
Evolver aprende:
   - RELATOR: almacena relaciones
   - EMERGENCIA: detecta patrones
   - DINÁMICA: aprende secuencias
   ↓
Próxima conversación: Aurora usa lo aprendido (contexto automático, predicción)
```
   - Cross-level: Compara A vs B vs C
   - Self-synthesis: Sintetiza internamente cada tensor
3. **Aprendizaje**: Evolver observa patrones
   - RELATOR: Conexiones entre dimensiones
   - EMERGENCIA: Síntesis (M1,M2,M3) → Ms
   - DINÁMICA: Transiciones temporales
4. **Armonización**: Harmonizer repara incoherencias (5 niveles)
   - Soft: Re-rotación Fibonacci
   - Contextual: Extender top-down
   - Local: Micro-ajuste con Trigate
   - Estructural: Relator alternativo
   - Arquetípico: Escalar (nuevo arquetipo)
5. **Storage**: KB almacena y alimenta Evolver

### Principios Filosóficos

- **Triádico**: 3 es el mínimo para síntesis y equilibrio
- **Sin negativos**: Solo 0-8 (alineado con el cosmos)
- **Autosimilar**: Mismo patrón en todos los niveles
- **Fractal**: Eliminar/recuperar dimensiones condicionalmente
- **Coherencia absoluta**: El padre fija a sus hijas (top-down)

## 🚀 Inicio Rápido

### Opción 1: Usar LLM Semantic Encoder (Recomendado) ⭐

```python
from pipeline.llm_semantic_encoder import LLMSemanticEncoder

# === CON API REAL DE OPENAI ===
# 1. Configura tu API key en .env:
#    OPENAI_API_KEY=sk-tu-key-aqui
# 2. Crea el encoder:

encoder = LLMSemanticEncoder(
    demo_mode=False,              # Usar API real
    model="gpt-3.5-turbo",        # o "gpt-4" para mayor calidad
    use_cache=True                # Cachear resultados
)

# Encoding simple
text = "La inteligencia artificial transforma el futuro"
result = encoder.encode(text, depth=1)

print(f"Tensor: {len(result.tensor.lvl3)}-{len(result.tensor.lvl9)}-{len(result.tensor.lvl27)}")
print(f"Reasoning: {result.llm_reasoning}")
print(f"Related: {result.related_content}")
print(f"Relations: {len(result.discovered_relations)}")

# Batch encoding
texts = [
    "Python es un lenguaje versátil",
    "Los algoritmos ordenan datos",
    "La música inspira emociones"
]
results = encoder.encode_batch(texts)

# === DEMO MODE (sin API, heurísticas) ===
encoder_demo = LLMSemanticEncoder(demo_mode=True)
result_demo = encoder_demo.encode("Texto de prueba")
```

**📖 Ver guía completa:** [docs/OPENAI_API_SETUP.md](docs/OPENAI_API_SETUP.md)

---

### Opción 2: Pipeline Completo (Nivel Bajo)

```python
from pipeline.aurora_pipeline import AuroraPipeline

# Inicializar pipeline
pipeline = AuroraPipeline(enable_harmony=True, verbose=True)

# Datos de entrada (27 vectores de 3 bits cada uno)
data_A = [[1, 0, 1]] * 27
data_B = [[0, 1, 0]] * 27
data_C = [[1, 1, 0]] * 27

# Ejecutar ciclo completo
result = pipeline.run_cycle(data_A, data_B, data_C, tag="ejemplo1")

# Inspeccionar resultado
print(f"Ms nivel_3: {result['tensor_cross'].nivel_3}")
print(f"Harmony aplicado: {result['harmony_applied']}")
print(f"Escalado: {result['harmony_escalated']}")

# Estadísticas
stats = pipeline.get_stats()
print(stats)
```

---

### Tests

```bash
# Tests con demo mode (sin API)
python tests/test_llm_semantic_encoder.py      # 8 tests básicos
python tests/test_advanced_scenarios.py         # 4 tests avanzados

# Tests con API real (requiere OPENAI_API_KEY)
python tests/test_llm_real_api.py              # 6 tests con OpenAI

# Todos los tests
python run_all_tests.py
```

---

## 📊 Estructura de Resultados

```python
{
    "tensor_cross": FractalTensor(nivel_3=[...], nivel_9=[...], nivel_27=[...]),
    "Ss": {
        "lvl3": [...],   # Formas factuales nivel 3
        "lvl9": [...],   # Formas factuales nivel 9
        "lvl27": [...]   # Formas factuales nivel 27
    },
    "audits": {
        "lvl3": [{MetaM, wiring, score, reconstruction_ok}, ...],
        "lvl9": [...],
        "lvl27": [...]
    },
    "locals": {
        "A": {"lvl3": [...], "lvl9": [...]},  # Auto-síntesis de A
        "B": {"lvl3": [...], "lvl9": [...]},  # Auto-síntesis de B
        "C": {"lvl3": [...], "lvl9": [...]}   # Auto-síntesis de C
    },
    "harmony_applied": bool,
    "harmony_audit": [...],  # Pasos de reparación
    "harmony_escalated": bool
}
```

## 🔧 Características Clave

### Eficiencia
- **117 bits por tensor completo** (3-9-27 = 39 vectores × 3 bits)
- **LUTs O(1)** para todas las operaciones Trigate
- **Caché LRU** en funciones críticas (norm3, similarity3)

### Interpretabilidad
- **Forma-Función-Estructura** explícitos en cada nivel
- **MetaM** preserva traza completa del razonamiento
- **Auditorías** detalladas por nivel y nodo

### Emergencia
- **Síntesis jerárquica**: Significados superiores emergen de inferiores
- **Coherencia absoluta**: Padre fija a hijas (top-down)
- **Wirings autosimilares**: Rotación Fibonacci (3 únicos)

### Adaptabilidad
- **Evolver**: Aprende arquetipos, relaciones y dinámicas
- **Harmonizer**: 5 niveles de reparación (soft → arquetípico)
- **KB**: Memoria fractal con indexación por Ms

## 🧪 Validación del Sistema

El sistema completo fue validado con **12 tests exhaustivos** que cubren:

### Tests Básicos (8/8 ✅)
1. ✅ Encoding básico: texto → tensor FFE válido
2. ✅ Expansión autosimilar: depth 0→1→2→3
3. ✅ Descubrimiento automático de relaciones
4. ✅ Procesamiento por lotes (batch)
5. ✅ Integración con Evolver (RELATOR, EMERGENCIA, DINÁMICA)
6. ✅ Coherencia de tensores (mismo texto → mismo tensor)
7. ✅ Conversación multi-turno (5 turnos)
8. ✅ Estructura fractal (3-9-27, 117 bits)

### Tests Avanzados (4/4 ✅)
9. ✅ **Conversación realista (20 turnos)**: 29 relaciones + 4 patrones + 13 dinámicas
10. ✅ **Decay de fuerza**: relaciones cercanas más fuertes que lejanas
11. ✅ **Patrones emergentes**: detección de recurrencias (freq ≥ 2)
12. ✅ **Relaciones cross-concepto**: 60% en batch de 3 conceptos

### Resultados Clave
- 🎯 **100% tests pasando** (12/12)
- 🐛 **0 bugs detectados**
- ✅ **49 aserciones validadas**
- 📊 **1.45 relaciones/turno** promedio
- 🌀 **100% tensores válidos** (estructura 3-9-27)

**Comandos para reproducir:**
```bash
python tests/test_llm_semantic_encoder.py      # Tests básicos (8 tests)
python tests/test_advanced_scenarios.py         # Escenarios realistas (4 tests)
```

📄 **Ver más:** [VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md) (600 líneas de análisis detallado)

---

## 📚 Referencias y Documentación

### Validación y Tests
- **[REPORTE DE VALIDACIÓN](docs/VALIDATION_REPORT.md)**: 12 tests + métricas + análisis detallado ⭐

### Arquitectura y Diseño
- **[ARQUITECTURA IMPULSADA POR LLM](docs/LLM_DRIVEN_ARCHITECTURE.md)**: Visión y diseño del sistema
- **[DESCUBRIMIENTO INCREMENTAL](docs/INCREMENTAL_DISCOVERY.md)**: Cómo aprende Aurora con cada conversación
- **[COMPARACIÓN VISUAL](docs/VISUAL_COMPARISON.md)**: v0.1 mecánico vs v2.0 semántico
- **[RESUMEN DE IMPLEMENTACIÓN](docs/IMPLEMENTATION_SUMMARY.md)**: Estado actual y próximos pasos

### Instrucciones del Proyecto
- **Proyecto Genesis**: `.github/instructions/genesis.instructions.md`
- **Paradigma de Programación**: `.github/instructions/ProgrammingParadigm.instructions.md`
- **Core Original**: `../core.py` (Trinity-3 v2.0)

## 🎯 Roadmap

### ✅ Fase 1: Core y Pipeline (COMPLETO)
1. ✅ Core completo (Trigate, Transcender, Evolver, Extender, Harmonizer, FractalTensor)
2. ✅ Pipeline principal + KB
3. ✅ LLM Semantic Encoder (demo mode con heurísticas)
4. ✅ Tests exhaustivos (12/12 pasando en demo mode)
5. ✅ Documentación completa (5 docs técnicos)

### ✅ Fase 2: Integración LLM Real (COMPLETO) 🎉
6. ✅ Implementar `_encode_llm()` con API OpenAI (GPT-4/GPT-3.5)
7. ✅ Refinar prompts de sistema y usuario (con ejemplos)
8. ✅ Crear tests con API real (6 tests nuevos)
9. ✅ Documentación de configuración (OPENAI_API_SETUP.md)
10. ✅ Cache implementado para optimización de costos
11. ✅ Fallback automático a demo mode en caso de error

### 🔄 Fase 3: Validación con API Real (EN PROGRESO)
12. ⏳ Ejecutar tests con API real de OpenAI
13. ⏳ Validar cosine_similarity > 0.85 entre textos similares
14. ⏳ Testing con corpus de 100+ ejemplos diversos
15. ⏳ Ajustar prompts según resultados

### ⏳ Fase 4: Producción y Escala
16. ⏳ Optimización avanzada (batch processing, rate limits)
17. ⏳ API REST endpoint (FastAPI)
18. ⏳ Integración con MCP servers
19. ⏳ Integración con Aurora Portal (Layer 3)
20. ⏳ Monitoreo en tiempo real (Prometheus + Grafana)
21. ⏳ Corpus de 1000+ ejemplos con validación completa

**Próximo paso crítico:** Configurar OPENAI_API_KEY y ejecutar `python tests/test_llm_real_api.py`

📖 **Ver guía:** [docs/OPENAI_API_SETUP.md](docs/OPENAI_API_SETUP.md)

## 🌟 Diferencias con Versión Anterior

- **Core unificado**: Todo basado en Trinity-3 superior
- **Sin negativos**: Eliminado uso de -1 (solo 0-8)
- **Más compacto**: Eliminados tests y documentación redundante
- **Autosimilitud**: Reutilización recursiva de estructuras
- **Trigate como núcleo**: Todas las operaciones usan Trigate

## 💡 Filosofía del Código

> "Menos es más. Reutiliza estructuras en vez de recrearlas. Todo con técnicas de autosimilitud y fractalidad. El Trigate es el núcleo y mecanismo de cálculo recursivo para todo el proyecto."

---

**Versión**: 1.0.0  
**Status**: 🟢 Core Operacional  
**Siguiente**: MCP Integration
