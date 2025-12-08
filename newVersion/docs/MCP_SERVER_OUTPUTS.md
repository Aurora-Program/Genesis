# 🔌 MCP Server - Opciones de Salida/Output

## 📊 ¿Qué salidas puede tener un MCP Server?

Los MCP servers pueden exponer **múltiples tipos de salidas** que otros sistemas pueden consumir:

---

## 🎯 1. **Tools** (Herramientas - Ya implementadas)

**Ya lo tienes**: `ffe_store`, `transcender_service`, etc.

```python
# FFEStoreMCPServer ya expone:
tools = [
    "ffe_store_tensor",      # Guardar tensor
    "ffe_query_recent",      # Consultar recientes
    "ffe_get_stats",         # Estadísticas
    "ffe_store_archetype",   # Guardar arquetipo
    "ffe_get_top_archetypes" # Top arquetipos
]
```

**Consumidores:**
- Claude Desktop
- VS Code Copilot
- Otros LLMs con MCP
- Scripts Python

---

## 🔔 2. **Resources** (Recursos - NUEVO)

Expone **contenido** que el LLM puede leer directamente.

### Ejemplos para Genesis:

```python
class FFEStoreMCPServer:
    def get_resources(self) -> List[Dict]:
        """Recursos MCP disponibles"""
        return [
            {
                "uri": "ffe://kb/recent",
                "name": "Recent Tensors",
                "description": "Últimos 20 tensores fractales",
                "mimeType": "application/json"
            },
            {
                "uri": "ffe://kb/archetypes",
                "name": "Universal Archetypes",
                "description": "Arquetipos universales descubiertos",
                "mimeType": "application/json"
            },
            {
                "uri": "ffe://kb/coherence/timeline",
                "name": "Coherence Timeline",
                "description": "Evolución de coherencia en el tiempo",
                "mimeType": "text/plain"
            },
            {
                "uri": "ffe://kb/spaces/{space_id}",
                "name": "Space Analysis",
                "description": "Análisis de un espacio lógico",
                "mimeType": "application/json"
            }
        ]
    
    def read_resource(self, uri: str) -> str:
        """Lee contenido de un recurso"""
        if uri == "ffe://kb/recent":
            tensors = self.store.query_recent(20)
            return json.dumps(tensors, indent=2)
        
        elif uri == "ffe://kb/archetypes":
            archetypes = self.store.get_top_archetypes(50)
            return json.dumps(archetypes, indent=2)
        
        elif uri == "ffe://kb/coherence/timeline":
            # Generar timeline ASCII art
            return self._generate_coherence_timeline()
        
        elif uri.startswith("ffe://kb/spaces/"):
            space_id = uri.split("/")[-1]
            return self._analyze_space(space_id)
```

**Uso en Claude/Copilot:**
```
Usuario: "Muéstrame los arquetipos universales"
LLM: [lee recurso ffe://kb/archetypes]
     "Aquí están los top 10 arquetipos universales..."
```

---

## 📢 3. **Prompts** (Plantillas - NUEVO)

Plantillas pre-configuradas para tareas comunes.

### Ejemplos para Genesis:

```python
class LLMSemanticEncoderMCPServer:
    def get_prompts(self) -> List[Dict]:
        """Prompts MCP disponibles"""
        return [
            {
                "name": "analyze_semantic_tensor",
                "description": "Analiza un tensor FFE y explica su significado",
                "arguments": [
                    {
                        "name": "tensor_id",
                        "description": "ID del tensor a analizar",
                        "required": True
                    }
                ]
            },
            {
                "name": "compare_tensors",
                "description": "Compara 2 tensores y encuentra similitudes",
                "arguments": [
                    {
                        "name": "tensor_a",
                        "description": "ID primer tensor",
                        "required": True
                    },
                    {
                        "name": "tensor_b",
                        "description": "ID segundo tensor",
                        "required": True
                    }
                ]
            },
            {
                "name": "discover_pattern",
                "description": "Descubre patrones en un espacio lógico",
                "arguments": [
                    {
                        "name": "space_id",
                        "description": "Espacio a analizar",
                        "required": True
                    }
                ]
            }
        ]
    
    def get_prompt(self, name: str, arguments: Dict) -> str:
        """Genera el prompt"""
        if name == "analyze_semantic_tensor":
            tensor = self.store.get_tensor(arguments["tensor_id"])
            return f"""Analiza este tensor fractal FFE:

Tensor: {tensor['tensor']}
Metadata: {tensor['metadata']}
Related content: {tensor.get('related_content', [])}

Explica:
1. ¿Qué patrón semántico representa?
2. ¿Qué estructura conceptual tiene?
3. ¿Con qué otros conceptos se relaciona?
"""
        
        elif name == "compare_tensors":
            tensor_a = self.store.get_tensor(arguments["tensor_a"])
            tensor_b = self.store.get_tensor(arguments["tensor_b"])
            return f"""Compara estos dos tensores:

TENSOR A:
{json.dumps(tensor_a, indent=2)}

TENSOR B:
{json.dumps(tensor_b, indent=2)}

Encuentra:
1. Similitudes estructurales
2. Diferencias semánticas
3. Relaciones potenciales
"""
```

