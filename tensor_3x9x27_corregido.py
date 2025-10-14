#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor 3×9×27 Corregido - Sistema FFE Aurora
Generador de tensor con arquitectura verdadera 3×9×27
Basado en la documentación corregida del catálogo FFE
"""

import yaml
import os

def load_ffe_catalog():
    """Carga el catálogo FFE corregido desde el archivo YAML"""
    catalog_path = os.path.join(os.path.dirname(__file__), 'catalogs', 'ffe_catalog.yaml')
    with open(catalog_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_3x9x27_tensor():
    """
    Genera un tensor 3×9×27 según la arquitectura fractal correcta:
    
    ARQUITECTURA FRACTAL:
    - NIVEL 1: 3 dimensiones principales (valores 0-7)
    - NIVEL 2: 9 subdimensiones (3×3 tríos fractal, valores 0-7)  
    - NIVEL 3: 27 especificaciones (9×3 tríos fractal, valores 0-7)
    
    FORMATO:
    [
      [a, b, c],                               # Capa 1: ejes principales
      [ [x1,x2,x3], [y1,y2,y3], [z1,z2,z3] ],  # Capa 2: fractalización 3×3
      [
        [ [a1,a2,a3], [a4,a5,a6], [a7,a8,a9] ],  # Capa 3: subfractales 9×3
        [ [b1,b2,b3], [b4,b5,b6], [b7,b8,b9] ],
        [ [c1,c2,c3], [c4,c5,c6], [c7,c8,c9] ]
      ]
    ]
    """
    
    # Ejemplo: palabra "FUEGO"
    tensor_fuego = [
        # CAPA 1: Ejes principales (3 dimensiones, valores 0-7)
        [0, 0, 0],  # [forma, funcion, estructura] - Sustantivo concreto elemental
        
        # CAPA 2: Fractalización 3×3 (9 subdimensiones, valores 0-7)
        [
            [0, 1, 2],  # FORMA: elementos_basicos (tipo, propiedades, función)
            [0, 1, 2],  # FUNCIÓN: empírico (experiencia, método, formalización)
            [0, 1, 2]   # ESTRUCTURA: componentes (integración, transformación, complejidad)
        ],
        
        # CAPA 3: Subfractales 9×3 (27 especificaciones, valores 0-7)
        [
            # FORMA subfractales (9 especificaciones en 3 tríos)
            [ [0, 1, 2], [3, 4, 5], [6, 7, 0] ],  # elementos_tipo, elementos_propiedades, elementos_funcion
            
            # FUNCIÓN subfractales (9 especificaciones en 3 tríos)  
            [ [1, 2, 3], [4, 5, 6], [7, 0, 1] ],  # empírico_experiencia, empírico_método, empírico_formalización
            
            # ESTRUCTURA subfractales (9 especificaciones en 3 tríos)
            [ [2, 3, 4], [5, 6, 7], [0, 1, 2] ]   # componentes_integración, componentes_transformación, componentes_complejidad
        ]
    ]
    
    return tensor_fuego

def validate_tensor_architecture(tensor):
    """Valida que el tensor cumpla la arquitectura 3×9×27"""
    
    print("🔍 VALIDACIÓN DE ARQUITECTURA 3×9×27")
    print("=" * 50)
    
    # Validar CAPA 1: 3 dimensiones
    capa1 = tensor[0]
    print(f"✅ CAPA 1: {len(capa1)} dimensiones principales")
    for i, val in enumerate(capa1):
        if 0 <= val <= 7:
            print(f"   Dimensión {i}: {val} (válido 0-7)")
        else:
            print(f"   ❌ Dimensión {i}: {val} (fuera de rango 0-7)")
    
    # Validar CAPA 2: 9 subdimensiones (3×3)
    capa2 = tensor[1]
    print(f"\n✅ CAPA 2: {len(capa2)} grupos de subdimensiones")
    total_subdim = 0
    for i, grupo in enumerate(capa2):
        print(f"   Grupo {i}: {len(grupo)} subdimensiones -> {grupo}")
        total_subdim += len(grupo)
    print(f"   Total subdimensiones: {total_subdim} (esperado: 9)")
    
    # Validar CAPA 3: 27 especificaciones (9×3)
    capa3 = tensor[2]
    print(f"\n✅ CAPA 3: {len(capa3)} grupos de especificaciones")
    total_specs = 0
    for i, grupo in enumerate(capa3):
        print(f"   Grupo {i}: {len(grupo)} tríos")
        for j, trio in enumerate(grupo):
            print(f"     Trío {j}: {len(trio)} valores -> {trio}")
            total_specs += len(trio)
    print(f"   Total especificaciones: {total_specs} (esperado: 27)")
    
    # Validar rangos de valores
    print(f"\n🎯 VALIDACIÓN DE RANGOS (todos los valores deben estar en 0-7)")
    all_valid = True
    
    # Validar todos los valores en el tensor
    def validate_range(valores, nivel):
        nonlocal all_valid
        for val in valores:
            if isinstance(val, list):
                validate_range(val, nivel)
            else:
                if not (0 <= val <= 7):
                    print(f"   ❌ Valor {val} fuera de rango en {nivel}")
                    all_valid = False
    
    validate_range(tensor, "tensor completo")
    
    if all_valid:
        print("   ✅ Todos los valores están en el rango correcto (0-7)")
    
    return all_valid

def analyze_tensor_meaning(tensor, catalog):
    """Analiza el significado del tensor usando el catálogo"""
    
    print("\n🎯 ANÁLISIS SEMÁNTICO DEL TENSOR")
    print("=" * 50)
    
    # CAPA 1: Dimensiones principales
    forma, funcion, estructura = tensor[0]
    print(f"\n📝 DIMENSIONES PRINCIPALES:")
    print(f"   • FORMA {forma}: {catalog['forma']['values'][forma]}")
    print(f"   • FUNCIÓN {funcion}: {catalog['funcion']['values'][funcion]}")
    print(f"   • ESTRUCTURA {estructura}: {catalog['estructura']['values'][estructura]}")
    
    # CAPA 2: Subdimensiones
    print(f"\n🔧 SUBDIMENSIONES FRACTAL:")
    subdim_names = [
        ["elementos_basicos", "modificadores", "determinantes"],
        ["empirico", "creativo", "relacional"], 
        ["componentes", "redes", "patrones"]
    ]
    
    for i, grupo in enumerate(tensor[1]):
        dim_name = ["FORMA", "FUNCIÓN", "ESTRUCTURA"][i]
        print(f"   • {dim_name} fractal: {grupo}")
        for j, val in enumerate(grupo):
            subdim_name = subdim_names[i][j]
            print(f"     - {subdim_name}: {val}")
    
    # CAPA 3: Especificaciones
    print(f"\n⚡ ESPECIFICACIONES FINALES:")
    spec_names = [
        [["tipo", "propiedades", "función"], ["alcance", "relación", "modalidad"], ["determinación", "especificidad", "expresión"]],
        [["experiencia", "método", "formalización"], ["modalidad", "profundidad", "temporal"], ["estructura", "trascendente", "integración"]],
        [["integración", "transformación", "complejidad"], ["topología", "jerarquía", "flujo"], ["regularidad", "emergencia", "estabilidad"]]
    ]
    
    for i, grupo in enumerate(tensor[2]):
        dim_name = ["FORMA", "FUNCIÓN", "ESTRUCTURA"][i]
        print(f"   • {dim_name} especificaciones:")
        for j, trio in enumerate(grupo):
            print(f"     Trío {j}: {trio} -> {spec_names[i][j]}")

def demonstrate_tensor_generation():
    """Demuestra la generación y análisis de tensor 3×9×27"""
    
    print("🚀 DEMOSTRACIÓN TENSOR 3×9×27 CORREGIDO")
    print("=" * 60)
    
    try:
        # Cargar catálogo corregido
        catalog = load_ffe_catalog()
        print("✅ Catálogo FFE corregido cargado")
        
        # Generar tensor de ejemplo
        tensor = generate_3x9x27_tensor()
        print("✅ Tensor 3×9×27 generado")
        
        # Mostrar estructura del tensor
        print(f"\n📊 ESTRUCTURA DEL TENSOR:")
        print(f"Tipo: {type(tensor)}")
        print(f"Forma: {len(tensor)} capas")
        print(f"Capa 1: {len(tensor[0])} dimensiones")
        print(f"Capa 2: {len(tensor[1])} grupos × {len(tensor[1][0])} subdimensiones")
        print(f"Capa 3: {len(tensor[2])} grupos × {len(tensor[2][0])} tríos × {len(tensor[2][0][0])} especificaciones")
        
        # Mostrar tensor completo
        print(f"\n📋 TENSOR COMPLETO:")
        print("```")
        for i, capa in enumerate(tensor):
            print(f"Capa {i+1}: {capa}")
        print("```")
        
        # Validar arquitectura
        is_valid = validate_tensor_architecture(tensor)
        
        # Analizar significado
        if is_valid:
            analyze_tensor_meaning(tensor, catalog)
        
        # Mostrar total de combinaciones
        total_combinations = 8**27  # 8 valores posibles (0-7) ^ 27 especificaciones
        print(f"\n🌟 CAPACIDAD TOTAL DEL SISTEMA:")
        print(f"   Combinaciones posibles: {total_combinations:,}")
        print(f"   Arquitectura: 3×9×27 = {3*9*27} especificaciones")
        print(f"   Rango de valores: 0-7 (8 opciones por especificación)")
        
        print(f"\n🎊 ¡Tensor 3×9×27 generado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo ffe_catalog.yaml corregido existe")

if __name__ == "__main__":
    demonstrate_tensor_generation()
