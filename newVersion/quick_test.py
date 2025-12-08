"""
Quick Test - Validar Transcender Real en Pipeline
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aurora_pipeline_complete import AuroraPipeline

print("🧪 TEST RÁPIDO: Transcender Real integrado\n")

# Crear pipeline
pipeline = AuroraPipeline(demo_mode=True)

# Texto de prueba
texto = """
La inteligencia artificial transforma el mundo.
Los sistemas aprenden de datos masivos.
El futuro es incierto pero prometedor.
"""

# Procesar
print("\n📝 Procesando texto...")
result = pipeline.process_text_long(texto, space_id="quick_test")

# Verificar
print("\n✅ Verificación:")
if result['transcensions']:
    print(f"   ✓ Transcender ACTIVO: {len(result['transcensions'])} síntesis generadas")
    for i, trans in enumerate(result['transcensions'][:3]):
        print(f"     Síntesis {i+1}: C_meta={trans['C_meta']:.3f}, reconstruction={trans['reconstruction_ok']}")
else:
    print("   ⚠️ Transcender no generó síntesis")

print(f"\n✅ Test completado!")
print(f"   Tensores: {len(result['sequence'].tensors)}")
print(f"   Arquetipos: {result['stats']['total_archetypes']}")
