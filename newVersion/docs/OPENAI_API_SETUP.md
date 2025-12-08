# 🔑 Guía de Configuración: OpenAI API

Esta guía te ayuda a configurar la API de OpenAI para usar el LLM Semantic Encoder con GPT-4/GPT-3.5.

---

## 📋 Requisitos Previos

1. Cuenta en OpenAI: https://platform.openai.com/
2. Créditos disponibles en tu cuenta
3. Python 3.10+ instalado
4. Dependencias instaladas (ver abajo)

---

## 🔧 Paso 1: Instalar Dependencias

```bash
# En el directorio newVersion/
pip install openai python-dotenv numpy scikit-learn
```

O si usas el virtual environment del proyecto:

```bash
C:/Users/p_m_a/Aurora/Genesis/.venv/Scripts/python.exe -m pip install openai python-dotenv numpy scikit-learn
```

---

## 🔑 Paso 2: Obtener API Key de OpenAI

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión con tu cuenta
3. Click en "Create new secret key"
4. Dale un nombre (ej: "Aurora Genesis Encoder")
5. **COPIA LA KEY** (no la volverás a ver)
6. Guarda la key en un lugar seguro

**Formato de la key:** `sk-proj-...` (empieza con `sk-`)

---

## ⚙️ Paso 3: Configurar Variable de Entorno

### Opción A: Archivo .env (Recomendado)

1. En el directorio `newVersion/`, crea un archivo llamado `.env`
2. Añade tu API key:

```bash
OPENAI_API_KEY=sk-tu-api-key-aqui
```

3. Guarda el archivo

**⚠️ IMPORTANTE:** El archivo `.env` está en `.gitignore` y **NO se subirá a Git**. Esto protege tu API key.

### Opción B: Variable de Entorno del Sistema

#### Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="sk-tu-api-key-aqui"
```

#### Linux/Mac:
```bash
export OPENAI_API_KEY="sk-tu-api-key-aqui"
```

**Nota:** Esta configuración es temporal (solo para la sesión actual).

---

## ✅ Paso 4: Verificar Configuración

Ejecuta este comando para verificar que todo está bien:

```bash
# Con Python del sistema
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...' if os.getenv('OPENAI_API_KEY') else '❌ No encontrada')"

# Con venv del proyecto
C:/Users/p_m_a/Aurora/Genesis/.venv/Scripts/python.exe -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...' if os.getenv('OPENAI_API_KEY') else '❌ No encontrada')"
```

**Salida esperada:**
```
✅ API Key: sk-proj-Ab...
```

---

## 🧪 Paso 5: Probar con API Real

### Test Simple
```python
from pipeline.llm_semantic_encoder import LLMSemanticEncoder

# Crear encoder con API real (usará gpt-3.5-turbo por defecto)
encoder = LLMSemanticEncoder(demo_mode=False, model="gpt-3.5-turbo")

# Verificar que no está en demo mode
if encoder.use_demo_mode:
    print("❌ Error: Encoder en demo mode (API key no válida)")
else:
    print("✅ Encoder configurado con API real")
    
    # Probar encoding
    text = "La inteligencia artificial transforma el futuro"
    result = encoder.encode(text)
    
    print(f"✅ Encoding exitoso!")
    print(f"   Tensor: {len(result.tensor.lvl3)}-{len(result.tensor.lvl9)}-{len(result.tensor.lvl27)}")
    print(f"   Reasoning: {result.llm_reasoning[:80]}...")
```

### Test Completo
```bash
# Ejecutar suite de tests con API real
python tests/test_llm_real_api.py
```

**Nota:** Estos tests consumen créditos de OpenAI (~$0.05 - $0.20 dependiendo del modelo).

---

## 💰 Costos Estimados

### GPT-3.5-Turbo (Recomendado para desarrollo)
- **Input:** $0.0005 / 1K tokens
- **Output:** $0.0015 / 1K tokens
- **Costo por encoding:** ~$0.002 - $0.005
- **100 encodings:** ~$0.20 - $0.50

### GPT-4 (Producción, alta calidad)
- **Input:** $0.03 / 1K tokens
- **Output:** $0.06 / 1K tokens
- **Costo por encoding:** ~$0.10 - $0.20
- **100 encodings:** ~$10 - $20

**Recomendación:** Usa `gpt-3.5-turbo` para desarrollo y tests, `gpt-4` para producción.

---

## ⚡ Optimización de Costos

### 1. Usar Caché
```python
# Cache está activado por defecto
encoder = LLMSemanticEncoder(use_cache=True)

