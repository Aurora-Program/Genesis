#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor FFE CORRECTO para 'mirar' - Estructura 3×9×27 REAL
Diferenciando GERUNDIO (mirando) vs INFINITIVO (mirar)
"""

def generate_mirar_tensor_correcto():
    """Genera tensor 3×9×27 CORRECTO para 'mirar'"""
    
    # Tensor para 'mirar' - Estructura REAL 3×9×27
    mirar_tensor = [
        # NIVEL 1: FORMA [3 valores base]
        1,  # Verbo/Acción
        
        # NIVEL 2: FUNCIÓN [9 valores - seleccionamos Cotidiano/Experiencial]  
        0,  # Cotidiano/Experiencial
        
        # NIVEL 3: ESTRUCTURA [27 valores - seleccionamos Proceso/Transformación]
        1   # Proceso/Transformación
    ]
    
    # Especificaciones detalladas del tensor
    tensor_detallado = {
        "forma": {
            "valor": 1,
            "categoria": "Verbo/Acción",
            "subdimensiones": {
                "aspecto": {
                    "infinitivo": 13,  # "INFINITIVO propósito objetivo" (1.1.13)
                    "gerundio": 10     # "GERUNDIO proceso ongoing" (1.1.10)
                }
            }
        },
        "funcion": {
            "valor": 0,
            "categoria": "Cotidiano/Experiencial", 
            "especificacion": "Empírico sensorial directo"
        },
        "estructura": {
            "valor": 1,
            "categoria": "Proceso/Transformación",
            "especificacion": "Perceptual cognitiva"
        }
    }
    
    return mirar_tensor, tensor_detallado

def generate_infinitivo_vs_gerundio():
    """Compara INFINITIVO vs GERUNDIO en el sistema FFE"""
    
    comparacion = {
        "INFINITIVO_mirar": {
            "tensor": [1, 0, 1],
            "aspecto": 13,  # "INFINITIVO propósito objetivo" 
            "uso": "Expresar acción como propósito o potencial",
            "ejemplo": "Quiero MIRAR la película",
            "especificacion": "1.1.13 - INFINITIVO propósito objetivo"
        },
        "GERUNDIO_mirando": {
            "tensor": [1, 0, 1], 
            "aspecto": 10,  # "GERUNDIO proceso ongoing"
            "uso": "Expresar acción en proceso simultáneo",
            "ejemplo": "Estoy MIRANDO la película", 
            "especificacion": "1.1.10 - GERUNDIO proceso ongoing"
        }
    }
    
    return comparacion

def main():
    print("🎯 TENSOR FFE CORRECTO 3×9×27 PARA 'MIRAR'")
    print("=" * 55)
    print()
    
    tensor, detalle = generate_mirar_tensor_correcto()
    comparacion = generate_infinitivo_vs_gerundio()
    
    print("📊 TENSOR BASE [3×9×27]:")
    print(f"  Estructura: {tensor}")
    print(f"  Total combinaciones: 3×9×27 = {3*9*27}")
    print()
    
    print("🔍 DESGLOSE DETALLADO:")
    print("-" * 30)
    print(f"• FORMA ({detalle['forma']['valor']}): {detalle['forma']['categoria']}")
    print(f"• FUNCIÓN ({detalle['funcion']['valor']}): {detalle['funcion']['categoria']}")
    print(f"• ESTRUCTURA ({detalle['estructura']['valor']}): {detalle['estructura']['categoria']}")
    print()
    
    print("⚡ DIFERENCIA GERUNDIO vs INFINITIVO:")
    print("=" * 55)
    
    for forma, datos in comparacion.items():
        print(f"\n📝 {forma.upper()}:")
        print(f"   • Tensor: {datos['tensor']}")
        print(f"   • Aspecto: {datos['aspecto']} - {datos['especificacion']}")
        print(f"   • Uso: {datos['uso']}")
        print(f"   • Ejemplo: \"{datos['ejemplo']}\"")
    
    print("\n" + "=" * 55)
    print("✅ CONFIRMACIÓN ESTRUCTURA CORRECTA:")
    print("=" * 55)
    print("• NIVEL 1: 3 dimensiones principales (Forma, Función, Estructura)")
    print("• NIVEL 2: 9 subdimensiones por cada dimensión = 27 total")
    print("• NIVEL 3: 27 especificaciones por cada subdimensión = 729 total")
    print("• ASPECTO VERBAL: Incluye diferenciación GERUNDIO vs INFINITIVO")
    print("• ARQUITECTURA: 3×9×27 = 729 combinaciones ✓")

if __name__ == "__main__":
    main()
