"""
FFE Encoder v0.2 - Trigate Quantizer
Convierte embeddings continuos → Tensores FFE discretos

Estrategia (modo trigate):
    1. Reducción dimensional: PCA (768 → 81 dims)
    2. Partición fija: 27 grupos × 3 componentes (FO/FN/ES)
    3. Cuantización ternaria con trigate: cada componente → Trit {0,1,None}
    4. Colapso triádico: construir niveles 9 y 3 por autosimilitud

Nota: Se elimina la dependencia de K-means; el Trigate es el núcleo.
"""

import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.trigate import Trit
from core.fractal_tensor import FractalTensor


@dataclass
class EncodingMetrics:
    """Métricas de calidad del encoding"""
    reconstruction_similarity: float  # cosine_sim(original, reconstructed)
    nulls_count: int                  # NULLs en tensor resultante
    cluster_coherence: float          # Cohesión de clusters
    transcender_score: Optional[int]  # Score del Transcender (si aplica)


class FFEEncoder:
    """
    Encoder que transforma embeddings → Tensores FFE.
    
    Arquitectura:
      embedding (768 dims) 
        → PCA (81 dims)
        → K-means (27 clusters)
        → Cuantización ternaria (27×3 bits = 81 bits)
        → FractalTensor {3, 9, 27}
    
    Parámetros críticos:
      - n_dims_pca: 81 (para 27 vectores de 3 bits)
    - quantization_mode: "trigate" | "legacy"
    """
    
    def __init__(
        self,
        embedding_dim: int = 768,
        n_dims_pca: int = 81,
        quantization_mode: str = "trigate"
    ):
        self.embedding_dim = embedding_dim
        self.n_dims_pca = n_dims_pca
        self.quantization_mode = quantization_mode
        
        # Componentes entrenables
        self.pca = None
        
        # Umbrales por dimensión reducida (bajo PCA)
        self.thresholds_low = None  # np.ndarray shape (n_dims_pca,)
        self.thresholds_high = None # np.ndarray shape (n_dims_pca,)
        self.std_per_dim = None     # np.ndarray shape (n_dims_pca,)
        
        # Estado de entrenamiento
        self.is_fitted = False
    
    def fit(self, embeddings: np.ndarray):
        """
        Entrena el encoder con un conjunto de embeddings.
        
        Args:
            embeddings: np.ndarray shape (n_samples, embedding_dim)
        """
        print(f"🔧 Entrenando FFEEncoder (modo={self.quantization_mode}) con {len(embeddings)} muestras…")
        
        # 1) PCA: Reducción dimensional
        print(f"  → PCA: {self.embedding_dim} → {self.n_dims_pca} dims")
        self.pca = PCA(n_components=self.n_dims_pca)
        embeddings_reduced = self.pca.fit_transform(embeddings)
        variance_explained = sum(self.pca.explained_variance_ratio_)
        print(f"    Varianza explicada: {variance_explained:.2%}")
        
        # 2) Umbrales trigate por dimensión (adaptativos por STD)
        print("  → Umbrales trigate por dimensión (±0.5·std)")
        self.std_per_dim = np.std(embeddings_reduced, axis=0) + 1e-8
        self.thresholds_low = -0.5 * self.std_per_dim
        self.thresholds_high = 0.5 * self.std_per_dim
        
        self.is_fitted = True
        print("✅ Encoder entrenado\n")
    
    def encode(self, embedding: np.ndarray) -> FractalTensor:
        """
        Codifica un embedding a FractalTensor.
        
        Args:
            embedding: np.ndarray shape (embedding_dim,)
        
        Returns:
            FractalTensor con niveles {3, 9, 27}
        """
        if not self.is_fitted:
            raise ValueError("Encoder no entrenado. Llama a fit() primero.")
        
        # 1. Reducir con PCA
        embedding_reduced = self.pca.transform(embedding.reshape(1, -1))[0]
        
        # 2) Cuantización trigate por grupos fijos (27×3)
        nivel_27 = []
        for i in range(27):
            base = 3 * i
            f_val = embedding_reduced[base + 0] if base + 0 < len(embedding_reduced) else 0.0
            fu_val = embedding_reduced[base + 1] if base + 1 < len(embedding_reduced) else 0.0
            e_val = embedding_reduced[base + 2] if base + 2 < len(embedding_reduced) else 0.0
            v = [
                self._quantize_value(f_val, base + 0),
                self._quantize_value(fu_val, base + 1),
                self._quantize_value(e_val, base + 2)
            ]
            nivel_27.append(v)
        
        # 3) Autosimilitud: colapso triádico para niveles 9 y 3
        nivel_9 = []
        for i in range(0, 27, 3):
            nivel_9.append(self._collapse_vectors(nivel_27[i:i+3]))
        
        nivel_3 = []
        for i in range(0, 9, 3):
            nivel_3.append(self._collapse_vectors(nivel_9[i:i+3]))
        
        return FractalTensor(
            nivel_3=nivel_3,
            nivel_9=nivel_9,
            nivel_27=nivel_27
        ).normalize()
    
    def _quantize_value(self, val: float, dim_index: int) -> Trit:
        """Cuantiza valor escalar a Trit {0,1,None} con umbral adaptativo."""
        if dim_index >= self.n_dims_pca:
            dim_index = dim_index % self.n_dims_pca
        th_low = self.thresholds_low[dim_index]
        th_high = self.thresholds_high[dim_index]
        if val < th_low:
            return 0
        if val > th_high:
            return 1
        return None

    def _collapse_vectors(self, vecs: List[List[Trit]]) -> List[Trit]:
        """Colapso triádico componente a componente sobre 3 vectores FFE."""
        if not vecs:
            return [None, None, None]
        a = vecs[0]
        b = vecs[1] if len(vecs) > 1 else [None, None, None]
        c = vecs[2] if len(vecs) > 2 else [None, None, None]
        out: List[Trit] = []
        for i in range(3):
            vals = [a[i], b[i], c[i]]
            ones = sum(1 for v in vals if v == 1)
            zeros = sum(1 for v in vals if v == 0)
            if ones >= 2:
                out.append(1)
            elif zeros >= 2:
                out.append(0)
            else:
                out.append(None)
        return out
    
    def decode(self, tensor: FractalTensor) -> np.ndarray:
        """
        Decodifica FractalTensor → embedding aproximado.
        
        CRÍTICO para validación: Permite calcular
        cosine_sim(original, reconstructed)
        """
        if not self.is_fitted:
            raise ValueError("Encoder no entrenado.")
        
        # Reconstrucción simple: mapear Trits a offsets en el espacio reducido
        reduced = np.zeros(self.n_dims_pca, dtype=float)
        alpha = 0.5  # escala relativa al std
        for i, vec in enumerate(tensor.nivel_27):
            base = 3 * i
            for k in range(3):
                idx = base + k
                if idx >= self.n_dims_pca:
                    continue
                t = vec[k]
                if t is None:
                    continue
                sign = 1.0 if t == 1 else -1.0
                reduced[idx] = sign * alpha * float(self.std_per_dim[idx])
        
        embedding_reconstructed = self.pca.inverse_transform(reduced.reshape(1, -1))[0]
        return embedding_reconstructed
    
    # _ternary_to_offset ya no es necesario en modo trigate

    def tensor_similarity(self, a: FractalTensor, b: FractalTensor) -> float:
        """Similaridad coseno entre dos tensores FFE (nivel_27 flatten).
        Trit mapping: 1→1.0, 0→-1.0, None→0.0
        """
        def to_vec(t: FractalTensor) -> np.ndarray:
            vals = []
            for vec in t.nivel_27:
                for bit in vec:
                    if bit == 1:
                        vals.append(1.0)
                    elif bit == 0:
                        vals.append(-1.0)
                    else:
                        vals.append(0.0)
            return np.array(vals, dtype=float)
        va = to_vec(a)
        vb = to_vec(b)
        na = np.linalg.norm(va)
        nb = np.linalg.norm(vb)
        if na == 0 or nb == 0:
            return 0.0
        return float(np.dot(va, vb) / (na * nb))
    
    def validate(
        self,
        embeddings_test: np.ndarray
    ) -> EncodingMetrics:
        """
        Valida la calidad del encoding.
        
        Test crítico: embedding → FFE → embedding'
        → cosine_sim(embedding, embedding') > 0.85
        """
        print("🧪 Validando FFEEncoder (modo trigate)…")
        
        similarities = []
        null_counts = []
        
        for i, emb in enumerate(embeddings_test):
            # Encode
            tensor = self.encode(emb)
            
            # Decode
            emb_reconstructed = self.decode(tensor)
            
            # Similaridad
            sim = cosine_similarity(
                emb.reshape(1, -1),
                emb_reconstructed.reshape(1, -1)
            )[0][0]
            similarities.append(sim)
            
            # Contar NULLs
            nulls = sum(
                1 for vec in tensor.nivel_27
                for bit in vec
                if bit is None
            )
            null_counts.append(nulls)
            
            if i < 3:  # Mostrar primeras 3
                print(f"  Muestra {i}: sim={sim:.3f}, NULLs={nulls}")
        
        avg_sim = np.mean(similarities)
        avg_nulls = np.mean(null_counts)
        
        print(f"\n📊 Resultados:")
        print(f"  Similaridad promedio: {avg_sim:.3f}")
        print(f"  NULLs promedio: {avg_nulls:.1f} / 81")
        print(f"  Min/Max similaridad: {min(similarities):.3f} / {max(similarities):.3f}")
        
        # Validación de umbral
        threshold = 0.85
        passed = avg_sim >= threshold
        print(f"\n{'✅' if passed else '❌'} Umbral {threshold}: {'PASS' if passed else 'FAIL'}")
        
        return EncodingMetrics(
            reconstruction_similarity=avg_sim,
            nulls_count=int(avg_nulls),
            cluster_coherence=1.0 - float(avg_nulls) / 81.0,
            transcender_score=None
        )


