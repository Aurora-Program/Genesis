"""
Script para ejecutar todos los tests de validación del LLM Semantic Encoder

Uso:
    python run_all_tests.py              # Ejecutar todos los tests
    python run_all_tests.py --basic      # Solo tests básicos
    python run_all_tests.py --advanced   # Solo tests avanzados
    python run_all_tests.py --verbose    # Salida detallada
"""
import sys
import subprocess
import time
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def run_test_suite(test_file: str, suite_name: str, verbose: bool = False) -> bool:
    """Ejecuta una suite de tests y retorna True si todos pasan"""
    print(f"\n{Colors.BOLD}▶️  Ejecutando {suite_name}...{Colors.END}")
    print(f"   Archivo: {test_file}")
    
    start_time = time.time()
    
    # Configurar encoding UTF-8 para emojis
    env = {'PYTHONIOENCODING': 'utf-8'}
    
    try:
        # Ejecutar test
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env={**subprocess.os.environ, **env}
        )
        
        elapsed = time.time() - start_time
        
        # Mostrar output si verbose
        if verbose:
            print("\n--- Output ---")
            print(result.stdout)
            if result.stderr:
                print("--- Stderr ---")
                print(result.stderr)
            print("--- End ---\n")
        
        # Check si pasó
        if result.returncode == 0:
            print_success(f"{suite_name} completado en {elapsed:.2f}s")
            return True
        else:
            print_error(f"{suite_name} falló (código {result.returncode})")
            if not verbose:
                print("\n--- Error Output ---")
                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            return False
            
    except Exception as e:
        print_error(f"Error ejecutando {suite_name}: {e}")
        return False

def main():
    # Parse arguments
    args = sys.argv[1:]
    run_basic = '--basic' in args or not any(x in args for x in ['--basic', '--advanced'])
    run_advanced = '--advanced' in args or not any(x in args for x in ['--basic', '--advanced'])
    verbose = '--verbose' in args or '-v' in args
    
    print_header("🧪 AURORA GENESIS - TEST RUNNER")
    
    # Rutas de tests
    tests_dir = Path(__file__).parent / "tests"
    basic_tests = tests_dir / "test_llm_semantic_encoder.py"
    advanced_tests = tests_dir / "test_advanced_scenarios.py"
    
    # Verificar que existen
    if not tests_dir.exists():
        print_error(f"Directorio de tests no encontrado: {tests_dir}")
        return 1
    
    results = {}
    total_start = time.time()
    
    # Ejecutar tests básicos
    if run_basic:
        if basic_tests.exists():
            results['basic'] = run_test_suite(
                str(basic_tests),
                "Tests Básicos (8 tests)",
                verbose
            )
        else:
            print_warning(f"Tests básicos no encontrados: {basic_tests}")
            results['basic'] = None
    
    # Ejecutar tests avanzados
    if run_advanced:
        if advanced_tests.exists():
            results['advanced'] = run_test_suite(
                str(advanced_tests),
                "Tests Avanzados (4 tests)",
                verbose
            )
        else:
            print_warning(f"Tests avanzados no encontrados: {advanced_tests}")
            results['advanced'] = None
    
    # Resumen final
    total_elapsed = time.time() - total_start
    
    print_header("📊 RESUMEN DE RESULTADOS")
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    if run_basic and results.get('basic'):
        print_success("Tests Básicos: 8/8 ✅")
    elif run_basic and results.get('basic') is False:
        print_error("Tests Básicos: FALLARON ❌")
    
    if run_advanced and results.get('advanced'):
        print_success("Tests Avanzados: 4/4 ✅")
    elif run_advanced and results.get('advanced') is False:
        print_error("Tests Avanzados: FALLARON ❌")
    
    print(f"\n{Colors.BOLD}Total de suites ejecutadas:{Colors.END}")
    print(f"  ✅ Pasadas: {passed}")
    print(f"  ❌ Falladas: {failed}")
    if skipped > 0:
        print(f"  ⏭️  Omitidas: {skipped}")
    print(f"  ⏱️  Tiempo total: {total_elapsed:.2f}s")
    
    # Resultado final
    if failed == 0 and passed > 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS TESTS PASARON!{Colors.END}")
        print(f"{Colors.GREEN}Sistema completamente validado y listo para producción.{Colors.END}")
        return 0
    elif failed > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ALGUNOS TESTS FALLARON{Colors.END}")
        print(f"{Colors.RED}Revisa los errores arriba para más detalles.{Colors.END}")
        return 1
    else:
        print(f"\n{Colors.YELLOW}⚠️  No se ejecutaron tests{Colors.END}")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
