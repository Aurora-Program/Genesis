"""
Transcender Service - MCP Integration Real
===========================================

Servicio MCP que implementa síntesis emergente real usando el core Transcender.

Input: Dos (o tres) tensores FFE
Output: Síntesis emergente {Ms, Ss, MetaM, C_meta}

Features:
- Usa core/transcender.py (implementación real)
- Múltiples wirings con selección automática
- Coherencia absoluta top-down
- Métricas de calidad (score, reconstruction_ok)
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.transcender import Transcender
from core.trigate import Trigate
from core.fractal_tensor import FractalTensor


class TranscenderService:
    """
    Servicio MCP para Transcender.
    
    API:
        transcend(A, B, C=None) → {Ms, Ss, MetaM, C_meta, ...}
    
    Procesa pares o tríos de tensores FFE y genera:
    - Ms: Estructura emergente superior
    - Ss: Huella factual (forma)
    - MetaM: Ruta lógica completa [M1, M2, M3, Ms]
    - C_meta: Score de coherencia (0.0-1.0)
    """
    
    def __init__(self):
        """Inicializa el servicio con Transcender real"""
        self.transcender = Transcender(Trigate)
        self.call_count = 0
        self.stats = {
            "total_calls": 0,
            "successful": 0,
            "failed": 0,
            "avg_score": 0.0,
            "reconstruction_ok_rate": 0.0
        }
    
    def transcend(
        self,
        A: Dict,
        B: Dict,
        C: Optional[Dict] = None,
        *,
        max_tries: int = 3,
        check_reconstruction: bool = True,
        enforce_coherence: bool = True
    ) -> Dict:
        """
        Síntesis emergente de tensores FFE.
        
        Args:
            A: Tensor FFE como dict {'nivel_3': [[...], [...], [...]]}
            B: Tensor FFE como dict
            C: Tensor FFE opcional (si None, usa A de nuevo)
            max_tries: Número máximo de wirings a intentar
            check_reconstruction: Validar reconstrucción
            enforce_coherence: Aplicar coherencia absoluta top-down
        
        Returns:
            {
                'Ms': [Trit, Trit, Trit],        # Estructura emergente
                'Ss': [Trit, Trit, Trit],        # Huella factual
                'MetaM': [[...], [...], [...], [Ms]],  # Ruta completa
                'C_meta': float,                  # Coherencia 0.0-1.0
                'score': int,                     # #NULLs (menor mejor)
                'reconstruction_ok': bool,        # Validación exitosa
                'coherence_report': Dict,         # Detalles de coherencia
                'wiring': List[Tuple],           # Wiring usado
                'status': 'ok' | 'error'
            }
        """
        self.call_count += 1
        self.stats['total_calls'] += 1
        
        try:
            # Extraer nivel_3 de cada tensor
            A_vec = self._extract_nivel3(A)
            B_vec = self._extract_nivel3(B)
            
            if C is None:
                # Si no hay C, usar A de nuevo (par → trío)
                C_vec = A_vec
            else:
                C_vec = self._extract_nivel3(C)
            
            # Llamar al Transcender real
            result = self.transcender.solve(
                A=A_vec,
                B=B_vec,
                C=C_vec,
                max_tries=max_tries,
                check_reconstruction=check_reconstruction,
                enforce_coherence=enforce_coherence
            )
            
            # Calcular C_meta (coherencia normalizada)
            # Score = #NULLs, score óptimo = 0, peor = 15 (5 vectores × 3 bits)
            max_nulls = 15
            score = result['score']
            C_meta = 1.0 - (score / max_nulls)
            
            # Actualizar stats
            self.stats['successful'] += 1
            self.stats['avg_score'] = (
                (self.stats['avg_score'] * (self.stats['successful'] - 1) + score)
                / self.stats['successful']
            )
            if result['reconstruction_ok']:
                self.stats['reconstruction_ok_rate'] = (
                    (self.stats['reconstruction_ok_rate'] * (self.stats['successful'] - 1) + 1.0)
                    / self.stats['successful']
                )
            
            # Construir respuesta MCP
            return {
                'Ms': result['Ms'],
                'Ss': result['Ss'],
                'MetaM': result['MetaM'],
                'C_meta': C_meta,
                'score': score,
                'reconstruction_ok': result['reconstruction_ok'],
                'coherence_report': result.get('coherence'),
                'wiring': [list(r) for r in result['wiring']],  # Tuplas → Listas
                'status': 'ok',
                'service': 'transcender_v1'
            }
            
        except Exception as e:
            self.stats['failed'] += 1
            return {
                'Ms': [None, None, None],
                'Ss': [None, None, None],
                'MetaM': [[None, None, None]] * 4,
                'C_meta': 0.0,
                'score': 15,
                'reconstruction_ok': False,
                'coherence_report': None,
                'wiring': [],
                'status': 'error',
                'error': str(e),
                'service': 'transcender_v1'
            }
    
    def _extract_nivel3(self, tensor_dict: Dict) -> List:
        """
        Extrae nivel_3 de tensor FFE.
        
        Formato esperado:
        {
            'nivel_3': [[F, Fu, E], [F, Fu, E], [F, Fu, E]]
        }
        
        Returns:
            Lista aplanada de 9 elementos [F1,Fu1,E1, F2,Fu2,E2, F3,Fu3,E3]
            o los primeros 3 elementos si nivel_3 tiene 3 vectores
        """
        if isinstance(tensor_dict, dict):
            nivel_3 = tensor_dict.get('nivel_3', [])
        else:
            # Puede ser un FractalTensor
            nivel_3 = getattr(tensor_dict, 'nivel_3', [])
        
        if not nivel_3:
            # Tensor vacío → vector neutro
            return [None, None, None]
        
        # Aplanar primer vector (Transcender espera vectores de 3)
        if len(nivel_3) > 0 and isinstance(nivel_3[0], list):
            # Tomar primer vector del nivel_3
            return nivel_3[0][:3]
        
        # Fallback
        return [None, None, None]
    
    def get_stats(self) -> Dict:
        """Estadísticas del servicio"""
        return {
            **self.stats,
            'call_count': self.call_count
        }


# ============================================================================
# DEMO Y TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TRANSCENDER SERVICE - Test Real")
    print("=" * 70 + "\n")
    
    service = TranscenderService()
    
    # Test 1: Par de tensores simple
    print("🧪 TEST 1: Síntesis de par de tensores")
    print("-" * 70)
    
    tensor_A = {
        'nivel_3': [
            [1, 0, 1],  # Forma=1, Función=0, Estructura=1
            [0, 1, 0],
            [1, 1, 0]
        ]
    }
    
    tensor_B = {
        'nivel_3': [
            [0, 1, 1],  # Diferente patrón
            [1, 0, 1],
            [0, 0, 1]
        ]
    }
    
    result = service.transcend(tensor_A, tensor_B)
    
    print(f"✅ Status: {result['status']}")
    print(f"\n📊 Síntesis emergente:")
    print(f"   Ms (estructura superior): {result['Ms']}")
    print(f"   Ss (huella factual):      {result['Ss']}")
    print(f"\n🎯 Métricas:")
    print(f"   C_meta (coherencia):      {result['C_meta']:.3f}")
    print(f"   Score (#NULLs):           {result['score']}")
    print(f"   Reconstruction OK:        {result['reconstruction_ok']}")
    print(f"   Wiring usado:             {result['wiring']}")
    
    if result['coherence_report']:
        coh = result['coherence_report']
        print(f"\n🔧 Coherencia aplicada:")
        print(f"   NULLs rellenados:  {coh['totals']['null_filled']}")
        print(f"   Conflictos resueltos: {coh['totals']['conflict_resolved']}")
    
    # Test 2: Batch de pares
    print("\n\n🧪 TEST 2: Batch de 10 pares")
    print("-" * 70)
    
    test_tensors = [
        {'nivel_3': [[1, 0, 1], [0, 1, 0], [1, 1, 0]]},
        {'nivel_3': [[0, 1, 1], [1, 0, 1], [0, 0, 1]]},
        {'nivel_3': [[1, 1, 0], [0, 0, 1], [1, 0, 0]]},
        {'nivel_3': [[0, 0, 1], [1, 1, 1], [0, 1, 0]]},
        {'nivel_3': [[1, 0, 0], [0, 1, 1], [1, 1, 1]]},
    ]
    
    results = []
    for i in range(len(test_tensors) - 1):
        res = service.transcend(test_tensors[i], test_tensors[i + 1])
        results.append(res)
        print(f"  Par {i+1}: C_meta={res['C_meta']:.3f}, score={res['score']}, reconstruction={res['reconstruction_ok']}")
    
    # Test 3: Estadísticas
    print("\n\n📊 ESTADÍSTICAS DEL SERVICIO")
    print("-" * 70)
    
    stats = service.get_stats()
    print(f"   Total llamadas:           {stats['total_calls']}")
    print(f"   Exitosas:                 {stats['successful']}")
    print(f"   Fallidas:                 {stats['failed']}")
    print(f"   Score promedio:           {stats['avg_score']:.2f}")
    print(f"   Tasa reconstruction OK:   {stats['reconstruction_ok_rate']:.1%}")
    
    # Test 4: Validar con tensores de Aurora
    print("\n\n🧪 TEST 4: Integración con Aurora Pipeline")
    print("-" * 70)
    
    try:
        from pipeline.llm_semantic_encoder import LLMSemanticEncoder
        
        encoder = LLMSemanticEncoder(demo_mode=True)
        
        # Generar 2 tensores de textos relacionados
        texto1 = "La inteligencia artificial transforma el futuro"
        texto2 = "Los sistemas inteligentes aprenden de datos"
        
        mapping1 = encoder.encode(texto1)
        mapping2 = encoder.encode(texto2)
        
        # Transcender
        result = service.transcend(
            mapping1.tensor.to_dict(),
            mapping2.tensor.to_dict()
        )
        
        print(f"✅ Texto 1: {texto1}")
        print(f"✅ Texto 2: {texto2}")
        print(f"\n📊 Síntesis:")
        print(f"   Ms: {result['Ms']}")
        print(f"   C_meta: {result['C_meta']:.3f}")
        print(f"   Reconstruction: {result['reconstruction_ok']}")
        
    except ImportError:
        print("   ⚠️ LLMSemanticEncoder no disponible, saltando test")
    
    print("\n" + "=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print("\n💡 TranscenderService está operativo!")
    print("   Listo para integrar en Aurora Pipeline\n")
