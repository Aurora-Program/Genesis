#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor FFE para 'mirar' - Verbo de percepción visual
"""

def generate_mirar_tensor():
    """Genera tensor específico para 'mirar'"""
    
    # Tensor para 'mirar' - Verbo de percepción visual activa
    mirar_tensor = [
        # NIVEL 1: FORMA [0-8] - VERBO
        [
            [1, 0, 0],  # verbo -> tiempo_verbal -> presente actual
            [1, 1, 2],  # verbo -> aspecto -> imperfectivo progresivo
            [1, 2, 0],  # verbo -> modo -> indicativo real
            [1, 3, 0],  # verbo -> voz -> activa directa
            [1, 4, 0],  # verbo -> transitividad -> transitivo directo
            [1, 5, 5],  # verbo -> persona -> tercera singular
            [1, 6, 0],  # verbo -> numero_verbal -> singular individual
            [1, 7, 0],  # verbo -> polaridad -> afirmativo positivo
            [1, 8, 2]   # verbo -> valencia_argumental -> bivalente [sujeto + objeto]
        ],
        
        # NIVEL 2: FUNCIÓN [0-8] - COTIDIANO/EXPERIENCIAL
        [
            [0, 0, 0],  # cotidiano -> origen_experiencial -> empírico sensorial directo
            [0, 1, 1],  # cotidiano -> grado_abstraccion -> bajo concreto
            [0, 2, 6],  # cotidiano -> dominio_aplicacion -> sensorial perceptivo
            [0, 3, 0],  # cotidiano -> nivel_formalidad -> informal cotidiano
            [0, 4, 0],  # cotidiano -> contexto_social -> individual personal
            [0, 5, 0],  # cotidiano -> temporalidad_vivencial -> inmediato presente
            [0, 6, 0],  # cotidiano -> modalidad_sensorial -> visual directo
            [0, 7, 0],  # cotidiano -> transmision_cultural -> innato natural
            [0, 8, 7]   # cotidiano -> accesibilidad_practica -> universal accesible
        ],
        
        # NIVEL 3: ESTRUCTURA [0-7] - PROCESO/TRANSFORMACIÓN
        [
            [1, 0, 1],  # proceso -> tipo_transformacion -> perceptual cognitiva
            [1, 1, 4],  # proceso -> duracion_temporal -> puntual instantáneo
            [1, 2, 0],  # proceso -> alcance_sistemico -> local individual
            [1, 3, 2],  # proceso -> direccionalidad -> sujeto hacia objeto
            [1, 4, 0],  # proceso -> reversibilidad -> reversible repetible
            [1, 5, 0],  # proceso -> energia_requerida -> mínima natural
            [1, 6, 1],  # proceso -> complejidad_procesual -> simple directo
            [1, 7, 2],  # proceso -> productos_emergentes -> información visual
            [1, 8, 1]   # proceso -> recursividad_procesual -> puede repetirse
        ]
    ]
    
    return mirar_tensor

def interpret_mirar_tensor():
    """Interpreta el tensor de mirar"""
    
    interpretacion = {
        "forma": {
            "categoria": "Verbo de acción perceptiva",
            "tiempo": "Presente actual",
            "aspecto": "Imperfectivo progresivo", 
            "modo": "Indicativo real",
            "voz": "Activa directa",
            "transitividad": "Transitivo directo",
            "valencia": "Bivalente (sujeto + objeto visual)"
        },
        "funcion": {
            "dominio": "Cotidiano/Experiencial",
            "origen": "Empírico sensorial directo",
            "modalidad": "Visual directo",
            "accesibilidad": "Universal accesible",
            "formalidad": "Informal cotidiano"
        },
        "estructura": {
            "tipo": "Proceso de transformación perceptual",
            "duracion": "Puntual instantáneo",
            "direccionalidad": "Sujeto hacia objeto",
            "complejidad": "Simple directo",
            "producto": "Información visual",
            "recursividad": "Repetible"
        }
    }
    
    return interpretacion

def main():
    print("🎯 TENSOR FFE PARA 'MIRAR'")
    print("=" * 40)
    print()
    
    tensor = generate_mirar_tensor()
    interpretacion = interpret_mirar_tensor()
    
    print("📊 TENSOR ESTRUCTURA 3×9×8:")
    for i, nivel in enumerate(tensor):
        print(f"\nNIVEL {i+1}:")
        for j, componente in enumerate(nivel):
            print(f"  {componente}")
    
    print("\n" + "=" * 40)
    print("🔍 INTERPRETACIÓN SEMÁNTICA:")
    print("=" * 40)
    
    print(f"\n👁️  FORMA (Verbo):")
    for key, value in interpretacion["forma"].items():
        print(f"  • {key.capitalize()}: {value}")
    
    print(f"\n🧠 FUNCIÓN (Cotidiano/Experiencial):")
    for key, value in interpretacion["funcion"].items():
        print(f"  • {key.capitalize()}: {value}")
    
    print(f"\n⚙️  ESTRUCTURA (Proceso):")
    for key, value in interpretacion["estructura"].items():
        print(f"  • {key.capitalize()}: {value}")
    
    print("\n" + "=" * 40)
    print("✨ RESUMEN CONCEPTUAL:")
    print("=" * 40)
    print("'MIRAR' es un verbo transitivo de percepción visual activa")
    print("que representa un proceso cognitivo simple y directo de")
    print("captación sensorial inmediata, universalmente accesible")
    print("y repetible, que transforma información visual del")
    print("entorno en experiencia consciente.")

if __name__ == "__main__":
    main()
