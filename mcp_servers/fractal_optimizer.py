"""
Fractal Memory Optimizer
=========================
Optimizaciones avanzadas de memoria fractal:
- Cuantización adaptativa según contexto
- Compresión diferencial entre turnos
- Cache de arquetipos frecuentes
- Pruning de patrones irrelevantes

Basado en principios de:
- Sparse coding
- Differential encoding
- LRU caching con prioridad por coherencia
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompressionStats:
    """Estadísticas de compresión"""
    original_size_bytes: int = 0
    compressed_size_bytes: int = 0
    compression_ratio: float = 1.0
    differential_savings: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    def update(self, original: int, compressed: int):
        """Actualiza estadísticas"""
        self.original_size_bytes += original
        self.compressed_size_bytes += compressed
        if self.original_size_bytes > 0:
            self.compression_ratio = self.compressed_size_bytes / self.original_size_bytes
    
    def get_summary(self) -> Dict[str, Any]:
        """Resumen de estadísticas"""
        cache_rate = (self.cache_hits / (self.cache_hits + self.cache_misses) * 100) if (self.cache_hits + self.cache_misses) > 0 else 0.0
        
        return {
            "original_size_kb": f"{self.original_size_bytes / 1024:.2f}",
            "compressed_size_kb": f"{self.compressed_size_bytes / 1024:.2f}",
            "compression_ratio": f"{self.compression_ratio:.3f}",
            "savings_percent": f"{(1 - self.compression_ratio) * 100:.1f}%",
            "differential_savings_bytes": self.differential_savings,
            "cache_hit_rate": f"{cache_rate:.1f}%"
        }


class AdaptiveQuantizer:
    """
    Cuantizador adaptativo basado en distribución de valores.
    
    En lugar de siempre usar 0-7, ajusta niveles según:
    - Entropía del embedding
    - Contexto del espacio lógico
    - Historial de valores
    """
    
    def __init__(self):
        # Historial de distribuciones por espacio lógico
        self.distributions: Dict[str, np.ndarray] = {}
        
        # Configuración adaptativa
        self.default_levels = 8  # 0-7
        self.min_levels = 4      # Para embeddings de baja entropía
        self.max_levels = 16     # Para embeddings complejos
    
    def quantize_adaptive(
        self,
        values: np.ndarray,
        space_id: str = "default"
    ) -> Tuple[List[int], int]:
        """
        Cuantiza valores adaptando niveles según entropía.
        
        Args:
            values: Array de valores a cuantizar
            space_id: Espacio lógico para contexto
        
        Returns:
            (quantized_values, num_levels_used)
        """
        # Calcular entropía del embedding
        entropy = self._calculate_entropy(values)
        
        # Decidir niveles de cuantización
        if entropy < 0.3:  # Baja entropía → menos niveles
            num_levels = self.min_levels
        elif entropy > 0.7:  # Alta entropía → más niveles
            num_levels = self.max_levels
        else:
            num_levels = self.default_levels
        
        # Normalizar a [0, 1]
        normalized = (values - values.min()) / (values.max() - values.min() + 1e-8)
        
        # Cuantizar
        quantized = (normalized * (num_levels - 1)).astype(int)
        quantized = np.clip(quantized, 0, num_levels - 1)
        
        # Actualizar distribución del espacio
        self._update_distribution(space_id, quantized, num_levels)
        
        logger.debug(f"Adaptive quantization: entropy={entropy:.3f}, levels={num_levels}")
        
        return quantized.tolist(), num_levels
    
    def _calculate_entropy(self, values: np.ndarray) -> float:
        """Calcula entropía normalizada de valores"""
        # Discretizar para histograma
        hist, _ = np.histogram(values, bins=20, density=True)
        hist = hist[hist > 0]  # Eliminar bins vacíos
        
        # Entropía de Shannon normalizada
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        max_entropy = np.log2(len(hist)) if len(hist) > 0 else 1.0
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _update_distribution(self, space_id: str, quantized: np.ndarray, num_levels: int):
        """Actualiza distribución histórica del espacio"""
        if space_id not in self.distributions:
            self.distributions[space_id] = np.zeros(num_levels)
        
        # Acumular histograma
        for val in quantized:
            if val < len(self.distributions[space_id]):
                self.distributions[space_id][val] += 1
    
    def get_distribution_stats(self, space_id: str) -> Dict[str, Any]:
        """Estadísticas de distribución del espacio"""
        if space_id not in self.distributions:
            return {"error": "No data for space"}
        
        dist = self.distributions[space_id]
        total = dist.sum()
        
        if total == 0:
            return {"error": "Empty distribution"}
        
        probs = dist / total
        entropy = -np.sum(probs[probs > 0] * np.log2(probs[probs > 0]))
        
        return {
            "space_id": space_id,
            "total_samples": int(total),
            "entropy": f"{entropy:.3f}",
            "most_common_value": int(np.argmax(dist)),
            "distribution": probs.tolist()
        }


class DifferentialEncoder:
    """
    Codificación diferencial entre turnos consecutivos.
    
    Solo almacena las diferencias respecto al turno anterior,
    aprovechando la localidad temporal en conversaciones.
    """
    
    def __init__(self):
        # Último tensor por espacio lógico
        self.last_tensors: Dict[str, List[int]] = {}
        self.stats = CompressionStats()
    
    def encode_differential(
        self,
        current_tensor: List[int],
        space_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Codifica tensor como diferencia del anterior.
        
        Returns:
            {
                "type": "full" | "differential",
                "data": encoded_data,
                "original_size": int,
                "compressed_size": int
            }
        """
        # Si no hay tensor previo, almacenar completo
        if space_id not in self.last_tensors:
            self.last_tensors[space_id] = current_tensor
            
            original_size = len(current_tensor) * 4  # 4 bytes por int
            
            self.stats.update(original_size, original_size)
            
            return {
                "type": "full",
                "data": current_tensor,
                "original_size": original_size,
                "compressed_size": original_size,
                "space_id": space_id
            }
        
        # Calcular diferencias
        prev_tensor = self.last_tensors[space_id]
        diffs = []
        indices = []
        
        for i, (curr, prev) in enumerate(zip(current_tensor, prev_tensor)):
            if curr != prev:
                diffs.append(curr - prev)
                indices.append(i)
        
        # Decidir si vale la pena diferencial
        original_size = len(current_tensor) * 4
        diff_size = (len(diffs) + len(indices)) * 4
        
        if diff_size < original_size * 0.7:  # Al menos 30% de ahorro
            self.last_tensors[space_id] = current_tensor
            self.stats.update(original_size, diff_size)
            self.stats.differential_savings += (original_size - diff_size)
            
            return {
                "type": "differential",
                "data": {"indices": indices, "diffs": diffs},
                "base_hash": self._hash_tensor(prev_tensor),
                "original_size": original_size,
                "compressed_size": diff_size,
                "space_id": space_id
            }
        else:
            # No vale la pena, usar codificación completa
            self.last_tensors[space_id] = current_tensor
            self.stats.update(original_size, original_size)
            
            return {
                "type": "full",
                "data": current_tensor,
                "original_size": original_size,
                "compressed_size": original_size,
                "space_id": space_id
            }
    
    def decode_differential(self, encoded: Dict[str, Any]) -> List[int]:
        """Decodifica tensor desde representación diferencial"""
        if encoded["type"] == "full":
            return encoded["data"]
        
        # Reconstruir desde diferencias
        space_id = encoded["space_id"]
        base_tensor = self.last_tensors.get(space_id)
        
        if base_tensor is None:
            raise ValueError(f"Missing base tensor for space '{space_id}'")
        
        # Aplicar diferencias
        result = base_tensor.copy()
        data = encoded["data"]
        
        for idx, diff in zip(data["indices"], data["diffs"]):
            result[idx] += diff
        
        return result
    
    def _hash_tensor(self, tensor: List[int]) -> str:
        """Hash de tensor para verificación"""
        tensor_bytes = bytes(tensor)
        return hashlib.sha256(tensor_bytes).hexdigest()[:16]
    
    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas de compresión diferencial"""
        return self.stats.get_summary()


class ArchetypeCache:
    """
    Cache LRU de arquetipos con prioridad por coherencia.
    
    Cachea arquetipos frecuentes para acelerar Evolver,
    priorizando patrones con mayor coherencia C_meta.
    """
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        
        # OrderedDict para LRU
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        
        # Prioridades por coherencia
        self.priorities: Dict[str, float] = {}
        
        self.stats = CompressionStats()
    
    def get(self, pattern_key: str) -> Optional[Dict[str, Any]]:
        """Obtiene arquetipo del cache"""
        if pattern_key in self.cache:
            # Mover al final (más reciente)
            self.cache.move_to_end(pattern_key)
            self.stats.cache_hits += 1
            
            logger.debug(f"Cache HIT: {pattern_key}")
            return self.cache[pattern_key]
        
        self.stats.cache_misses += 1
        logger.debug(f"Cache MISS: {pattern_key}")
        return None
    
    def put(
        self,
        pattern_key: str,
        archetype_data: Dict[str, Any],
        coherence: float = 0.0
    ):
        """Almacena arquetipo en cache con prioridad"""
        # Si ya existe, actualizar
        if pattern_key in self.cache:
            self.cache.move_to_end(pattern_key)
            self.cache[pattern_key] = archetype_data
            self.priorities[pattern_key] = coherence
            return
        
        # Si cache lleno, remover según prioridad
        if len(self.cache) >= self.max_size:
            self._evict_lowest_priority()
        
        # Insertar nuevo
        self.cache[pattern_key] = archetype_data
        self.priorities[pattern_key] = coherence
    
    def _evict_lowest_priority(self):
        """Remueve arquetipo con menor prioridad (coherencia)"""
        if not self.cache:
            return
        
        # Encontrar clave con menor prioridad
        min_key = min(self.priorities.keys(), key=lambda k: self.priorities[k])
        
        logger.debug(f"Cache eviction: {min_key} (priority={self.priorities[min_key]:.3f})")
        
        del self.cache[min_key]
        del self.priorities[min_key]
    
    def get_top_patterns(self, limit: int = 10) -> List[Tuple[str, float]]:
        """Obtiene patrones más prioritarios"""
        sorted_patterns = sorted(
            self.priorities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_patterns[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas del cache"""
        total_requests = self.stats.cache_hits + self.stats.cache_misses
        hit_rate = (self.stats.cache_hits / total_requests * 100) if total_requests > 0 else 0.0
        
        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": f"{hit_rate:.1f}%",
            "total_hits": self.stats.cache_hits,
            "total_misses": self.stats.cache_misses,
            "avg_priority": f"{np.mean(list(self.priorities.values())):.3f}" if self.priorities else "N/A"
        }