**Uso:**
```
Usuario: "Analiza el tensor 42"
LLM: [usa prompt analyze_semantic_tensor con tensor_id=42]
     [recibe prompt pre-formateado con datos]
     "Este tensor representa un concepto de..."
```

---

## 📡 4. **Notifications** (Notificaciones - NUEVO)

El servidor **empuja** eventos a los clientes.

### Ejemplos para Genesis:

```python
class GenesisOrchestratorMCPServer:
    def __init__(self):
        self.subscribers = []
    
    def on_new_archetype(self, archetype: Dict):
        """Notifica cuando se descubre un arquetipo nuevo"""
        self.notify({
            "type": "archetype_discovered",
            "archetype": archetype,
            "timestamp": time.time(),
            "message": f"Nuevo arquetipo universal: {archetype['pattern']}"
        })
    
    def on_coherence_drop(self, space_id: str, coherence: float):
        """Alerta cuando la coherencia cae"""
        if coherence < 0.85:
            self.notify({
                "type": "coherence_alert",
                "space_id": space_id,
                "coherence": coherence,
                "severity": "warning",
                "message": f"⚠️ Coherencia baja en {space_id}: {coherence:.2f}"
            })
    
    def on_pattern_emergence(self, pattern: Dict):
        """Notifica patrones emergentes"""
        self.notify({
            "type": "pattern_emerged",
            "pattern": pattern,
            "occurrences": pattern['count'],
            "message": f"Patrón emergente detectado: {pattern['key']}"
        })
    
    def notify(self, event: Dict):
        """Envía notificación a todos los suscriptores"""
        for subscriber in self.subscribers:
            subscriber.send_notification(event)
```

**Uso:**
```
# En tiempo real, el LLM recibe:
🔔 Notificación MCP:
   Tipo: archetype_discovered
   Patrón: (1,0,1) → "concepto_abstracto"
   Espacios: filosofia, matematicas, poesia
   
LLM: "Interesante, he detectado un arquetipo universal..."
```

---

## 📊 5. **Sampling** (Monitoreo - NUEVO)

Expone métricas en tiempo real.

### Ejemplos para Genesis:

```python
class GenesisMetricsMCPServer:
    def get_sampling_capabilities(self) -> List[Dict]:
        """Métricas disponibles"""
        return [
            {
                "name": "system_coherence",
                "description": "Coherencia promedio del sistema",
                "unit": "ratio",
                "range": [0.0, 1.0]
            },
            {
                "name": "tensors_per_minute",
                "description": "Tasa de procesamiento",
                "unit": "count/minute"
            },
            {
                "name": "archetypes_discovered",
                "description": "Arquetipos únicos encontrados",
                "unit": "count"
            },
            {
                "name": "memory_usage",
                "description": "Uso de memoria KB",
                "unit": "MB"
            }
        ]
    
    def sample_metric(self, metric_name: str) -> float:
        """Lee valor actual de métrica"""
        if metric_name == "system_coherence":
            recent = self.store.query_recent(50)
            coherences = [t['coherence']['C_meta'] for t in recent]
            return sum(coherences) / len(coherences)
        
        elif metric_name == "tensors_per_minute":
            return self._calculate_processing_rate()
        
        elif metric_name == "archetypes_discovered":
            stats = self.store.get_stats()
            return stats['total_archetypes']
```

**Uso:**
```
# Claude/Copilot puede ver dashboard:

📊 Genesis System Metrics:
   Coherence:        ████████░░ 0.94
   Processing:       42 tensors/min
   Archetypes:       156 discovered
   Memory:           23.4 MB
```

---

## 🎨 6. **Visualizations** (Ya tienes base)

Ya tienes `fractal_visualizer.py`, puedes exponerlo como recurso MCP:

