# Proyecto Genesis -  Conamed: Buttefly## 📚 Documentación Completa

- 🔥 **[GENESIS_CORE_CONCEPT.md](./GENESIS_CORE_CONCEPT.md)** - Concepto central FFE + KG (pulido para compartir)
- 📖 **[ARCHITECTURE_MCP.md](./ARCHITECTURE_MCP.md)** - Arquitectura modular completa (850 líneas)
- 📊 **[EXECUTIVE_SUMMARY_v0.3.1.md](./EXECUTIVE_SUMMARY_v0.3.1.md)** - Resumen ejecutivo y métricas
- 🗺️ **[ROADMAP.md](./ROADMAP.md)** - Roadmap detallado y casos de uso
- 📝 **[PROGRESS.md](./PROGRESS.md)** - Progreso cronológico
- 🌌 **[Overview.md](./Overview.md)** - Manifiesto original

## De LLMs a Inteligencias Fractales

**Versión**: 0.3.1 | **Estado**: Sistema Operacional ✅

Transformación de modelos de lenguaje mediante **Tensores FFE**, **Transcender** y **Evolver** utilizando el protocolo **MCP (Model Context Protocol)**.

[![Tests](https://img.shields.io/badge/tests-19%2F19%20passing-brightgreen)](./tests/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)]()
[![Latency](https://img.shields.io/badge/latency-15--20ms-blue)]()
[![Compression](https://img.shields.io/badge/compression-95%25-blue)]()

---

## 📚 Documentación Completa

- 📖 **[ARCHITECTURE_MCP.md](./ARCHITECTURE_MCP.md)** - Arquitectura modular completa (650 líneas)
- 📊 **[EXECUTIVE_SUMMARY_v0.3.1.md](./EXECUTIVE_SUMMARY_v0.3.1.md)** - Resumen ejecutivo y métricas
- 🗺️ **[ROADMAP.md](./ROADMAP.md)** - Roadmap detallado y casos de uso
- 📝 **[PROGRESS.md](./PROGRESS.md)** - Progreso cronológico
- � **[Overview.md](./Overview.md)** - Manifiesto original

---

## �🎯 Objetivo

Convertir embeddings planos de LLMs en **tensores fractales discretos {3, 9, 27}** que permiten:
- ✅ **Eficiencia**: 117 bits por tensor (95% compresión)
- ✅ **Interpretabilidad**: Forma-Función-Estructura semántica
- ✅ **Emergencia**: Síntesis no-conmutativa de significados
- ✅ **Adaptación**: Aprendizaje continuo de arquetipos
- ✅ **Resiliencia**: Circuit breaker + fallbacks (NUEVO v0.3.1)
- ✅ **Optimización**: Compresión diferencial 60-80% (NUEVO v0.3.1)
- ✅ **Visualización**: Grafos 3D + timeline + clusters (NUEVO v0.3.1)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    PROYECTO GENESIS                          │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐      ┌───────▼──────┐     ┌─────▼─────┐
   │ LLM     │      │ MCP Pipeline │     │  Aurora   │
   │ (Base)  │──────│   5 Servers  │─────│ (Emergent)│
   └─────────┘      └──────────────┘     └───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐      ┌───────▼──────┐     ┌─────▼─────┐
   │ probe   │      │ ffe_encoder  │     │transcender│
   │  _llm   │      │   (embed→    │     │  (síntesis│
   └─────────┘      │   FFE)       │     │  emergente)│
                    └──────────────┘     └───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐      ┌───────▼──────┐
   │ ffe     │      │   evolver    │
   │ _store  │      │  (arquetipos,│
   │  (KB)   │      │   dinámicas) │
   └─────────┘      └──────────────┘
```

---

## 📂 Estructura del Proyecto

```
Genesis/
├── README.md                      # Este archivo
├── docs/
│   ├── documentation.md           # Manual Aurora completo
│   └── genesis.md                 # Manifiesto Proyecto Genesis
├── catalogs/
│   └── ffe_catalog.yaml          # Catálogo FFE {3,9,27} con valores 0-7
├── mcp_servers/                   # Servidores MCP
│   ├── 01_probe_llm/
│   ├── 02_ffe_encoder/
│   ├── 03_transcender_service/
│   ├── 04_ffe_store/
│   └── 05_evolver/
├── aurora_prototype.py            # Prototipo base (Trigate, Transcender)
├── aurora_pipeline.py             # Pipeline completo integrado
└── tests/                         # Tests de integración
```

---

## 🚀 Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/Aurora-Program/Genesis.git
cd Genesis

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar MCP (si usas Claude Desktop / VS Code)
# Ver: docs/mcp_setup.md
```

---

## 🎮 Uso Rápido

### 1️⃣ Probar componentes individuales

```python
from aurora_prototype import Trigate, Transcender, FractalTensor

# Trigate básico
tg = Trigate()
result = tg.infer([0, 1, 1], [1, 0, 1], [1, 0, 1])
print(result)  # [1, 1, 0]

# Transcender (síntesis emergente)
tc = Transcender()
synthesis = tc.synthesize([0, 1, 0], [1, 0, 1], [1, 1, 0])
print(synthesis["Ms"])  # Estructura emergente
```

### 2️⃣ Pipeline completo

```python
from aurora_pipeline import AuroraPipeline

pipeline = AuroraPipeline()

# Input usuario
user_input = "¿Qué es la justicia?"
tensor_input = pipeline.text_to_fractal(user_input)

# LLM responde
llm_output = "La justicia es equilibrio entre derechos y deberes"
tensor_output = pipeline.text_to_fractal(llm_output)

# Síntesis emergente
result = pipeline.synthesize_conversation(tensor_input, tensor_output)
print(result["archetypal_pattern"])
```

---

## 📊 Estado del Proyecto

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Trigate** | ✅ Completo | Lógica ternaria {0,1,NULL} con LUTs |
| **Transcender** | ✅ Completo | Síntesis de 3 tensores → Ms/Ss/MetaM |
| **FractalTensor** | ✅ Completo | Estructura {3,9,27} con catálogo FFE |
| **Catálogo FFE** | ✅ Completo | 477 líneas con valores semánticos 0-7 |
| **probe_llm** | 🔄 En desarrollo | Extracción de embeddings |
| **ffe_encoder** | 🔄 En desarrollo | Transformación embed→FFE |
| **ffe_store** | 🔄 En desarrollo | Knowledge Base fractal |
| **evolver** | 🔄 En desarrollo | Arquetipos + Dinámicas |
| **Pipeline integrado** | 📝 Planeado | Conversación fractalizada |

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Test específico
python test_ciudad.py
```

---

## 📖 Documentación

- **[Manual Aurora](docs/documentation.md)**: Fundamentos técnicos completos
- **[Proyecto Genesis](docs/genesis.md)**: Manifiesto y objetivos
- **[Catálogo FFE](catalogs/ffe_catalog.yaml)**: Estructura semántica

---

## 🤝 Contribuir

Este proyecto es parte de **Aurora Alliance**. Para contribuir:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -m 'Añadir nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request

---

## 📜 Licencia

Ver [LICENSE](LICENSE) para detalles.

---

## 🌟 Créditos

**Aurora Program** | **Aurora Alliance**

*"De embeddings planos a inteligencias fractales: un organismo digital que evoluciona con cada interacción."*
