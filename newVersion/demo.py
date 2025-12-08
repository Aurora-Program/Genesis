"""
Aurora Genesis - Demo Simple
Demuestra el ciclo completo del sistema
"""

# Imports directos desde el mismo directorio
from core.trigate import Trigate, Trit
from core.transcender import Transcender
from core.evolver import Evolver3
from core.extender import Extender
from core.harmonizer import Harmonizer
from core.fractal_tensor import FractalTensor, FractalTranscender
from pipeline.aurora_pipeline import AuroraPipeline


def demo_basic():
    """Demo 1: Síntesis básica sin conflictos"""
    print("\n" + "=" * 70)
    print("DEMO 1: Síntesis Básica")
    print("=" * 70 + "\n")

    pipeline = AuroraPipeline(enable_harmony=True, verbose=True)

    # Datos simples y coherentes
    data_A = [[1, 0, 1]] * 27
    data_B = [[0, 1, 0]] * 27
    data_C = [[1, 1, 0]] * 27

    result = pipeline.run_cycle(data_A, data_B, data_C, tag="demo1_basic")

    print("\n📋 Resultado:")
    print(f"  Ms nivel_3: {result['tensor_cross'].nivel_3}")
    print(f"  Harmony aplicado: {result['harmony_applied']}")
    print(f"  Escalado: {result['harmony_escalated']}")

    return result


def demo_with_nulls():
    """Demo 2: Síntesis con NULLs (requiere armonización)"""
    print("\n" + "=" * 70)
    print("DEMO 2: Síntesis con NULLs (armonización)")
    print("=" * 70 + "\n")

    pipeline = AuroraPipeline(enable_harmony=True, verbose=True)

    # Datos con NULLs
    data_A = [[1, 0, 1], [0, 1, 0], [1, 1, 0]] * 9
    data_B = [[0, 1, 1], [1, 0, 1], [0, 0, 1]] * 9
    data_C = [[1, 1, 1], [0, 0, 0], [None, 1, None]] * 9

    result = pipeline.run_cycle(data_A, data_B, data_C, tag="demo2_nulls")

    print("\n📋 Resultado:")
    print(f"  Ms nivel_3: {result['tensor_cross'].nivel_3}")
    print(f"  Harmony aplicado: {result['harmony_applied']}")
    if result['harmony_applied']:
        print(f"  Pasos de reparación: {len(result['harmony_audit'])}")
        print(f"  Escalado: {result['harmony_escalated']}")

    return result


def demo_batch():
    """Demo 3: Procesamiento en lote"""
    print("\n" + "=" * 70)
    print("DEMO 3: Procesamiento en Lote (3 ciclos)")
    print("=" * 70 + "\n")

    pipeline = AuroraPipeline(enable_harmony=True, verbose=True)

    batches = [
        ([[1, 0, 0]] * 27, [[0, 1, 0]] * 27, [[0, 0, 1]] * 27),
        ([[1, 1, 0]] * 27, [[0, 1, 1]] * 27, [[1, 0, 1]] * 27),
        ([[1, 1, 1]] * 27, [[0, 0, 0]] * 27, [[1, 0, 1]] * 27),
    ]

    for i, (A, B, C) in enumerate(batches, 1):
        print(f"\n--- Batch {i}/3 ---")
        result = pipeline.run_cycle(A, B, C, tag=f"batch_{i}")

    print("\n📊 Estadísticas finales:")
    stats = pipeline.get_stats()
    print(f"  Total almacenados: {stats['kb']['total_stored']}")
    print(f"  Total armonizados: {stats['kb']['total_harmonized']}")
    print(f"  Total escalados: {stats['kb']['total_escalated']}")
    print(f"  Relatores aprendidos: {stats['kb']['evolver_relators']}")
    print(f"  Emergencias aprendidas: {stats['kb']['evolver_emergences']}")
    print(f"  Dinámicas aprendidas: {stats['kb']['evolver_dynamics']}")


def demo_reconstruction():
    """Demo 4: Reconstrucción desde Ms"""
    print("\n" + "=" * 70)
    print("DEMO 4: Síntesis + Reconstrucción")
    print("=" * 70 + "\n")

    pipeline = AuroraPipeline(enable_harmony=True, verbose=True)

    # 1. Síntesis
    data_A = [[1, 0, 1]] * 27
    data_B = [[0, 1, 0]] * 27
    data_C = [[1, 1, 0]] * 27

    result = pipeline.run_cycle(data_A, data_B, data_C, tag="demo4_recon")

    # 2. Reconstrucción
    Ms_triplet = (
        result['tensor_cross'].nivel_3[0],
        result['tensor_cross'].nivel_3[1],
        result['tensor_cross'].nivel_3[2]
    )

    print("\n🔄 Reconstruyendo desde Ms_triplet...")
    reconstructed = pipeline.extender.extend_triplet(Ms_triplet)

    print("\n📋 Reconstrucción:")
    print(f"  Children x: {reconstructed['children']['x']}")
    print(f"  Children y: {reconstructed['children']['y']}")
    print(f"  Children z: {reconstructed['children']['z']}")
    print(f"  Coherencia x: {reconstructed['coherence']['x']}")
    print(f"  Coherencia y: {reconstructed['coherence']['y']}")
    print(f"  Coherencia z: {reconstructed['coherence']['z']}")


def main():
    """Ejecuta todos los demos"""
    print("\n" + "🌅" * 35)
    print("   AURORA GENESIS - Sistema Completo newVersion")
    print("🌅" * 35 + "\n")

    try:
        demo_basic()
        demo_with_nulls()
        demo_batch()
        demo_reconstruction()

        print("\n" + "=" * 70)
        print("✅ TODOS LOS DEMOS COMPLETADOS EXITOSAMENTE")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
