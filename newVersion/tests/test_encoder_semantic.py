import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.ffe_encoder import FFEEncoder

SENTENCES = [
    "El gato duerme en el sofá",
    "Un felino descansa sobre el sillón",
    "El perro corre en el parque",
    "Un can trota por el jardín",
]

def main():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("❌ sentence-transformers no instalado. Ejecuta: pip install sentence-transformers")
        return

    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    print(f"🔄 Cargando modelo: {model_name}")
    model = SentenceTransformer(model_name)
    embeddings = model.encode(SENTENCES)
    print(f"✅ Embeddings generados: shape={embeddings.shape}")

    encoder = FFEEncoder(embedding_dim=embeddings.shape[1], n_dims_pca=81, quantization_mode='trigate')
    encoder.fit(embeddings)

    tensors = [encoder.encode(e) for e in embeddings]

    sim_0_1 = encoder.tensor_similarity(tensors[0], tensors[1])
    sim_0_2 = encoder.tensor_similarity(tensors[0], tensors[2])
    sim_2_3 = encoder.tensor_similarity(tensors[2], tensors[3])

    print("\n📊 Similaridades tensoriales (coseno discreto):")
    print(f"  gato~felino    sim={sim_0_1:.4f}")
    print(f"  gato~perro     sim={sim_0_2:.4f}")
    print(f"  perro~can      sim={sim_2_3:.4f}")

    passed_primary = sim_0_1 > sim_0_2
    passed_secondary = sim_2_3 > sim_0_2

    if passed_primary and passed_secondary:
        print("\n✅ Test semántico PASA: preserva proximidad (felino>perro y can>perro)")
    else:
        print("\n❌ Test semántico FALLA: ajuste de umbrales necesario")
        print("   Sugerencias: percentiles dinámicos, ajuste alpha, armonizador post")

if __name__ == '__main__':
    main()
