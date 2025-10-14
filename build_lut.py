"""
Script para compilar/generar las tablas de búsqueda (LUTs) a partir de los catálogos FFE.
Maneja la estructura fractal 3-9-27 de los vectores Aurora.
"""
import yaml
import msgpack
import os
import json
from typing import Dict, List, Any

CATALOG_PATH = os.path.join(os.path.dirname(__file__), 'catalogs', 'ffe_catalog.yaml')
WORDS_PATH = os.path.join(os.path.dirname(__file__), 'catalogs', 'example_words.yaml')
LUT_PATH = os.path.join(os.path.dirname(__file__), 'catalogs', 'lut.msgpack')
LUT_JSON_PATH = os.path.join(os.path.dirname(__file__), 'catalogs', 'lut.json')

def load_yaml(path: str) -> Dict[str, Any]:
    """Carga un archivo YAML."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_fractal_vector(word: str, word_data: Dict[str, Any]) -> bool:
    """Valida que el vector fractal tenga la estructura correcta 3-9-27."""
    try:
        # Verificar nivel_3: debe tener 3 elementos
        nivel_3 = word_data.get('nivel_3', [])
        if len(nivel_3) != 3:
            print(f"⚠️  {word}: nivel_3 debe tener 3 elementos, tiene {len(nivel_3)}")
            return False
        
        # Verificar nivel_9: debe tener 3 sublistas de 3 elementos cada una
        nivel_9 = word_data.get('nivel_9', [])
        if len(nivel_9) != 3:
            print(f"⚠️  {word}: nivel_9 debe tener 3 sublistas, tiene {len(nivel_9)}")
            return False
        
        for i, sublista in enumerate(nivel_9):
            if len(sublista) != 3:
                print(f"⚠️  {word}: nivel_9[{i}] debe tener 3 elementos, tiene {len(sublista)}")
                return False
        
        # Verificar nivel_27: debe tener estructura forma/funcion/estructura con 3x3 cada una
        nivel_27 = word_data.get('nivel_27', {})
        required_keys = ['forma', 'funcion', 'estructura']
        
        for key in required_keys:
            if key not in nivel_27:
                print(f"⚠️  {word}: nivel_27 debe tener clave '{key}'")
                return False
            
            section = nivel_27[key]
            if len(section) != 3:
                print(f"⚠️  {word}: nivel_27.{key} debe tener 3 sublistas, tiene {len(section)}")
                return False
            
            for i, sublista in enumerate(section):
                if len(sublista) != 3:
                    print(f"⚠️  {word}: nivel_27.{key}[{i}] debe tener 3 elementos, tiene {len(sublista)}")
                    return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error validando {word}: {e}")
        return False

def build_fractal_tensor(word: str, word_data: Dict[str, Any], catalog: Dict[str, Any]) -> Dict[str, Any]:
    """Construye un tensor fractal completo para una palabra."""
    
    if not validate_fractal_vector(word, word_data):
        return None
    
    # Extraer datos del vector fractal
    nivel_3 = word_data['nivel_3']
    nivel_9 = word_data['nivel_9']
    nivel_27 = word_data['nivel_27']
    
    # Construir tensor con metadatos descriptivos
    tensor = {
        'palabra': word,
        'nivel_3': {
            'vector': nivel_3,
            'descripcion': [
                catalog['forma']['values'].get(nivel_3[0], f"forma_{nivel_3[0]}"),
                catalog['funcion']['values'].get(nivel_3[1], f"funcion_{nivel_3[1]}"), 
                catalog['estructura']['values'].get(nivel_3[2], f"estructura_{nivel_3[2]}")
            ]
        },
        'nivel_9': {
            'vector': nivel_9,
            'descripcion': {
                'forma': nivel_9[0],
                'funcion': nivel_9[1], 
                'estructura': nivel_9[2]
            }
        },
        'nivel_27': {
            'vector': nivel_27,
            'total_dimensions': 27,
            'estructura_fractal': {
                'forma': nivel_27['forma'],
                'funcion': nivel_27['funcion'],
                'estructura': nivel_27['estructura']
            }
        },
        'metadata': {
            'total_bits': 27 * 3,  # Aproximadamente para valores 1-3
            'fractal_depth': 3,
            'expandible': True
        }
    }
    
    return tensor

def build_lut():
    """Construye la tabla de búsqueda (LUT) con tensores fractales."""
    print("🔧 Cargando catálogos...")
    
    try:
        ffe_catalog = load_yaml(CATALOG_PATH)
        words = load_yaml(WORDS_PATH)
    except Exception as e:
        print(f"❌ Error cargando archivos: {e}")
        return
    
    print(f"📖 Procesando {len(words)} palabras...")
    
    lut = {}
    valid_words = 0
    
    for word, word_data in words.items():
        tensor = build_fractal_tensor(word, word_data, ffe_catalog)
        if tensor:
            lut[word] = tensor
            valid_words += 1
            print(f"✅ {word}: tensor fractal generado")
        else:
            print(f"❌ {word}: error en la estructura del vector")
    
    # Guardar en formato msgpack (binario, compacto)
    try:
        with open(LUT_PATH, 'wb') as f:
            msgpack.pack(lut, f)
        print(f"💾 LUT binario guardado en {LUT_PATH}")
    except Exception as e:
        print(f"❌ Error guardando LUT binario: {e}")
    
    # Guardar también en JSON (legible, para debug)
    try:
        with open(LUT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(lut, f, indent=2, ensure_ascii=False)
        print(f"💾 LUT JSON guardado en {LUT_JSON_PATH}")
    except Exception as e:
        print(f"❌ Error guardando LUT JSON: {e}")
    
    print(f"\n📊 Resumen:")
    print(f"   - Palabras procesadas: {len(words)}")
    print(f"   - Tensores válidos: {valid_words}")
    print(f"   - Dimensiones por tensor: 3 + 9 + 27 = 39")
    print(f"   - Tamaño estimado por tensor: ~117 bits")

def test_lut():
    """Prueba la LUT generada."""
    if not os.path.exists(LUT_PATH):
        print("❌ LUT no encontrada. Ejecuta build_lut() primero.")
        return
    
    try:
        with open(LUT_PATH, 'rb') as f:
            lut = msgpack.unpack(f)
        
        print("\n🧪 Probando LUT...")
        test_words = ['casa', 'sol', 'amor']
        
        for word in test_words:
            if word in lut:
                tensor = lut[word]
                print(f"\n📍 {word}:")
                print(f"   Nivel 3: {tensor['nivel_3']['vector']} -> {tensor['nivel_3']['descripcion']}")
                print(f"   Nivel 9: {tensor['nivel_9']['vector']}")
                print(f"   Nivel 27: Estructura fractal con {tensor['nivel_27']['total_dimensions']} dimensiones")
            else:
                print(f"❌ {word} no encontrada en LUT")
                
    except Exception as e:
        print(f"❌ Error probando LUT: {e}")

if __name__ == "__main__":
    print("🚀 Generador de LUT para tensores fractales Aurora")
    print("=" * 50)
    
    build_lut()
    test_lut()
    
    print("\n✨ Proceso completado.")
