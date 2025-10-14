#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tensor Adivinanza - Sistema FFE 3×9×27 Aurora
Generador de tensor para juego de adivinanza
¿Puedes adivinar qué palabra representa este tensor?
"""

import yaml
import os

def load_ffe_catalog():
    """Carga el catálogo FFE desde el archivo YAML"""
    catalog_path = os.path.join(os.path.dirname(__file__), 'catalogs', 'ffe_catalog.yaml')
    with open(catalog_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_mystery_tensor():
    """
    Genera un tensor misterioso para adivinanza
    
    PISTAS DEL TENSOR:
    - Es algo que todos conocemos
    - Tiene relación con el movimiento y la percepción
    - Es fundamental en la experiencia humana
    - Puede ser tanto literal como metafórico
    """
    
    # Tensor misterioso - ¿Qué palabra será?
    mystery_tensor = [
        [
            # FORMA 0 (Nombre/Sustantivo)
            [2, 1, 0, 0, 0, 4, 0, 0, 0],  # 0.0: tipo_sustantivo = "Abstracto mental conceptual" 
            [4, 4, 4, 4, 4, 4, 4, 4, 4],  # 0.1: genero = "Neutro inherente absoluto"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0.2: numero = "Singular individual único"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0.3: caso = "Nominativo sujeto agente"
            [6, 6, 6, 6, 6, 6, 6, 6, 6],  # 0.4: animacidad = "Inanimado abstracto mental"
            [3, 3, 3, 3, 3, 3, 3, 3, 3],  # 0.5: contabilidad = "Incontable masa homogénea"
            [2, 2, 2, 2, 2, 2, 2, 2, 2],  # 0.6: definitud = "Definido genérico universal"
            [4, 4, 4, 4, 4, 4, 4, 4, 4],  # 0.7: especificidad = "Genérico universal absoluto"
            [0, 0, 0, 0, 0, 0, 0, 0, 0]   # 0.8: funcion_nominal = "Sujeto agente actor"
        ],
        [
            # FORMA 1 (Verbo/Acción) - PISTA: Acción perceptual
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.0: tiempo_verbal = "Presente actual"
            [2, 2, 2, 2, 2, 2, 2, 2, 2],  # 1.1: aspecto = "Imperfectivo progresivo continuo"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.2: modo = "Indicativo real"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.3: voz = "Activa directa"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.4: transitividad = "Transitivo directo"
            [0, 1, 2, 3, 4, 5, 6, 7, 0],  # 1.5: persona = Variable según contexto
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.6: numero_verbal = "Singular individual"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1.7: polaridad = "Afirmativo positivo"
            [0, 0, 0, 0, 0, 0, 0, 0, 0]   # 1.8: valencia_argumental (pendiente)
        ],
        [
            # FORMA 2 (Adjetivo/Calificativo) - PISTA: Cualidad sensorial
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2.0: tipo_adjetivo = "Calificativo descriptivo"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2.1: grado = "Positivo neutro"
            [2, 2, 2, 2, 2, 2, 2, 2, 2],  # 2.2: posicion = "Postnominal descriptivo"
            [7, 7, 7, 7, 7, 7, 7, 7, 7],  # 2.3: concordancia = "Invariable flexión"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2.4: funcion_sintactica = "Modificador directo"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2.5: clase_semantica = "Físico perceptible"
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2.6: derivacion = "Primitivo léxico"
            [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 2.7: intensidad = "Moderada estándar"
            [0, 0, 0, 0, 0, 0, 0, 0, 0]   # 2.8: evaluacion (pendiente)
        ]
    ]
    
    return mystery_tensor

def analyze_tensor_clues(tensor, catalog):
    """Analiza las pistas del tensor misterioso"""
    
    print("🔍 ANÁLISIS DE PISTAS DEL TENSOR MISTERIOSO 🔍")
    print("=" * 60)
    
    # Analizar FORMA 0 (Sustantivo)
    print("\n📝 PISTAS DE LA FORMA (Sustantivo):")
    tipo_sust = tensor[0][0][0]  # 2 = "Abstracto mental conceptual"
    genero = tensor[0][1][0]     # 4 = "Neutro inherente absoluto"
    animacidad = tensor[0][4][0] # 6 = "Inanimado abstracto mental"
    
    print(f"   • Es abstracto y mental (tipo: {tipo_sust})")
    print(f"   • Género neutro (valor: {genero})")
    print(f"   • Concepto abstracto (animacidad: {animacidad})")
    
    # Analizar FORMA 1 (Verbo)
    print("\n🎬 PISTAS DE LA ACCIÓN (Verbo):")
    aspecto = tensor[1][1][0]    # 2 = "Imperfectivo progresivo continuo"
    transitividad = tensor[1][4][0] # 0 = "Transitivo directo"
    
    print(f"   • Acción continua y progresiva (aspecto: {aspecto})")
    print(f"   • Requiere objeto directo (transitividad: {transitividad})")
    print(f"   • Es una acción perceptual/sensorial")
    
    # Analizar FORMA 2 (Adjetivo)
    print("\n✨ PISTAS DE LA CUALIDAD (Adjetivo):")
    clase_sem = tensor[2][5][0]  # 0 = "Físico perceptible"
    posicion = tensor[2][2][0]   # 2 = "Postnominal descriptivo"
    
    print(f"   • Cualidad físicamente perceptible (clase: {clase_sem})")
    print(f"   • Se describe después del sustantivo (posición: {posicion})")
    
    print("\n🎯 PISTAS ADICIONALES:")
    print("   • Fundamental en la experiencia humana")
    print("   • Relacionado con movimiento y percepción")
    print("   • Puede ser literal o metafórico")
    print("   • Todos lo experimentamos diariamente")
    
    print("\n" + "=" * 60)
    print("🤔 ¿PUEDES ADIVINAR QUÉ PALABRA ES?")
    print("   Pista final: 'Los ojos son las ventanas del...'")
    print("=" * 60)

def reveal_answer():
    """Revela la respuesta del tensor misterioso"""
    
    print("\n" + "🎊" * 20)
    print("¡RESPUESTA REVELADA!")
    print("🎊" * 20)
    print("\n🎯 LA PALABRA ES: *** ALMA *** 🎯")
    print("\n💫 EXPLICACIÓN DEL TENSOR:")
    print("   • FORMA 0 (Sustantivo): Concepto abstracto, neutro, mental")
    print("   • FORMA 1 (Verbo): 'Almar' - percibir el alma (acción continua)")
    print("   • FORMA 2 (Adjetivo): 'Alma' como cualidad perceptible")
    print("\n🔮 El tensor representa las múltiples dimensiones de 'ALMA':")
    print("   - Como sustantivo: entidad abstracta mental")
    print("   - Como verbo: acción de percibir/conectar espiritualmente")  
    print("   - Como adjetivo: cualidad que se percibe en otros")
    print("\n✨ Tensor FFE 3×9×27 completamente funcional ✨")

def main():
    """Función principal del juego de adivinanza"""
    
    print("🎮 TENSOR ADIVINANZA - Sistema FFE 3×9×27 🎮")
    print("=" * 50)
    
    try:
        # Cargar catálogo
        catalog = load_ffe_catalog()
        print("✅ Catálogo FFE cargado correctamente")
        
        # Generar tensor misterioso
        mystery_tensor = generate_mystery_tensor()
        print(f"✅ Tensor misterioso generado: {len(mystery_tensor)}×{len(mystery_tensor[0])}×{len(mystery_tensor[0][0])}")
        
        # Mostrar tensor sin revelar la palabra
        print("\n🔢 TENSOR MISTERIOSO:")
        print("-" * 30)
        for i, forma in enumerate(mystery_tensor):
            print(f"Forma {i}: {forma[0][:3]}... (parcial)")
        
        # Analizar pistas
        analyze_tensor_clues(mystery_tensor, catalog)
        
        # Preguntar si quiere ver la respuesta
        print("\n" + "⏳" * 10)
        input("Presiona ENTER para ver la respuesta...")
        
        # Revelar respuesta
        reveal_answer()
        
        # Mostrar tensor completo
        print("\n📊 TENSOR COMPLETO:")
        print("-" * 40)
        for i, forma in enumerate(mystery_tensor):
            print(f"\nForma {i} ({'Sustantivo' if i==0 else 'Verbo' if i==1 else 'Adjetivo'}):")
            for j, subdim in enumerate(forma):
                print(f"  Subdim {i}.{j}: {subdim}")
        
        print("\n🏆 ¡Gracias por jugar con el tensor Aurora!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que el archivo ffe_catalog.yaml existe en catalogs/")

if __name__ == "__main__":
    main()