class FractalOptimizer:
    """
    Optimizador integral de memoria fractal.
    
    Integra:
    - Cuantización adaptativa
    - Codificación diferencial
    - Cache de arquetipos
    """
    
    def __init__(self, cache_size: int = 100):
        self.quantizer = AdaptiveQuantizer()
        self.differential = DifferentialEncoder()
        self.cache = ArchetypeCache(max_size=cache_size)
        
        logger.info("FractalOptimizer initialized")
    
    def optimize_tensor(
        self,
        tensor_flat: List[int],
        space_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Optimiza almacenamiento de tensor completo.
        
        Returns:
            Tensor optimizado con estadísticas
        """
        # Codificación diferencial
        encoded = self.differential.encode_differential(tensor_flat, space_id)
        
        return {
            "encoded": encoded,
            "space_id": space_id,
            "optimization": "differential",
            "stats": self.differential.get_stats()
        }
    
    def optimize_embedding(
        self,
        embedding: np.ndarray,
        space_id: str = "default"
    ) -> Tuple[List[int], Dict[str, Any]]:
        """
        Optimiza codificación de embedding a FFE.
        
        Returns:
            (quantized_values, optimization_info)
        """
        quantized, num_levels = self.quantizer.quantize_adaptive(embedding, space_id)
        
        info = {
            "num_levels_used": num_levels,
            "space_id": space_id,
            "distribution": self.quantizer.get_distribution_stats(space_id)
        }
        
        return quantized, info
    
    def cache_archetype(
        self,
        pattern_key: str,
        archetype_data: Dict[str, Any],
        coherence: float
    ):
        """Cachea arquetipo con prioridad"""
        self.cache.put(pattern_key, archetype_data, coherence)
    
    def get_cached_archetype(self, pattern_key: str) -> Optional[Dict[str, Any]]:
        """Obtiene arquetipo del cache"""
        return self.cache.get(pattern_key)
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Estadísticas consolidadas de optimización"""
        return {
            "differential_encoding": self.differential.get_stats(),
            "archetype_cache": self.cache.get_stats(),
            "top_cached_patterns": self.cache.get_top_patterns(5)
        }


if __name__ == "__main__":
    # Demo de optimización
    print("⚡ Fractal Optimizer Demo\n")
    
    optimizer = FractalOptimizer(cache_size=50)
    
    # 1. Cuantización adaptativa
    print("1. Adaptive Quantization:")
    embedding_low_entropy = np.random.normal(0.5, 0.1, 100)  # Baja entropía
    embedding_high_entropy = np.random.uniform(0, 1, 100)    # Alta entropía
    
    quant_low, info_low = optimizer.optimize_embedding(embedding_low_entropy, "space_A")
    quant_high, info_high = optimizer.optimize_embedding(embedding_high_entropy, "space_B")
    
    print(f"   Low entropy: {info_low['num_levels_used']} levels")
    print(f"   High entropy: {info_high['num_levels_used']} levels\n")
    
    # 2. Codificación diferencial
    print("2. Differential Encoding:")
    tensor1 = [3, 4, 5] * 13  # 39 elementos
    tensor2 = [3, 4, 6] * 13  # Solo un valor diferente repetido
    
    opt1 = optimizer.optimize_tensor(tensor1, "conv_1")
    print(f"   Turn 1: {opt1['encoded']['type']}, {opt1['encoded']['compressed_size']} bytes")
    
    opt2 = optimizer.optimize_tensor(tensor2, "conv_1")
    print(f"   Turn 2: {opt2['encoded']['type']}, {opt2['encoded']['compressed_size']} bytes")
    print(f"   Savings: {opt2['encoded']['original_size'] - opt2['encoded']['compressed_size']} bytes\n")
    
    # 3. Cache de arquetipos
    print("3. Archetype Cache:")
    optimizer.cache_archetype("pattern_A", {"Ms": [1, 2, 3]}, coherence=0.95)
    optimizer.cache_archetype("pattern_B", {"Ms": [4, 5, 6]}, coherence=0.80)
    optimizer.cache_archetype("pattern_C", {"Ms": [7, 8, 9]}, coherence=0.92)
    
    cached = optimizer.get_cached_archetype("pattern_A")
    print(f"   Cached pattern_A: {cached}")
    
    stats = optimizer.get_comprehensive_stats()
    print(f"\n   Cache stats: {stats['archetype_cache']}")
    print(f"   Top patterns: {stats['top_cached_patterns']}\n")
    
    print("✅ Demo completed")
