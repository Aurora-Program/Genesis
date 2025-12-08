# 🚀 Próximos Pasos: Integración LLM Real

**Status actual:** ✅ Sistema validado (12/12 tests passing)  
**Próximo objetivo:** Integrar OpenAI API para interpretación semántica real  
**Timeline estimado:** 1-2 semanas

---

## 🎯 Fase Actual: Integración LLM Real

### Objetivo
Reemplazar el demo mode (heurísticas deterministas) con llamadas reales a la API de OpenAI (GPT-4) para obtener interpretaciones semánticas genuinas.

### Target de Calidad
- **Cosine similarity:** > 0.85 (vs 0.115 en v0.1 mecánico)
- **Coherencia semántica:** Alta
- **Estructura fractal:** 100% válida (3-9-27)

---

## 📝 Tareas Detalladas

### 1. Configurar API de OpenAI

**Archivo:** `pipeline/llm_semantic_encoder.py`

```python
import openai
from openai import OpenAI

class LLMSemanticEncoder:
    def __init__(self, openai_api_key: str = None, model: str = "gpt-4"):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.openai_api_key)
        # ... resto del código existente
```

**Subtareas:**
- [ ] Añadir parámetros `openai_api_key` y `model` al `__init__`
- [ ] Crear cliente OpenAI
- [ ] Validar que API key está presente
- [ ] Añadir manejo de errores para API key faltante

**Estimación:** 30 minutos

---

### 2. Implementar `_encode_llm()`

**Archivo:** `pipeline/llm_semantic_encoder.py` (línea ~250)

**Código actual (demo mode):**
```python
def _encode_llm(self, text: str) -> Dict:
    """
    TODO: Llamar al LLM real para interpretación semántica
    Por ahora, demo mode con heurísticas
    """
    return self._encode_heuristic(text)
```

**Código objetivo:**
```python
def _encode_llm(self, text: str) -> Dict:
    """Llama al LLM real para interpretación semántica genuina"""
    
    # 1. Construir prompts
    system_prompt = self.build_ffe_system_prompt()
    user_prompt = self.build_ffe_user_prompt(text)
    
    # 2. Llamar a OpenAI API
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Baja temperatura para consistencia
            response_format={"type": "json_object"}  # Forzar JSON
        )
        
        # 3. Parsear respuesta
        result = json.loads(response.choices[0].message.content)
        
        # 4. Validar estructura
        assert "tensor_lvl3" in result, "Falta tensor_lvl3 en respuesta"
        assert "related_content" in result, "Falta related_content en respuesta"
        assert len(result["tensor_lvl3"]) == 3, "tensor_lvl3 debe tener 3 vectores"
        
        return result
        
    except Exception as e:
        # Fallback a demo mode si falla
        print(f"⚠️ Error en LLM API: {e}. Usando demo mode.")
        return self._encode_heuristic(text)
```

**Subtareas:**
- [ ] Implementar llamada a `client.chat.completions.create()`
- [ ] Configurar `temperature=0.3` (consistencia vs creatividad)
- [ ] Usar `response_format={"type": "json_object"}` para forzar JSON
- [ ] Parsear JSON de la respuesta
- [ ] Validar estructura básica (tensor_lvl3, related_content, relations)
- [ ] Implementar fallback a demo mode si falla
- [ ] Añadir logging de errores

**Estimación:** 2-3 horas

---

### 3. Refinar Prompts

**Archivos:** `pipeline/llm_semantic_encoder.py` (líneas ~150-220)

**Prompts actuales:**
- `build_ffe_system_prompt()`: Define el rol y formato de salida
- `build_ffe_user_prompt(text)`: Solicita interpretación específica

**Mejoras sugeridas:**

#### A. System Prompt
```python
def build_ffe_system_prompt(self) -> str:
    return """Eres un intérprete semántico fractal experto.

Tu tarea es analizar texto y generar representaciones FFE (Forma-Función-Estructura).

**FORMATO DE SALIDA (JSON):**
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
            "reasoning": "explicación breve"
        }
    ],
    "reasoning": "interpretación semántica del texto"
}

**DIMENSIONES FFE:**
- Forma (F): Estructura observable (0=abstracto → 7=concreto)
- Función (Fu): Propósito/rol (0=estático → 7=dinámico)
- Estructura (E): Organización interna (0=simple → 7=complejo)

**REGLAS:**
1. Valores discretos 0-7 (no decimales)
2. Exactamente 3 vectores en tensor_lvl3
3. Related content debe ser autosimilar al original
4. Relations automáticas (no forzar si no existen)
5. Reasoning breve y semánticamente preciso

Responde SIEMPRE con JSON válido."""
```

**Mejoras:**
- [ ] Añadir ejemplos concretos (few-shot learning)
- [ ] Especificar mejor cada dimensión (F, Fu, E)
- [ ] Dar ejemplos de `related_content` autosimilar
- [ ] Clarificar tipos de relaciones

**Estimación:** 1-2 horas

