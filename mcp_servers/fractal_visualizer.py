"""
Fractal Visualization & Monitoring
===================================
Herramientas de visualización para tensores FFE, coherencia y arquetipos.

Componentes:
- Visualización 3D de tensores fractales
- Heatmap de coherencia temporal
- Clustering de arquetipos
- Métricas en tiempo real
- Export a formatos estándar (JSON, GraphML)
"""

import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VisualizationConfig:
    """Configuración de visualización"""
    include_metadata: bool = True
    color_scheme: str = "viridis"  # viridis, plasma, coolwarm
    graph_layout: str = "force"     # force, hierarchical, circular
    max_nodes: int = 100
    edge_threshold: float = 0.5     # Mínima strength para mostrar relación


class FractalVisualizer:
    """
    Generador de visualizaciones para tensores fractales.
    
    Produce representaciones para:
    - Estructura 3-9-27 del tensor
    - Coherencia temporal
    - Clusters de arquetipos
    - Grafo de relaciones
    """
    
    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()
        logger.info("FractalVisualizer initialized")
    
    def visualize_tensor(self, tensor_id: int, tensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera visualización de tensor fractal.
        
        Args:
            tensor_id: ID del tensor
            tensor_data: Datos del tensor (level_1, level_2, level_3)
        
        Returns:
            {
                "type": "fractal_tensor",
                "tensor_id": int,
                "graph_json": {...},
                "heatmap_data": [...],
                "summary": {...}
            }
        """
        ffe = tensor_data.get("ffe_tensor", {})
        
        if not ffe:
            return {"error": "Missing ffe_tensor data"}
        
        # Extraer niveles
        level_1 = ffe.get("level_1", [])
        level_2 = ffe.get("level_2", [])
        level_3 = ffe.get("level_3", [])
        
        # Generar estructura de grafo jerárquico
        nodes = []
        edges = []
        
        # Nivel 1: Axes (F, Fo, E)
        axis_names = ["Forma", "Función", "Estructura"]
        for i, (name, value) in enumerate(zip(axis_names, level_1)):
            nodes.append({
                "id": f"L1_{i}",
                "label": name,
                "level": 1,
                "value": value,
                "color": self._value_to_color(value, 7)
            })
        
        # Nivel 2: Subdimensiones (9 total)
        subdim_idx = 0
        for i, axis_values in enumerate(level_2):
            for j, value in enumerate(axis_values):
                node_id = f"L2_{subdim_idx}"
                nodes.append({
                    "id": node_id,
                    "label": f"{axis_names[i][:2]}{j+1}",
                    "level": 2,
                    "value": value,
                    "color": self._value_to_color(value, 7),
                    "parent": f"L1_{i}"
                })
                
                # Edge al padre
                edges.append({
                    "source": f"L1_{i}",
                    "target": node_id,
                    "weight": 1.0
                })
                
                subdim_idx += 1
        
        # Nivel 3: Especificaciones (27 total)
        spec_idx = 0
        for i, subdim_group in enumerate(level_3):
            for j, specs in enumerate(subdim_group):
                parent_id = f"L2_{i*3 + j}"
                for k, value in enumerate(specs):
                    node_id = f"L3_{spec_idx}"
                    nodes.append({
                        "id": node_id,
                        "label": f"S{spec_idx+1}",
                        "level": 3,
                        "value": value,
                        "color": self._value_to_color(value, 7),
                        "parent": parent_id
                    })
                    
                    # Edge al padre
                    edges.append({
                        "source": parent_id,
                        "target": node_id,
                        "weight": 0.5
                    })
                    
                    spec_idx += 1
        
        # Generar heatmap de valores
        flat = ffe.get("flat", [])
        heatmap_data = self._generate_heatmap(flat, width=13, height=3)
        
        # Resumen estadístico
        summary = self._tensor_summary(flat)
        
        return {
            "type": "fractal_tensor",
            "tensor_id": tensor_id,
            "graph_json": {
                "nodes": nodes,
                "edges": edges,
                "layout": self.config.graph_layout
            },
            "heatmap_data": heatmap_data,
            "summary": summary
        }
    
    def visualize_coherence_timeline(
        self,
        history: List[Dict[str, Any]],
        space_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Genera timeline de coherencia temporal.
        
        Args:
            history: Lista de turnos con coherence metrics
            space_id: Filtrar por espacio lógico
        
        Returns:
            {
                "type": "coherence_timeline",
                "timeline": [...],
                "heatmap": [...],
                "trends": {...}
            }
        """
        # Filtrar por espacio si aplica
        if space_id:
            history = [h for h in history if h.get("space_id") == space_id]
        
        if not history:
            return {"error": "No data for timeline"}
        
        # Extraer métricas
        timeline = []
        for i, turn in enumerate(history):
            coherence = turn.get("coherence", {})
            timeline.append({
                "turn_index": i,
                "turn_id": turn.get("turn_id"),
                "C_meta": coherence.get("C_meta", 0.0),
                "C_ext": coherence.get("C_ext", 0.0),
                "C_dyn": coherence.get("C_dyn", 0.0),
                "is_coherent": coherence.get("is_coherent", False),
                "timestamp": turn.get("timestamp", 0)
            })
        
        # Generar heatmap (turnos × métricas)
        heatmap = []
        for point in timeline:
            heatmap.append([
                point["C_meta"],
                point["C_ext"],
                point["C_dyn"]
            ])
        
        # Calcular tendencias
        c_meta_values = [p["C_meta"] for p in timeline]
        c_ext_values = [p["C_ext"] for p in timeline]
        c_dyn_values = [p["C_dyn"] for p in timeline]
        
        trends = {
            "C_meta": self._calculate_trend(c_meta_values),
            "C_ext": self._calculate_trend(c_ext_values),
            "C_dyn": self._calculate_trend(c_dyn_values),
            "coherent_ratio": sum(1 for p in timeline if p["is_coherent"]) / len(timeline)
        }
        
        return {
            "type": "coherence_timeline",
            "space_id": space_id or "all",
            "timeline": timeline,
            "heatmap": heatmap,
            "trends": trends,
            "total_turns": len(timeline)
        }
    
    def visualize_archetype_clusters(
        self,
        archetypes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genera clustering de arquetipos.
        
        Args:
            archetypes: Lista de arquetipos con pattern_key y metadata
        
        Returns:
            {
                "type": "archetype_clusters",
                "clusters": [...],
                "graph_json": {...}
            }
        """
        if not archetypes:
            return {"error": "No archetypes to visualize"}
        
        # Agrupar por espacios lógicos
        space_groups: Dict[str, List[Dict]] = {}
        for arch in archetypes:
            spaces = arch.get("spaces", [])
            for space in spaces:
                if space not in space_groups:
                    space_groups[space] = []
                space_groups[space].append(arch)
        
        # Crear nodos (arquetipos) y clusters (espacios)
        nodes = []
        clusters = []
        edges = []
        
        arch_idx = 0
        for space_id, arch_list in space_groups.items():
            # Cluster por espacio
            cluster_id = f"cluster_{space_id}"
            clusters.append({
                "id": cluster_id,
                "label": space_id,
                "size": len(arch_list),
                "color": self._space_to_color(space_id)
            })
            
            # Nodos de arquetipos
            for arch in arch_list:
                node_id = f"arch_{arch_idx}"
                nodes.append({
                    "id": node_id,
                    "label": arch.get("pattern_key", "unknown")[:16],
                    "cluster": cluster_id,
                    "frequency": arch.get("frequency", 1),
                    "coherence": arch.get("avg_coherence", 0.0),
                    "size": arch.get("frequency", 1) * 10
                })
                arch_idx += 1
        
        # Crear edges entre arquetipos similares (mismo Ms pattern)
        for i, arch1 in enumerate(archetypes):
            for j, arch2 in enumerate(archetypes[i+1:], start=i+1):
                if self._archetypes_similar(arch1, arch2):
                    edges.append({
                        "source": f"arch_{i}",
                        "target": f"arch_{j}",
                        "weight": 0.7,
                        "type": "similarity"
                    })
        
        return {
            "type": "archetype_clusters",
            "clusters": clusters,
            "graph_json": {
                "nodes": nodes,
                "edges": edges,
                "clusters": clusters,
                "layout": "force"
            },
            "total_archetypes": len(archetypes),
            "total_spaces": len(space_groups)
        }
    
    def visualize_relation_graph(
        self,
        relations: List[Dict[str, Any]],
        tensor_metadata: Dict[int, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genera grafo de relaciones entre tensores.
        
        Args:
            relations: Lista de relaciones {src, dst, type, strength}
            tensor_metadata: Metadata de tensores por ID
        
        Returns:
            {
                "type": "relation_graph",
                "graph_json": {...},
                "stats": {...}
            }
        """
        if not relations:
            return {"error": "No relations to visualize"}
        
        # Limitar número de nodos
        unique_tensors = set()
        for rel in relations:
            unique_tensors.add(rel["src"])
            unique_tensors.add(rel["dst"])
        
        if len(unique_tensors) > self.config.max_nodes:
            logger.warning(f"Too many nodes ({len(unique_tensors)}), limiting to {self.config.max_nodes}")
            # Tomar solo relaciones más fuertes
            relations = sorted(relations, key=lambda r: r.get("strength", 0), reverse=True)
            relations = relations[:self.config.max_nodes]
        
        # Crear nodos
        nodes = []
        for tensor_id in unique_tensors:
            metadata = tensor_metadata.get(tensor_id, {})
            nodes.append({
                "id": f"t_{tensor_id}",
                "label": f"T{tensor_id}",
                "space_id": metadata.get("space_id", "unknown"),
                "coherence": metadata.get("coherence", {}).get("C_meta", 0.0),
                "color": self._space_to_color(metadata.get("space_id", "default"))
            })
        
        # Crear edges (filtrar por threshold)
        edges = []
        for rel in relations:
            strength = rel.get("strength", 0.0)
            if strength >= self.config.edge_threshold:
                edges.append({
                    "source": f"t_{rel['src']}",
                    "target": f"t_{rel['dst']}",
                    "weight": strength,
                    "type": rel.get("type", "unknown")
                })
        
        # Estadísticas
        stats = {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "avg_strength": sum(e["weight"] for e in edges) / len(edges) if edges else 0.0,
            "relation_types": list(set(e["type"] for e in edges))
        }
        
        return {
            "type": "relation_graph",
            "graph_json": {
                "nodes": nodes,
                "edges": edges,
                "layout": self.config.graph_layout
            },
            "stats": stats
        }
    
    # Métodos auxiliares
    
    def _value_to_color(self, value: int, max_value: int) -> str:
        """Convierte valor discreto a color hex"""
        # Normalizar a [0, 1]
        normalized = value / max_value if max_value > 0 else 0.5
        
        # Gradiente simple (azul → verde → rojo)
        if normalized < 0.5:
            r = int(normalized * 2 * 255)
            g = int(normalized * 2 * 255)
            b = 255
        else:
            r = 255
            g = int((1 - normalized) * 2 * 255)
            b = int((1 - normalized) * 2 * 255)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _space_to_color(self, space_id: str) -> str:
        """Color consistente por espacio lógico"""
        # Hash del space_id para color determinístico
        hash_val = int(hashlib.md5(space_id.encode()).hexdigest()[:6], 16)
        r = (hash_val >> 16) & 0xFF
        g = (hash_val >> 8) & 0xFF
        b = hash_val & 0xFF
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _generate_heatmap(self, flat: List[int], width: int, height: int) -> List[List[int]]:
        """Genera matriz 2D para heatmap"""
        heatmap = []
        idx = 0
        for _ in range(height):
            row = []
            for _ in range(width):
                if idx < len(flat):
                    row.append(flat[idx])
                else:
                    row.append(0)
                idx += 1
            heatmap.append(row)
        return heatmap
    
    def _tensor_summary(self, flat: List[int]) -> Dict[str, Any]:
        """Resumen estadístico de tensor"""
        if not flat:
            return {}
        
        return {
            "min": min(flat),
            "max": max(flat),
            "mean": sum(flat) / len(flat),
            "unique_values": len(set(flat)),
            "most_common": max(set(flat), key=flat.count)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendencia de serie temporal"""
        if len(values) < 2:
            return "unknown"
        
        # Regresión lineal simple
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if slope > 0.01:
            return "improving"
        elif slope < -0.01:
            return "degrading"
        else:
            return "stable"
    
    def _archetypes_similar(self, arch1: Dict, arch2: Dict) -> bool:
        """Verifica si dos arquetipos son similares"""
        # Por simplicidad, verificar si comparten pattern_key prefix
        key1 = arch1.get("pattern_key", "")
        key2 = arch2.get("pattern_key", "")
        
        if not key1 or not key2:
            return False
        
        # Comparar primeros 8 caracteres (hash parcial)
        return key1[:8] == key2[:8]


class MonitoringDashboard:
    """
    Dashboard de monitoreo en tiempo real.
    
    Proporciona endpoints para métricas agregadas y visualizaciones.
    """
    
    def __init__(self, visualizer: Optional[FractalVisualizer] = None):
        self.visualizer = visualizer or FractalVisualizer()
        logger.info("MonitoringDashboard initialized")
    
    def get_system_overview(self, ffe_store) -> Dict[str, Any]:
        """
        Vista general del sistema.
        
        Args:
            ffe_store: Instancia de FFEStore
        
        Returns:
            Métricas agregadas y estadísticas
        """
        stats = ffe_store.get_stats()
        
        # Agregar visualizaciones
        overview = {
            "timestamp": stats.get("timestamp"),
            "tensors": {
                "total": stats.get("total_tensors", 0),
                "by_space": stats.get("tensors_by_space", {})
            },
            "archetypes": {
                "total": stats.get("total_archetypes", 0),
                "top_10": stats.get("top_archetypes", [])
            },
            "health": "healthy" if stats.get("total_tensors", 0) > 0 else "empty"
        }
        
        return overview
    
    def get_space_analysis(
        self,
        space_id: str,
        ffe_store,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Análisis detallado de un espacio lógico.
        
        Args:
            space_id: Espacio a analizar
            ffe_store: Instancia de FFEStore
            limit: Número de turnos recientes
        
        Returns:
            Visualizaciones y métricas del espacio
        """
        # Obtener tensores recientes del espacio
        recent = ffe_store.query_recent(limit=limit)
        space_tensors = [t for t in recent if t.get("space_id") == space_id]
        
        if not space_tensors:
            return {"error": f"No data for space '{space_id}'"}
        
        # Generar visualizaciones
        coherence_viz = self.visualizer.visualize_coherence_timeline(space_tensors, space_id)
        
        # Arquetipos del espacio
        archetypes = [
            arch for arch in ffe_store.get_top_archetypes(limit=50)
            if space_id in arch.get("spaces", [])
        ]
        archetype_viz = self.visualizer.visualize_archetype_clusters(archetypes)
        
        return {
            "space_id": space_id,
            "total_tensors": len(space_tensors),
            "coherence_timeline": coherence_viz,
            "archetype_clusters": archetype_viz,
            "recent_tensors": space_tensors[:5]  # Top 5 más recientes
        }
    
    def export_visualization(
        self,
        viz_data: Dict[str, Any],
        format: str = "json"
    ) -> str:
        """
        Exporta visualización a formato estándar.
        
        Args:
            viz_data: Datos de visualización
            format: "json" | "graphml" | "cytoscape"
        
        Returns:
            String con datos exportados
        """
        if format == "json":
            return json.dumps(viz_data, indent=2)
        
        elif format == "graphml":
            return self._to_graphml(viz_data)
        
        elif format == "cytoscape":
            return self._to_cytoscape(viz_data)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _to_graphml(self, viz_data: Dict[str, Any]) -> str:
        """Convierte a formato GraphML"""
        graph = viz_data.get("graph_json", {})
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        xml.append('  <graph id="G" edgedefault="directed">')
        
        # Nodos
        for node in nodes:
            xml.append(f'    <node id="{node["id"]}">')
            xml.append(f'      <data key="label">{node.get("label", "")}</data>')
            xml.append('    </node>')
        
        # Edges
        for i, edge in enumerate(edges):
            xml.append(f'    <edge id="e{i}" source="{edge["source"]}" target="{edge["target"]}">')
            xml.append(f'      <data key="weight">{edge.get("weight", 1.0)}</data>')
            xml.append('    </edge>')
        
        xml.append('  </graph>')
        xml.append('</graphml>')
        
        return '\n'.join(xml)
    
    def _to_cytoscape(self, viz_data: Dict[str, Any]) -> str:
        """Convierte a formato Cytoscape.js"""
        graph = viz_data.get("graph_json", {})
        
        cytoscape = {
            "elements": {
                "nodes": [
                    {"data": node}
                    for node in graph.get("nodes", [])
                ],
                "edges": [
                    {"data": edge}
                    for edge in graph.get("edges", [])
                ]
            },
            "style": [
                {
                    "selector": "node",
                    "style": {
                        "background-color": "data(color)",
                        "label": "data(label)"
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "width": "data(weight)",
                        "line-color": "#ccc"
                    }
                }
            ]
        }
        
        return json.dumps(cytoscape, indent=2)


if __name__ == "__main__":
    # Demo de visualización
    print("📊 Fractal Visualization Demo\n")
    
    visualizer = FractalVisualizer()
    
    # 1. Visualizar tensor
    print("1. Tensor Visualization:")
    tensor_data = {
        "ffe_tensor": {
            "level_1": [3, 4, 5],
            "level_2": [[3, 4, 5]] * 3,
            "level_3": [[[3, 4, 5]] * 3] * 3,
            "flat": [3, 4, 5] * 13
        }
    }
    
    viz = visualizer.visualize_tensor(42, tensor_data)
    print(f"   Type: {viz['type']}")
    print(f"   Nodes: {len(viz['graph_json']['nodes'])}")
    print(f"   Edges: {len(viz['graph_json']['edges'])}")
    print(f"   Summary: {viz['summary']}\n")
    
    # 2. Timeline de coherencia
    print("2. Coherence Timeline:")
    history = [
        {
            "turn_id": f"t{i}",
            "space_id": "test",
            "coherence": {
                "C_meta": 0.90 + i * 0.01,
                "C_ext": 0.95,
                "C_dyn": 0.92 - i * 0.01,
                "is_coherent": True
            },
            "timestamp": 1000 + i
        }
        for i in range(10)
    ]
    
    timeline_viz = visualizer.visualize_coherence_timeline(history, "test")
    print(f"   Turns: {timeline_viz['total_turns']}")
    print(f"   Trends: {timeline_viz['trends']}\n")
    
    # 3. Clusters de arquetipos
    print("3. Archetype Clusters:")
    archetypes = [
        {
            "pattern_key": f"pattern_{i}",
            "spaces": ["space_A", "space_B"],
            "frequency": 5 + i,
            "avg_coherence": 0.9 + i * 0.01
        }
        for i in range(5)
    ]
    
    cluster_viz = visualizer.visualize_archetype_clusters(archetypes)
    print(f"   Total archetypes: {cluster_viz['total_archetypes']}")
    print(f"   Spaces: {cluster_viz['total_spaces']}\n")
    
    print("✅ Demo completed")
