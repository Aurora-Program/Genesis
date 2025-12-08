# 🆓 Opciones de LLMs Gratuitos para Genesis

## Opciones Principales (2024-2025)

### 1. **Hugging Face Inference API** (GRATIS con límites)
- **Modelos**: Llama 3, Mixtral, Mistral, Falcon, etc.
- **Límites**: ~1000 requests/día gratuitos
- **Ventajas**: 
  - API compatible con OpenAI
  - Múltiples modelos open source
  - Sin tarjeta de crédito requerida
- **URL**: https://huggingface.co/inference-api

### 2. **Groq API** (GRATIS - beta pública)
- **Modelos**: Llama 3 70B, Mixtral 8x7B, Gemma
- **Límites**: Generosos en beta
- **Ventajas**:
  - **MUY RÁPIDO** (~300 tokens/seg)
  - Compatible con OpenAI SDK
  - Calidad comparable a GPT-3.5
- **URL**: https://groq.com

### 3. **Together.ai** (Créditos iniciales gratuitos)
- **Modelos**: 50+ modelos open source
- **Límites**: $25 créditos gratis al registrarse
- **Ventajas**:
  - Amplia selección
  - API simple
  - Llama 3, Qwen, DeepSeek
- **URL**: https://together.ai

### 4. **Ollama** (100% Local - GRATIS total)
- **Modelos**: Llama 3, Mistral, Phi, Gemma
- **Límites**: Solo tu hardware
- **Ventajas**:
  - **Sin costos**
  - Sin límites de rate
  - Total privacidad
  - Sin internet requerido
- **Desventajas**:
  - Requiere GPU/RAM decente
  - Setup más complejo
- **URL**: https://ollama.ai

### 5. **Google AI Studio** (Gemini - GRATIS)
- **Modelos**: Gemini 1.5 Flash, Gemini 1.5 Pro
- **Límites**: 15 requests/minuto (gratuito)
- **Ventajas**:
  - Calidad alta (comparable GPT-4)
  - Contexto largo (1M tokens)
  - JSON mode
- **URL**: https://ai.google.dev

---

## 🎯 Recomendación para Genesis

### **OPCIÓN 1: Groq API** (Recomendado)
```python
# pip install groq

from groq import Groq

client = Groq(api_key="gsk_...")  # GRATIS

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[...],
    temperature=0.3,
    response_format={"type": "json_object"}
)
```

**Por qué Groq:**
- ✅ **100% compatible** con nuestro código OpenAI
- ✅ **Gratis** en beta pública
- ✅ **Rapidísimo** (respuestas en <1 segundo)
- ✅ **Llama 3 70B** es excelente para tareas semánticas
- ✅ Solo cambiar 2 líneas de código

### **OPCIÓN 2: Ollama Local** (Zero costos)
```python
# pip install ollama

import ollama

response = ollama.chat(
    model='llama3',
    messages=[...],
    format='json'
)
```

**Por qué Ollama:**
- ✅ **Gratis total** (corre en tu PC)
- ✅ **Sin límites** de requests
- ✅ **Privacidad** total
- ❌ Requiere GPU decente (8GB+ VRAM recomendado)

---

## 🔄 Modificación del Código

### Cambio Mínimo para Groq

```python
# pipeline/llm_semantic_encoder.py

# ANTES:
from openai import OpenAI

# DESPUÉS:
try:
    from groq import Groq as OpenAI  # API compatible!
    DEFAULT_MODEL = "llama-3.1-70b-versatile"
except ImportError:
    from openai import OpenAI
    DEFAULT_MODEL = "gpt-3.5-turbo"

# El resto del código IGUAL (100% compatible)
```

### Cambio para Ollama

```python
# pipeline/llm_semantic_encoder.py

try:
    import ollama
    USE_OLLAMA = True
except ImportError:
    USE_OLLAMA = False

def _encode_llm(self, text: str, depth: int):
    if USE_OLLAMA:
        response = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            format='json'
        )
        result = json.loads(response['message']['content'])
    else:
        # Código OpenAI actual...
```

---

## 📊 Comparación

| Servicio | Costo | Velocidad | Calidad | Setup |
|----------|-------|-----------|---------|-------|
| **Groq** | 🆓 Gratis | ⚡ Muy rápido | ⭐⭐⭐⭐ | Fácil |
| **Ollama** | 🆓 Gratis | 🐢 Depende GPU | ⭐⭐⭐⭐ | Medio |
| **HuggingFace** | 🆓 Gratis* | 🐢 Lento | ⭐⭐⭐ | Fácil |
| **Google Gemini** | 🆓 Gratis* | ⚡ Rápido | ⭐⭐⭐⭐⭐ | Fácil |
| **Together.ai** | 💰 $25 gratis | ⚡ Rápido | ⭐⭐⭐⭐ | Fácil |
| **OpenAI** | 💰 Pago | ⚡ Rápido | ⭐⭐⭐⭐⭐ | Fácil |

*Con límites

---

## 🚀 Plan de Migración

### Fase 1: Probar Groq (5 minutos)
1. Registrarse: https://console.groq.com
2. Obtener API key gratuita
3. `pip install groq`
4. Cambiar 2 líneas en `.env`:
   ```
   # OPENAI_API_KEY=sk-proj-...
   GROQ_API_KEY=gsk_...
   ```
5. Ejecutar tests

### Fase 2: Si Groq funciona
- Usar Groq como default
- Mantener OpenAI como fallback opcional
- Documentar costos = $0

### Fase 3: Considerar Ollama (opcional)
- Si quieres 100% local
- Instalar Ollama
- Descargar Llama 3 (4GB)
- Configurar encoder para usar local

---

## ✅ Recomendación Final

**Para Genesis:** Usar **Groq API**
- Gratis
- Rápido
- Compatible con código actual
- Solo cambiar API key

**Código casi idéntico**, solo cambia la importación y API key.

¿Probamos con Groq ahora? 🚀