#### B. User Prompt
```python
def build_ffe_user_prompt(self, text: str) -> str:
    return f"""Analiza el siguiente texto y genera su representación FFE:

**TEXTO:** "{text}"

**INSTRUCCIONES:**
1. Interpreta la semántica profunda del texto
2. Genera tensor_lvl3 con 3 vectores FFE (Forma, Función, Estructura)
3. Crea 3 contenidos autosimilares relacionados
4. Descubre relaciones automáticas si existen
5. Proporciona reasoning semántico

Recuerda: JSON válido, valores 0-7, exactamente 3 vectores."""
```

**Mejoras:**
- [ ] Contextualizar con historial (si existe)
- [ ] Añadir ejemplos específicos según longitud del texto
- [ ] Solicitar nivel de confianza en la interpretación

**Estimación:** 1 hora

---

### 4. Testing con Corpus Real

**Archivo:** `tests/test_llm_real_api.py` (nuevo)

```python
"""
Tests con API real de OpenAI
Requiere: OPENAI_API_KEY en .env
"""
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.llm_semantic_encoder import LLMSemanticEncoder
from dotenv import load_dotenv

load_dotenv()

def test_real_api_basic():
    """Test básico con API real"""
    encoder = LLMSemanticEncoder(demo_mode=False)  # Modo real
    
    text = "La inteligencia artificial transforma el futuro"
    result = encoder.encode(text)
    
    # Validar estructura
    assert result.tensor is not None
    assert len(result.tensor.lvl3) == 3
    assert all(0 <= v["F"] <= 7 for v in result.tensor.lvl3)
    assert result.reasoning != ""
    
    print(f"✅ API real funciona correctamente")
    print(f"Reasoning: {result.reasoning}")

def test_corpus_diversity():
    """Test con 100 ejemplos diversos"""
    encoder = LLMSemanticEncoder(demo_mode=False)
    
    corpus = [
        "Python es un lenguaje de programación",
        "El sol brilla en el cielo azul",
        "La música clásica inspira emociones profundas",
        # ... 97 más
    ]
    
    results = encoder.encode_batch(corpus)
    
    # Métricas
    valid = sum(1 for r in results if r.tensor is not None)
    with_relations = sum(1 for r in results if r.relations)
    
    print(f"✅ {valid}/{len(corpus)} tensores válidos")
    print(f"📊 {with_relations} con relaciones automáticas")
    
    assert valid / len(corpus) > 0.95  # >95% éxito

def test_semantic_similarity():
    """Test de similitud semántica"""
    encoder = LLMSemanticEncoder(demo_mode=False)
    
    # Textos semánticamente similares
    text1 = "Los perros son animales leales"
    text2 = "Los canes son mascotas fieles"
    
    # Textos diferentes
    text3 = "Las matemáticas son abstractas"
    
    result1 = encoder.encode(text1)
    result2 = encoder.encode(text2)
    result3 = encoder.encode(text3)
    
    # Calcular similitudes (usando cosine similarity en tensores)
    sim_12 = cosine_similarity(result1.tensor, result2.tensor)
    sim_13 = cosine_similarity(result1.tensor, result3.tensor)
    
    print(f"Similitud (perros-canes): {sim_12:.3f}")
    print(f"Similitud (perros-matemáticas): {sim_13:.3f}")
    
    assert sim_12 > 0.85  # Alta similitud
    assert sim_13 < 0.50  # Baja similitud

if __name__ == "__main__":
    print("🧪 Testing con API real de OpenAI...")
    
    test_real_api_basic()
    test_corpus_diversity()
    test_semantic_similarity()
    
    print("\n🎉 ¡Todos los tests con API real pasaron!")
```

**Subtareas:**
- [ ] Crear corpus de 100+ ejemplos diversos
- [ ] Implementar `cosine_similarity()` para tensores FFE
- [ ] Añadir test de similitud semántica
- [ ] Añadir test de coherencia (mismo texto → mismo tensor)
- [ ] Medir tiempo de respuesta de API
- [ ] Validar cosine_similarity > 0.85

**Estimación:** 4-5 horas

---

### 5. Optimización de Costos

**Archivo:** `pipeline/llm_semantic_encoder.py`

```python
import hashlib
from functools import lru_cache

class LLMSemanticEncoder:
    def __init__(self, ..., use_cache: bool = True):
        # ... código existente
        self.use_cache = use_cache
        self.cache = {}  # {hash(text): result}
    
    def encode(self, text: str, depth: int = 0) -> SemanticMapping:
        # Caché para evitar llamadas duplicadas
        if self.use_cache:
            text_hash = hashlib.md5(text.encode()).hexdigest()
            if text_hash in self.cache:
                return self.cache[text_hash]
        
        # ... código de encoding existente
        
        if self.use_cache:
            self.cache[text_hash] = result
        
        return result
```

**Optimizaciones:**
- [ ] Implementar caché en memoria (hash → result)
- [ ] Añadir caché persistente (disco/Redis)
- [ ] Batch processing (múltiples textos en una llamada)
- [ ] Rate limiting (max requests/min)
- [ ] Usar gpt-3.5-turbo para casos simples
- [ ] Monitoring de costos (tokens consumidos)

