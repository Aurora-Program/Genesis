"""
🚀 Setup & Verificación - Proyecto Genesis
Script para verificar instalación y ejecutar diagnósticos completos
"""

import sys
import subprocess
from pathlib import Path
import importlib


def print_header(text):
    """Imprime encabezado con formato"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")


def check_python_version():
    """Verifica versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    print(f"   Versión: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Requiere Python 3.8+")
        return False
    else:
        print("   ✅ Versión compatible")
        return True


def check_dependencies():
    """Verifica dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required = {
        "numpy": "numpy",
        "yaml": "pyyaml",
        "pytest": "pytest",
    }
    
    missing = []
    for module, package in required.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (faltante)")
            missing.append(package)
    
    if missing:
        print(f"\n   Para instalar: pip install {' '.join(missing)}")
        return False
    return True


def check_file_structure():
    """Verifica estructura de archivos"""
    print("\n📁 Verificando estructura de archivos...")
    
    required_files = [
        "aurora_prototype.py",
        "aurora_pipeline.py",
        "mcp_servers/ffe_store.py",
        "catalogs/ffe_catalog.yaml",
        "tests/test_full_pipeline.py",
        "README.md",
        "requirements.txt",
    ]
    
    missing = []
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (faltante)")
            missing.append(file)
    
    return len(missing) == 0


def run_tests():
    """Ejecuta suite de tests"""
    print("\n🧪 Ejecutando tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_full_pipeline.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parsear salida
        output = result.stdout
        if "passed" in output:
            # Extraer número de tests pasados
            import re
            match = re.search(r'(\d+) passed', output)
            if match:
                passed = int(match.group(1))
                print(f"   ✅ {passed} tests pasados")
                
                # Verificar si hay fallos
                fail_match = re.search(r'(\d+) failed', output)
                if fail_match:
                    failed = int(fail_match.group(1))
                    print(f"   ❌ {failed} tests fallidos")
                    return False
                return True
        else:
            print("   ❌ Error ejecutando tests")
            print(f"   Output: {output[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ Timeout ejecutando tests")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def run_demo():
    """Ejecuta demo básica"""
    print("\n🎬 Ejecutando demo básica...")
    
    try:
        from aurora_prototype import Trigate, Transcender, FractalTensor
        
        # Test Trigate
        tg = Trigate()
        result = tg.infer([0, 1, 1], [1, 0, 1], [1, 0, 1])
        assert result == [1, 0, 0], "Trigate infer falló"
        print("   ✅ Trigate operativo")
        
        # Test Transcender
        tc = Transcender()
        synthesis = tc.synthesize([0, 1, 0], [1, 0, 1], [0, 1, 1])
        assert "Ms" in synthesis, "Transcender falló"
        print("   ✅ Transcender operativo")
        
        # Test FractalTensor
        tensor = FractalTensor([1, 2, 3])
        coherent, _ = tensor.check_ethical_coherence(tc)
        assert coherent is True, "FractalTensor coherence check falló"
        print("   ✅ FractalTensor operativo")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_catalog():
    """Verifica catálogo FFE"""
    print("\n📖 Verificando catálogo FFE...")
    
    try:
        import yaml
        with open("catalogs/ffe_catalog.yaml", "r", encoding="utf-8") as f:
            catalog = yaml.safe_load(f)
        
        # Verificar estructura
        assert "axes" in catalog, "Catálogo sin campo 'axes'"
        assert len(catalog["axes"]) == 3, f"Esperado 3 ejes, encontrado {len(catalog['axes'])}"
        
        total_subdims = sum(len(axis["subdimensions"]) for axis in catalog["axes"])
        assert total_subdims == 9, f"Esperado 9 subdimensiones, encontrado {total_subdims}"
        
        total_specs = sum(
            len(subdim["specs"])
            for axis in catalog["axes"]
            for subdim in axis["subdimensions"]
        )
        assert total_specs == 27, f"Esperado 27 especificaciones, encontrado {total_specs}"
        
        print(f"   ✅ Catálogo válido: 3 ejes, 9 subdimensiones, 27 especificaciones")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en catálogo: {e}")
        return False


def generate_report():
    """Genera reporte de verificación"""
    print_header("📊 REPORTE DE VERIFICACIÓN")
    
    checks = {
        "Python 3.8+": check_python_version(),
        "Dependencias": check_dependencies(),
        "Estructura de archivos": check_file_structure(),
        "Catálogo FFE": check_catalog(),
        "Demo básica": run_demo(),
        "Suite de tests": run_tests(),
    }
    
    print("\n" + "="*80)
    print("  RESUMEN")
    print("="*80 + "\n")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
    
    print(f"\n   Total: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n   🎉 ¡INSTALACIÓN COMPLETA Y VERIFICADA!")
        print("\n   Próximos pasos:")
        print("      1. Ejecutar demo completa: python demo_complete.py")
        print("      2. Explorar pipeline: python aurora_pipeline.py")
        print("      3. Ver documentación: docs/documentation.md")
        print("      4. Leer estado del proyecto: PROGRESS.md")
        return True
    else:
        print("\n   ⚠️  Algunas verificaciones fallaron")
        print("\n   Soluciones:")
        if not checks["Dependencias"]:
            print("      • Instalar dependencias: pip install -r requirements.txt")
        if not checks["Estructura de archivos"]:
            print("      • Verificar que todos los archivos estén presentes")
        if not checks["Suite de tests"]:
            print("      • Revisar errores de tests con: pytest tests/ -v")
        return False


def quick_start_guide():
    """Muestra guía de inicio rápido"""
    print_header("🚀 GUÍA DE INICIO RÁPIDO")
    
    print("""
1. INSTALACIÓN
   pip install -r requirements.txt

2. VERIFICACIÓN
   python setup_and_verify.py

3. EJECUTAR DEMO COMPLETA
   python demo_complete.py

4. EJECUTAR PIPELINE
   python aurora_pipeline.py

5. EJECUTAR TESTS
   pytest tests/ -v

6. EXPLORAR CÓDIGO
   • aurora_prototype.py - Componentes básicos (Trigate, Transcender)
   • aurora_pipeline.py - Pipeline completo
   • mcp_servers/ffe_store.py - Knowledge Base
   • catalogs/ffe_catalog.yaml - Catálogo semántico FFE

7. DOCUMENTACIÓN
   • README.md - Visión general
   • PROGRESS.md - Estado del proyecto
   • EXECUTIVE_SUMMARY.md - Resumen ejecutivo
   • docs/documentation.md - Manual técnico completo
   • docs/genesis.md - Manifiesto del proyecto
    """)


def main():
    """Función principal"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                🌌 PROYECTO GENESIS - SETUP & VERIFICACIÓN 🌌                  ║
║                                                                               ║
║                     Aurora Program | Aurora Alliance                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    import argparse
    parser = argparse.ArgumentParser(description="Setup y verificación del Proyecto Genesis")
    parser.add_argument("--quick-start", action="store_true", help="Mostrar guía de inicio rápido")
    parser.add_argument("--skip-tests", action="store_true", help="Saltar ejecución de tests")
    args = parser.parse_args()
    
    if args.quick_start:
        quick_start_guide()
        return
    
    # Ejecutar verificación completa
    success = generate_report()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
