# 🚨 IMPORTANTE: Filosofía de Diseño Genesis

## Principio Fundamental: NO MODIFICAR EL CORE

El archivo `core.py` (Trinity-3 v2.0) es la **referencia canónica** del sistema Aurora. 

### ❌ PROHIBIDO
- Modificar cualquier firma de método del core
- "Simplificar" o "mejorar" el diseño original
- Cambiar la estructura de datos del core
- Alterar la lógica de Trigate, Transcender, Evolver, etc.

### ✅ PERMITIDO
- Crear **adapters** en el pipeline para compatibilidad
- Agregar **wrappers** que preserven las firmas originales
- Extender funcionalidad SIN modificar el core
- Documentar diferencias de uso

## Lección Aprendida

> "Ya he visto que eso ha pasado más veces" - Usuario

La simplificación prematura pierde el **espíritu del diseño inicial**. El core tiene razones profundas para su estructura:

1. **Consistencia**: Mismo código en todas las áreas del programa
2. **Integridad**: El diseño Trinity-3 es coherente internamente
3. **Evolución**: El core puede evolucionar independientemente
4. **Confianza**: Una sola fuente de verdad

## Estrategia Correcta: Copy, Don't Modify

### Paso 1: Copiar literalmente del core.py
```bash
# Extraer secciones exactas del core.py
# Sin cambios, sin "mejoras"
```

### Paso 2: Crear adapters en pipeline
```python
# En pipeline/aurora_pipeline.py

class EvolverAdapter:
    """Adapter para mantener compatibilidad con firmas del core"""
    def __init__(self, evolver_core):
        self._evolver = evolver_core
    
    def observe_fractal_safe(self, data, tag="default"):
        """Wrapper que adapta la llamada al core sin modificarlo"""
        # Usa la firma EXACTA del core
        return self._evolver.observe_fractal(data, tag)
```

### Paso 3: Pipeline como orquestador
- El pipeline **usa** el core, no lo modifica
- Toda lógica de adaptación va en el pipeline
- El core permanece puro e inmutable

## Ejemplo de Error Corregido

### ❌ Incorrecto (modificar core)
```python
# En core/evolver.py
def observe_fractal(self, res, *, level_name: str = "default"):  # ← Modificado
    ...
```

### ✅ Correcto (adaptar en pipeline)
```python
# En pipeline/aurora_pipeline.py
def store(self, key, data, tag="default"):
    if "audits" in data:
        # Usa la firma ORIGINAL del core (positional arg)
        self.evolver.observe_fractal(data, tag)  # ← Sin modificar core
```

## Regla de Oro

**Si necesitas cambiar algo del core, primero pregúntate:**
1. ¿Puedo resolver esto con un adapter?
2. ¿Puedo resolver esto con un wrapper?
3. ¿Puedo resolver esto en el pipeline?

**Solo si las 3 respuestas son "NO", considera modificar el core.**
(Y aún así, consulta primero)

---

**Versión**: 1.0.0  
**Fecha**: 2025-10-20  
**Lección**: Preservar el espíritu del diseño original