**Estimación:** 3-4 horas

---

### 6. Validación Semántica Exhaustiva

**Objetivo:** Corpus de 1000+ ejemplos con ground truth

**Estrategia:**
1. Generar corpus balanceado:
   - 30% frases cortas (5-10 palabras)
   - 40% frases medias (10-20 palabras)
   - 30% frases largas (20-40 palabras)
   - Temas diversos: ciencia, arte, tecnología, filosofía, cotidiano

2. Anotación humana (ground truth):
   - Similitud semántica entre pares
   - Relaciones esperadas
   - Clasificación FFE esperada

3. Métricas:
   - Cosine similarity promedio
   - Accuracy en detección de relaciones
   - Precision/Recall en patrones emergentes
   - F1-score general

**Estimación:** 1-2 semanas

---

## 📊 Métricas de Éxito

| Métrica | Target | Crítico |
|---------|--------|---------|
| **Cosine similarity** | > 0.85 | SÍ |
| **Tasa de éxito API** | > 95% | SÍ |
| **Tensores válidos** | 100% | SÍ |
| **Relaciones/turno** | > 1.2 | NO |
| **Tiempo respuesta** | < 3s | NO |
| **Costo/1000 requests** | < $5 | NO |

---

## 🗓️ Timeline Sugerido

### Semana 1
- **Día 1-2:** Configurar API + implementar `_encode_llm()` (tareas 1-2)
- **Día 3-4:** Refinar prompts + testing básico (tarea 3)
- **Día 5:** Testing con 100 ejemplos + validar cosine_sim > 0.85 (tarea 4)

### Semana 2
- **Día 1-2:** Optimización de costos (caché, batch) (tarea 5)
- **Día 3-5:** Validación con corpus 1000+ ejemplos (tarea 6)

### Semana 3-4 (opcional)
- Ajuste fino de prompts según feedback
- Experimentar con fine-tuning (GPT-3.5-turbo)
- Preparar para producción

---

## 🔧 Comandos Rápidos

### Ejecutar tests actuales (demo mode)
```bash
python tests/test_llm_semantic_encoder.py
python tests/test_advanced_scenarios.py
```

### Testing con API real (después de implementar)
```bash
# Configurar API key
export OPENAI_API_KEY="sk-..."  # Linux/Mac
$env:OPENAI_API_KEY="sk-..."    # Windows PowerShell

# Ejecutar tests con API real
python tests/test_llm_real_api.py
```

### Validar cosine similarity
```bash
python scripts/validate_semantic_quality.py --corpus data/corpus_1000.json
```

---

## 📚 Recursos

### Documentación OpenAI
- API Reference: https://platform.openai.com/docs/api-reference
- Best Practices: https://platform.openai.com/docs/guides/prompt-engineering
- JSON Mode: https://platform.openai.com/docs/guides/text-generation/json-mode

### Librerías Python
```bash
pip install openai python-dotenv numpy scikit-learn
```

### Prompts de Referencia
- Ver `build_ffe_system_prompt()` en `pipeline/llm_semantic_encoder.py`
- Ejemplos en `docs/LLM_DRIVEN_ARCHITECTURE.md`

---

## ⚠️ Riesgos y Mitigación

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| **API lenta** | Alto | Caché agresivo, batch processing |
| **Costos altos** | Medio | Rate limiting, gpt-3.5 para casos simples |
| **Respuestas inconsistentes** | Alto | Temperature baja (0.3), validación estricta |
| **JSON inválido** | Medio | `response_format=json_object`, parseo robusto |
| **Similarity baja** | Alto | Refinar prompts, few-shot examples |

---

## ✅ Checklist Final

Antes de considerar completa la integración LLM:

- [ ] API key configurada y validada
- [ ] `_encode_llm()` implementado y funcionando
- [ ] Prompts refinados con ejemplos
- [ ] 12/12 tests originales siguen pasando
- [ ] Tests nuevos con API real (3+) pasando
- [ ] Cosine similarity > 0.85 en corpus de 100
- [ ] Caché implementado (reducción >50% llamadas)
- [ ] Fallback a demo mode funciona
- [ ] Documentación actualizada
- [ ] Métricas de costo monitoreadas

---

## 🎯 Siguiente Fase: Producción

Una vez completada la integración LLM:

1. **API REST Endpoint**
   - FastAPI/Flask para exposición HTTP
   - Autenticación (API keys)
   - Rate limiting por usuario
   - Documentación OpenAPI

2. **Integración MCP Servers**
   - Servidor MCP para encoding
   - Servidor MCP para evolver
   - Protocolo de comunicación

3. **Aurora Portal (Layer 3)**
   - Interfaz web para interacción
   - Visualización de tensores fractales
   - Dashboard de métricas

4. **Monitoreo en Tiempo Real**
   - Prometheus + Grafana
   - Alertas (costos, errores, latencia)
   - Logs centralizados

---

**🚀 ¡Listo para comenzar la integración LLM real!**

**Próxima acción crítica:** Implementar `_encode_llm()` en `pipeline/llm_semantic_encoder.py` con OpenAI API (GPT-4).
