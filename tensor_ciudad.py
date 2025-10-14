#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor FFE para 'ciudad' - Formato limpio
"""

def show_ciudad_tensor():
    """Muestra el tensor de ciudad en formato claro"""
    
    # Tensor para 'ciudad' con estructura 3x9x8
    ciudad_tensor = [
        # NIVEL 1: FORMA [0-8]
        [
            [0, 0, 1],  # sustantivo -> tipo_sustantivo -> concreto geográfico territorial
            [0, 1, 2],  # sustantivo -> genero -> femenino natural biológico  
            [0, 2, 3],  # sustantivo -> numero -> plural múltiple indefinido
            [0, 3, 4],  # sustantivo -> caso -> ablativo separación origen
            [0, 4, 5],  # sustantivo -> animacidad -> inanimado concreto artificial
            [0, 5, 6],  # sustantivo -> contabilidad -> dual contable/masa material
            [0, 6, 7],  # sustantivo -> definitud -> variable contextual definitud
            [0, 7, 0],  # sustantivo -> especificidad -> específico identificable único
            [0, 8, 1]   # sustantivo -> funcion_nominal -> sujeto experiencer perceptor
        ],
        
        # NIVEL 2: FUNCIÓN [0-8] 
        [
            [1, 0, 2],  # cotidiano -> origen_experiencial -> tradicional cultural heredado
            [1, 1, 3],  # cotidiano -> grado_abstraccion -> [valor 3]
            [1, 2, 4],  # cotidiano -> dominio_aplicacion -> [valor 4]
            [1, 3, 5],  # cotidiano -> nivel_formalidad -> [valor 5]
            [1, 4, 6],  # cotidiano -> contexto_social -> [valor 6]
            [1, 5, 7],  # cotidiano -> temporalidad_vivencial -> [valor 7]
            [1, 6, 0],  # cotidiano -> modalidad_sensorial -> [valor 0]
            [1, 7, 1],  # cotidiano -> transmision_cultural -> [valor 1]
            [1, 8, 2]   # cotidiano -> accesibilidad_practica -> [valor 2]
        ],
        
        # NIVEL 3: ESTRUCTURA [0-7] - Con mejoras territoriales
        [
            [2, 0, 4],  # sistema -> complejidad_estructural -> integrado metropolitano
            [2, 1, 5],  # sistema -> organización_territorial -> metropolitana integrada
            [2, 2, 2],  # sistema -> conectividad_geográfica -> integrado regional
            [2, 3, 2],  # sistema -> escala_territorial -> municipal urbano
            [2, 4, 4],  # sistema -> densidad_geográfica -> urbano denso
            [2, 5, 7],  # sistema -> tipología_espacial -> mixto multifuncional
            [2, 6, 7],  # sistema -> morfología_urbana -> policéntrico multinuclear
            [2, 7, 4],  # sistema -> accesibilidad_territorial -> altamente accesible
            [2, 8, 4]   # sistema -> gobernanza_territorial -> participativo democrático
        ]
    ]
    
    return ciudad_tensor

def main():
    tensor = show_ciudad_tensor()
    
    print("TENSOR FFE PARA 'CIUDAD'")
    print("========================")
    print()
    
    for i, nivel in enumerate(tensor):
        print(f"NIVEL {i+1}:")
        for j, componente in enumerate(nivel):
            print(f"  {componente}")
        print()
    
    print("INTERPRETACIÓN:")
    print("• FORMA: Sustantivo concreto geográfico territorial femenino")
    print("• FUNCIÓN: Conocimiento cotidiano tradicional cultural")  
    print("• ESTRUCTURA: Sistema metropolitano integrado policéntrico")

if __name__ == "__main__":
    main()