# Esto solo llamará a la API una vez
result1 = encoder.encode("texto")  # API call
result2 = encoder.encode("texto")  # Cache hit (gratis)
```

### 2. Batch Processing
```python
# Procesar múltiples textos de una vez
texts = ["texto1", "texto2", "texto3"]
results = encoder.encode_batch(texts)  # Más eficiente
```

### 3. Usar Modelo Más Barato
```python
# gpt-3.5-turbo es ~20x más barato que gpt-4
encoder = LLMSemanticEncoder(model="gpt-3.5-turbo")
```

---

## 🔧 Configuración Avanzada

### Cambiar Modelo
```python
# GPT-4 (mejor calidad, más caro)
encoder = LLMSemanticEncoder(model="gpt-4")

# GPT-3.5-Turbo (buena calidad, económico)
encoder = LLMSemanticEncoder(model="gpt-3.5-turbo")

# GPT-4-Turbo (balance)
encoder = LLMSemanticEncoder(model="gpt-4-turbo-preview")
```

### Pasar API Key Directamente
```python
# En vez de usar .env
encoder = LLMSemanticEncoder(
    openai_api_key="sk-tu-key-aqui",
    model="gpt-3.5-turbo"
)
```

### Forzar Demo Mode
```python
# Usar heurísticas (sin API)
encoder = LLMSemanticEncoder(demo_mode=True)
```

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY no encontrada"
**Solución:**
1. Verifica que el archivo `.env` existe en `newVersion/`
2. Verifica que el archivo contiene `OPENAI_API_KEY=sk-...`
3. Verifica que no hay espacios extras: ❌ `OPENAI_API_KEY = sk-...` ✅ `OPENAI_API_KEY=sk-...`

### Error: "Incorrect API key provided"
**Solución:**
1. Verifica que copiaste la key completa (empieza con `sk-`)
2. Verifica que la key no ha expirado (revisa en OpenAI dashboard)
3. Genera una nueva key en https://platform.openai.com/api-keys

### Error: "You exceeded your current quota"
**Solución:**
1. Ve a https://platform.openai.com/account/billing
2. Añade créditos a tu cuenta
3. Verifica que tienes un método de pago configurado

### Error: "Rate limit reached"
**Solución:**
1. Espera unos minutos antes de reintentar
2. Reduce la frecuencia de llamadas
3. Considera actualizar tu tier en OpenAI

### Encoder se queda en demo_mode
**Solución:**
1. Verifica que `openai` está instalado: `pip install openai`
2. Verifica que `OPENAI_API_KEY` está configurada
3. Verifica que la key es válida
4. Revisa los mensajes de error en consola

---

## 📊 Monitoreo de Uso

### Ver uso en tiempo real
```python
encoder = LLMSemanticEncoder(model="gpt-3.5-turbo")

# Procesar textos
for text in texts:
    result = encoder.encode(text)
    
    # Info de caché
    if text in encoder.cache:
        print("📦 Cache hit")
    else:
        print("🌐 API call")
```

### Dashboard de OpenAI
Ve a https://platform.openai.com/usage para ver:
- Créditos consumidos
- Número de requests
- Tokens usados
- Costos por día/mes

---

## ✅ Checklist de Configuración

- [ ] Python 3.10+ instalado
- [ ] Cuenta OpenAI creada
- [ ] Créditos disponibles en cuenta
- [ ] API key generada
- [ ] Dependencias instaladas (`pip install openai python-dotenv`)
- [ ] Archivo `.env` creado con API key
- [ ] Test de conexión ejecutado (`python -c "..."`)
- [ ] Test básico ejecutado exitosamente
- [ ] `.env` añadido a `.gitignore`

---

## 🚀 Siguiente Paso

Una vez configurado, ejecuta los tests con API real:

```bash
python tests/test_llm_real_api.py
```

Si todos los tests pasan, ¡estás listo para usar el LLM Semantic Encoder en producción! 🎉

---

## 📚 Referencias

- **OpenAI API Docs:** https://platform.openai.com/docs/api-reference
- **Pricing:** https://openai.com/pricing
- **Rate Limits:** https://platform.openai.com/docs/guides/rate-limits
- **Best Practices:** https://platform.openai.com/docs/guides/prompt-engineering

---

**Última actualización:** 2024-01-XX  
**Mantenido por:** GitHub Copilot + Usuario (p_m_a)
