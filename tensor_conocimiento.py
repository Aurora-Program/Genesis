#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor FFE para la palabra "CONOCIMIENTO"
Utilizando la arquitectura 3×9×27 corregida del catálogo Aurora
"""

import yaml
import os

def load_ffe_catalog():
    """Carga el catálogo FFE corregido"""
    catalog_path = os.path.join(os.path.dirname(__file__), 'catalogs', 'ffe_catalog.yaml')
    with open(catalog_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_tensor_conocimiento():
    """
    Crea el tensor FFE para la palabra "CONOCIMIENTO"
    
    ANÁLISIS SEMÁNTICO:
    - FORMA: Sustantivo abstracto (0)
    - FUNCIÓN: Filosófico/Abstracto (4) 
    - ESTRUCTURA: Sistema/Organización (2)
    """
    
    # CAPA 1: Dimensiones principales [forma, función, estructura]
    capa1 = [0, 4, 2]  # [Sustantivo, Filosófico, Sistema]
    
    # CAPA 2: Subdimensiones fractal 3×3
    capa2 = [
        # FORMA: elementos_básicos (0, 1, 2)
        [0, 1, 2],  # tipo_elemento, propiedades_inherentes, función_sintáctica
        
        # FUNCIÓN: filosófico se mapea a 'creativo' (1) 
        [1, 1, 2],  # modalidad_expresiva, profundidad_reflexiva, perspectiva_temporal
        
        # ESTRUCTURA: sistema se mapea a 'componentes' (0)
        [2, 1, 2]   # complejidad_organizacional, tipo_transformación, estabilidad
    ]
    
    # CAPA 3: Especificaciones fractal 9×3 (27 valores)
    capa3 = [
        # FORMA especificaciones (9 valores en 3 tríos)
        [
            [0, 0, 0],  # elementos_tipo: sustantivo_concreto, género_gramatical, sujeto_agente
            [1, 1, 1],  # elementos_propiedades: número_morfológico, sintagmal_constituyente
            [2, 2, 2]   # elementos_función: adjetivo_cualidad, caso_funcional, complemento_modificador
        ],
        
        # FUNCIÓN especificaciones (9 valores en 3 tríos)
        [
            [1, 2, 1],  # creativo_modalidad: filosófica_reflexiva, formal_sistemático, intermedia_contextual
            [2, 1, 2],  # creativo_profundidad: profunda_trascendental, intermedia_contextual, futuro_proyectivo
            [1, 2, 2]   # creativo_temporal: pasado_histórico, trascendente_espiritual, integrado_holístico
        ],
        
        # ESTRUCTURA especificaciones (9 valores en 3 tríos)
        [
            [2, 2, 2],  # componentes_integración: sistémico_holístico, evolutivo_emergente, caótico_emergente
            [1, 2, 2],  # componentes_transformación: distribuida_reticular, matricial_multidimensional, multidireccional_turbulento
            [2, 2, 2]   # componentes_complejidad: fractal_autosimilar, emergente_innovador, antifragil_potenciador
        ]
    ]
    
    return [capa1, capa2, capa3]

def analyze_tensor_conocimiento(tensor, catalog):
    """Analiza el tensor de CONOCIMIENTO paso a paso"""
    
    print("🧠 TENSOR FFE PARA 'CONOCIMIENTO'")
    print("=" * 60)
    
    # Mostrar tensor completo
    print("\n📊 TENSOR COMPLETO:")
    print("```")
    for i, capa in enumerate(tensor):
        print(f"Capa {i+1}: {capa}")
    print("```")
    
    # CAPA 1: Análisis dimensional principal
    forma, funcion, estructura = tensor[0]
    print(f"\n📝 CAPA 1 - DIMENSIONES PRINCIPALES:")
    print(f"   • FORMA {forma}: {catalog['forma']['values'][forma]}")
    print(f"   • FUNCIÓN {funcion}: {catalog['funcion']['values'][funcion]}")  
    print(f"   • ESTRUCTURA {estructura}: {catalog['estructura']['values'][estructura]}")
    
    print(f"\n💡 INTERPRETACIÓN CAPA 1:")
    print(f"   'CONOCIMIENTO' es un SUSTANTIVO (forma gramatical)")
    print(f"   con función FILOSÓFICA/ABSTRACTA (dominio conceptual)")
    print(f"   que actúa como SISTEMA/ORGANIZACIÓN (función sistémica)")
    
    # CAPA 2: Análisis subdimensional
    print(f"\n🔧 CAPA 2 - SUBDIMENSIONES FRACTAL:")
    subdim_groups = [
        ["elementos_básicos", "modificadores", "determinantes"],
        ["empírico", "creativo", "relacional"],
        ["componentes", "redes", "patrones"]
    ]
    
    dim_names = ["FORMA", "FUNCIÓN", "ESTRUCTURA"]
    for i, grupo in enumerate(tensor[1]):
        print(f"   • {dim_names[i]} fractal: {grupo}")
        for j, val in enumerate(grupo):
            print(f"     - {subdim_groups[i][j]}: {val}")
    
    print(f"\n💡 INTERPRETACIÓN CAPA 2:")
    print(f"   FORMA: Elemento básico (tipo, propiedades, función sintáctica)")
    print(f"   FUNCIÓN: Creativo-filosófico (modalidad, profundidad, temporalidad)")
    print(f"   ESTRUCTURA: Sistémico complejo (organización, transformación, estabilidad)")
    
    # CAPA 3: Análisis especificaciones finales
    print(f"\n⚡ CAPA 3 - ESPECIFICACIONES FINALES:")
    
    spec_labels = [
        # FORMA
        [["sustantivo_concreto", "género_gramatical", "sujeto_agente"],
         ["número_morfológico", "sintagmal_constituyente", "espacial_locativo"], 
         ["adjetivo_cualidad", "caso_funcional", "complemento_modificador"]],
        
        # FUNCIÓN  
        [["filosófica_reflexiva", "formal_sistemático", "intermedia_contextual"],
         ["profunda_trascendental", "intermedia_contextual", "futuro_proyectivo"],
         ["pasado_histórico", "trascendente_espiritual", "integrado_holístico"]],
        
        # ESTRUCTURA
        [["sistémico_holístico", "evolutivo_emergente", "caótico_emergente"],
         ["distribuida_reticular", "matricial_multidimensional", "multidireccional_turbulento"],
         ["fractal_autosimilar", "emergente_innovador", "antifragil_potenciador"]]
    ]
    
    for i, grupo in enumerate(tensor[2]):
        print(f"   • {dim_names[i]} especificaciones:")
        for j, trio in enumerate(grupo):
            labels = spec_labels[i][j]
            print(f"     Trío {j}: {trio} → {labels}")
    
    print(f"\n💡 INTERPRETACIÓN CAPA 3:")
    print(f"   FORMA: Sustantivo abstracto con función nuclear compleja")
    print(f"   FUNCIÓN: Conocimiento filosófico profundo con proyección temporal")
    print(f"   ESTRUCTURA: Sistema emergente, holístico y antifragil")

def validate_conocimiento_tensor(tensor):
    """Valida que el tensor cumple la arquitectura 3×9×27"""
    
    print(f"\n🔍 VALIDACIÓN ARQUITECTURAL:")
    print("=" * 40)
    
    # Verificar estructura
    errors = []
    
    # Capa 1: debe tener 3 valores (0-7)
    if len(tensor[0]) != 3:
        errors.append(f"Capa 1: {len(tensor[0])} valores (esperado: 3)")
    
    for i, val in enumerate(tensor[0]):
        if not (0 <= val <= 7):
            errors.append(f"Capa 1[{i}]: valor {val} fuera de rango 0-7")
    
    # Capa 2: debe tener 3 grupos de 3 valores cada uno
    if len(tensor[1]) != 3:
        errors.append(f"Capa 2: {len(tensor[1])} grupos (esperado: 3)")
    
    for i, grupo in enumerate(tensor[1]):
        if len(grupo) != 3:
            errors.append(f"Capa 2[{i}]: {len(grupo)} valores (esperado: 3)")
        for j, val in enumerate(grupo):
            if not (0 <= val <= 7):
                errors.append(f"Capa 2[{i}][{j}]: valor {val} fuera de rango 0-7")
    
    # Capa 3: debe tener 3 grupos de 3 tríos de 3 valores cada uno
    if len(tensor[2]) != 3:
        errors.append(f"Capa 3: {len(tensor[2])} grupos (esperado: 3)")
    
    for i, grupo in enumerate(tensor[2]):
        if len(grupo) != 3:
            errors.append(f"Capa 3[{i}]: {len(grupo)} tríos (esperado: 3)")
        for j, trio in enumerate(grupo):
            if len(trio) != 3:
                errors.append(f"Capa 3[{i}][{j}]: {len(trio)} valores (esperado: 3)")
            for k, val in enumerate(trio):
                if not (0 <= val <= 7):
                    errors.append(f"Capa 3[{i}][{j}][{k}]: valor {val} fuera de rango 0-7")
    
    if errors:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ TENSOR VÁLIDO - Cumple arquitectura 3×9×27")
        print("✅ Todos los valores en rango 0-7")
        print("✅ Estructura fractal correcta")
        return True

def generate_conocimiento_report():
    """Genera el reporte completo del tensor CONOCIMIENTO"""
    
    try:
        # Cargar catálogo
        catalog = load_ffe_catalog()
        print("✅ Catálogo FFE cargado")
        
        # Crear tensor
        tensor = create_tensor_conocimiento()
        print("✅ Tensor CONOCIMIENTO creado")
        
        # Validar tensor
        is_valid = validate_conocimiento_tensor(tensor)
        
        if is_valid:
            # Analizar tensor
            analyze_tensor_conocimiento(tensor, catalog)
            
            # Mostrar resumen final
            print(f"\n🎯 RESUMEN FINAL:")
            print("=" * 40)
            print(f"Palabra analizada: CONOCIMIENTO")
            print(f"Arquitectura: 3×9×27 fractal")
            print(f"Dimensiones principales: [0, 4, 2]")
            print(f"Total especificaciones: 27")
            print(f"Valores usados: rango 0-7")
            print(f"Status: ✅ TENSOR VÁLIDO")
            
        return tensor
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    generate_conocimiento_report()