```python
class VisualizationMCPServer:
    def get_resources(self) -> List[Dict]:
        return [
            {
                "uri": "viz://tensor/{id}",
                "name": "Tensor 3D Graph",
                "mimeType": "image/svg+xml"  # O "text/html" con D3.js
            },
            {
                "uri": "viz://coherence/{space_id}",
                "name": "Coherence Timeline",
                "mimeType": "image/png"
            },
            {
                "uri": "viz://archetypes/clusters",
                "name": "Archetype Network",
                "mimeType": "application/vnd.graphml+xml"
            }
        ]
    
    def read_resource(self, uri: str) -> bytes:
        """Genera visualización"""
        if uri.startswith("viz://tensor/"):
            tensor_id = int(uri.split("/")[-1])
            svg = self.visualizer.render_tensor_svg(tensor_id)
            return svg.encode()
        
        elif uri.startswith("viz://coherence/"):
            space_id = uri.split("/")[-1]
            png = self.visualizer.render_coherence_chart(space_id)
            return png
```

**Uso en Claude Desktop:**
```
Usuario: "Visualiza el tensor 42"
LLM: [lee viz://tensor/42]
     [muestra SVG embebido en chat]
```

---

## 🚀 Recomendaciones para Genesis

### Implementar primero:

1. **Resources** ✅ PRIORIDAD ALTA
   - `ffe://kb/recent` - Tensores recientes
   - `ffe://kb/archetypes` - Arquetipos universales
   - `ffe://kb/spaces/{id}` - Análisis de espacio

2. **Prompts** ✅ PRIORIDAD ALTA
   - `analyze_semantic_tensor` - Análisis de tensor
   - `discover_pattern` - Descubrimiento de patrones
   - `compare_tensors` - Comparación semántica

3. **Notifications** ⚡ PRIORIDAD MEDIA
   - `archetype_discovered` - Nuevos arquetipos
   - `coherence_alert` - Alertas de coherencia
   - `pattern_emerged` - Patrones emergentes

4. **Sampling** 📊 PRIORIDAD BAJA
   - Métricas de sistema (después)

---

## 💡 Código Mínimo para Agregar

### Archivo: `newVersion/mcp_servers/genesis_mcp_server.py`

```python
"""
MCP Server completo para Genesis
Expone Tools + Resources + Prompts + Notifications
"""

from typing import List, Dict, Optional
import json
from pathlib import Path

class GenesisMCPServer:
    """MCP Server central de Genesis"""
    
    def __init__(self, ffe_store, encoder, visualizer):
        self.store = ffe_store
        self.encoder = encoder
        self.visualizer = visualizer
        self.subscribers = []
    
    # ========== TOOLS ==========
    def get_tools(self) -> List[Dict]:
        return [
            {
                "name": "encode_text",
                "description": "Convierte texto a tensor FFE semántico",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "depth": {"type": "integer", "default": 1}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "query_similar",
                "description": "Encuentra tensores similares",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "limit": {"type": "integer", "default": 5}
                    },
                    "required": ["text"]
                }
            }
        ]
    
    # ========== RESOURCES ==========
    def get_resources(self) -> List[Dict]:
        return [
            {
                "uri": "genesis://kb/recent",
                "name": "Recent Tensors",
                "mimeType": "application/json"
            },
            {
                "uri": "genesis://kb/archetypes",
                "name": "Universal Archetypes",
                "mimeType": "application/json"
            }
        ]
    
    def read_resource(self, uri: str) -> str:
        if uri == "genesis://kb/recent":
            return json.dumps(self.store.query_recent(20), indent=2)
        elif uri == "genesis://kb/archetypes":
            return json.dumps(self.store.get_top_archetypes(50), indent=2)
    
    # ========== PROMPTS ==========
    def get_prompts(self) -> List[Dict]:
        return [
            {
                "name": "analyze_tensor",
                "description": "Analiza tensor FFE semánticamente",
                "arguments": [
                    {"name": "tensor_id", "required": True}
                ]
            }
        ]
    
    def get_prompt(self, name: str, args: Dict) -> str:
        if name == "analyze_tensor":
            tensor = self.store.get_tensor(args["tensor_id"])
            return f"Analiza este tensor: {json.dumps(tensor, indent=2)}"
    
    # ========== NOTIFICATIONS ==========
    def notify_archetype(self, archetype: Dict):
        self._notify({
            "type": "archetype_discovered",
            "data": archetype
        })
    
    def _notify(self, event: Dict):
        for sub in self.subscribers:
            sub(event)
```

---

## ✅ Próximos Pasos

1. **Crear** `newVersion/mcp_servers/genesis_mcp_server.py` (arriba)
2. **Integrar** con `pipeline/llm_semantic_encoder.py`
3. **Exponer** como MCP server real (stdio transport)
4. **Configurar** en Claude Desktop / VS Code

¿Quieres que implemente el MCP server completo con todas las salidas? 🚀