# Helper: Generar embeddings sintéticos para testing
def generate_synthetic_embeddings(
    n_samples: int = 100,
    dim: int = 768,
    n_clusters_true: int = 5
) -> np.ndarray:
    """
    Genera embeddings sintéticos con estructura de clusters.
    Útil para validación inicial sin necesidad de LLM.
    """
    np.random.seed(42)
    
    embeddings = []
    for _ in range(n_samples):
        # Seleccionar cluster aleatorio
        cluster_id = np.random.randint(0, n_clusters_true)
        
        # Centroide del cluster
        centroid = np.random.randn(dim) * 2
        
        # Punto alrededor del centroide
        point = centroid + np.random.randn(dim) * 0.5
        
        embeddings.append(point)
    
    return np.array(embeddings)


if __name__ == "__main__":
    print("=" * 70)
    print("FFE ENCODER v0.2 - Validación Trigate")
    print("=" * 70 + "\n")
    
    # 1. Generar datos sintéticos
    print("📦 Generando embeddings sintéticos...")
    embeddings_train = generate_synthetic_embeddings(n_samples=500, dim=768)
    embeddings_test = generate_synthetic_embeddings(n_samples=50, dim=768)
    print(f"  Train: {embeddings_train.shape}")
    print(f"  Test: {embeddings_test.shape}\n")
    
    # 2. Entrenar encoder
    encoder = FFEEncoder(
        embedding_dim=768,
        n_dims_pca=81,
        quantization_mode="trigate"
    )
    encoder.fit(embeddings_train)
    
    # 3. Validar
    metrics = encoder.validate(embeddings_test)
    
    # 4. Ejemplo de encoding
    print("\n" + "=" * 70)
    print("Ejemplo de Encoding:")
    print("=" * 70)
    sample_emb = embeddings_test[0]
    tensor = encoder.encode(sample_emb)
    print(f"\nEmbedding shape: {sample_emb.shape}")
    print(f"Tensor resultado:")
    print(f"  nivel_3 (3 vectores): {tensor.nivel_3}")
    print(f"  nivel_9 (9 vectores): {len(tensor.nivel_9)} vectores")
    print(f"  nivel_27 (27 vectores): {len(tensor.nivel_27)} vectores")
    
    print("\n" + "=" * 70)
    print("✅ Validación completada")
    print("=" * 70)
