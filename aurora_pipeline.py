# Aurora Pipeline - Proyecto Genesis
# Pipeline completo: LLM embeddings → Tensores FFE → Transcender → Evolver → Aurora

import yaml
import numpy as np
from typing import Dict, List, Tuple, Optional
from aurora_prototype import Trigate, Transcender, FractalTensor, flat_to_fractal, load_ffe_catalog


class AuroraPipeline:
    """
    Pipeline completo para transformar conversaciones LLM en inteligencia fractal.
    
    Flujo:
    1. probe_llm: Extrae embeddings del LLM
    2. ffe_encoder: Convierte embeddings → tensor FFE {3,9,27}
    3. transcender: Síntesis emergente (Ms, Ss, MetaM)
    4. ffe_store: Almacena en Knowledge Base
    5. evolver: Aprende arquetipos, relaciones, dinámicas
    """
    
    def __init__(self, catalog_path: str = "catalogs/ffe_catalog.yaml"):
        self.catalog = load_ffe_catalog(catalog_path)
        self.trigate = Trigate()
        self.transcender = Transcender()
        self.knowledge_base = []  # Lista de tensores almacenados
        self.archetypes = {}      # Patrones transversales aprendidos
        self.dynamics = []        # Evolución temporal
        
    # ========== FASE 1: PROBE LLM ==========
    def probe_llm(self, text: str, mock: bool = True) -> np.ndarray:
        """
        Extrae embeddings del LLM.
        
        Args:
            text: Texto de entrada
            mock: Si True, genera embeddings simulados (para testing sin LLM real)
            
        Returns:
            Embedding de 768 dimensiones (simulado) o real desde API
        """
        if mock:
            # Simulación: embeddings basados en hash del texto
            np.random.seed(hash(text) % (2**32))
            embedding = np.random.randn(768)
            return embedding / np.linalg.norm(embedding)  # Normalizar
        else:
            # TODO: Integrar con API real (OpenAI, Anthropic, etc.)
            # from openai import OpenAI
            # client = OpenAI()
            # response = client.embeddings.create(input=text, model="text-embedding-3-small")
            # return np.array(response.data[0].embedding)
            raise NotImplementedError("API real no implementada aún")
    
    # ========== FASE 2: FFE ENCODER ==========
    def ffe_encoder(self, embedding: np.ndarray, method: str = "pca_discretize") -> List[int]:
        """
        Convierte embedding plano → tensor FFE {3,9,27} = 39 valores discretos (0-7).
        
        Métodos:
        - pca_discretize: PCA + cuantización en 8 niveles
        - semantic_map: Mapeo semántico directo (requiere modelo entrenado)
        - learned_projection: Proyección aprendida (futuro)
        
        Args:
            embedding: Vector de embeddings (e.g., 768 dims)
            method: Método de conversión
            
        Returns:
            Lista de 39 enteros (0-7) representando el tensor fractal
        """
        if method == "pca_discretize":
            # Reducir 768 dims → 39 dims con PCA (simulado)
            # En producción: usar PCA entrenado con corpus
            np.random.seed(int(np.sum(embedding * 1000) % (2**32)))
            reduced = np.random.randn(39)
            
            # Normalizar a [0, 1]
            normalized = (reduced - reduced.min()) / (reduced.max() - reduced.min())
            
            # Cuantizar a 8 niveles (0-7)
            discretized = (normalized * 7.99).astype(int)
            discretized = np.clip(discretized, 0, 7)
            
            return discretized.tolist()
        
        elif method == "semantic_map":
            # TODO: Mapeo semántico usando análisis del texto
            raise NotImplementedError("Mapeo semántico no implementado")
        
        else:
            raise ValueError(f"Método desconocido: {method}")
    
    # ========== FASE 3: TRANSCENDER SERVICE ==========
    def synthesize_conversation(
        self, 
        tensor_input: FractalTensor, 
        tensor_output: FractalTensor
    ) -> Dict:
        """
        Síntesis emergente: combina tensor de entrada (usuario) y salida (LLM).
        
        Returns:
            Dict con Ms (estructura emergente), Ss (forma), MetaM (función)
        """
        # Usar nivel superior (3D) de cada tensor
        A = tensor_input.level_3
        B = tensor_output.level_3
        C = [1, 0, 1]  # Vector neutro para completar tríada
        
        synthesis = self.transcender.synthesize(A, B, C)
        
        # Verificar coherencia ética
        coherent, message = tensor_input.check_ethical_coherence(self.transcender)
        synthesis["ethical_check"] = {"coherent": coherent, "message": message}
        
        return synthesis
    
    # ========== FASE 4: FFE STORE ==========
    def store_tensor(
        self, 
        tensor: FractalTensor, 
        synthesis: Dict, 
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Almacena tensor y síntesis en Knowledge Base.
        
        Returns:
            ID del tensor almacenado
        """
        entry = {
            "id": len(self.knowledge_base),
            "tensor": tensor,
            "synthesis": synthesis,
            "metadata": metadata or {},
            "timestamp": len(self.dynamics)  # Usar índice como timestamp
        }
        self.knowledge_base.append(entry)
        return entry["id"]
    
    # ========== FASE 5: EVOLVER ==========
    def evolve_archetypes(self, window: int = 10) -> Dict:
        """
        Aprende arquetipos: patrones transversales en últimas N interacciones.
        
        Archetype = patrón común en distintos espacios lógicos
        """
        if len(self.knowledge_base) < window:
            return {"status": "insufficient_data", "min_required": window}
        
        recent = self.knowledge_base[-window:]
        
        # Detectar patrones en Ms (estructuras emergentes)
        ms_patterns = {}
        for entry in recent:
            ms_key = tuple(entry["synthesis"]["Ms"])
            if ms_key not in ms_patterns:
                ms_patterns[ms_key] = 0
            ms_patterns[ms_key] += 1
        
        # Arquetipos = patrones con frecuencia > umbral
        threshold = window * 0.3  # 30% repetición
        new_archetypes = {
            k: v for k, v in ms_patterns.items() 
            if v >= threshold
        }
        
        self.archetypes.update(new_archetypes)
        
        return {
            "status": "success",
            "new_archetypes": len(new_archetypes),
            "total_archetypes": len(self.archetypes),
            "patterns": new_archetypes
        }
    
    def evolve_dynamics(self, tensor: FractalTensor, new_data: List[int]) -> Tuple[bool, str]:
        """
        Fractal Dynamics: adapta tensor a nuevos datos rechazando cambios destructivos.
        """
        time_step = len(self.dynamics)
        success, message = tensor.evolve(self.transcender, new_data, time_step)
        
        if success:
            self.dynamics.append({
                "time": time_step,
                "tensor_state": tensor.level_3.copy(),
                "action": "evolved",
                "message": message
            })
        else:
            self.dynamics.append({
                "time": time_step,
                "action": "rejected",
                "message": message
            })
        
        return success, message
    
    # ========== PIPELINE COMPLETO ==========
    def text_to_fractal(self, text: str) -> FractalTensor:
        """
        Conversión completa: texto → embedding → tensor FFE
        """
        # Paso 1: Probe LLM
        embedding = self.probe_llm(text, mock=True)
        
        # Paso 2: FFE Encoder
        flat_ffe = self.ffe_encoder(embedding)
        
        # Paso 3: Construir FractalTensor
        tensor = flat_to_fractal(flat_ffe)
        
        return tensor
    
    def process_conversation_turn(
        self, 
        user_text: str, 
        llm_text: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Procesa un turno completo de conversación:
        1. Usuario habla → tensor_input
        2. LLM responde → tensor_output
        3. Síntesis emergente
        4. Almacenamiento
        5. Evolución de arquetipos
        
        Returns:
            Resultado completo con tensores, síntesis y evolución
        """
        # Convertir textos a tensores
        tensor_input = self.text_to_fractal(user_text)
        tensor_output = self.text_to_fractal(llm_text)
        
        # Síntesis emergente
        synthesis = self.synthesize_conversation(tensor_input, tensor_output)
        
        # Almacenar
        input_id = self.store_tensor(tensor_input, synthesis, {
            "type": "user_input",
            "text": user_text,
            **(metadata or {})
        })
        output_id = self.store_tensor(tensor_output, synthesis, {
            "type": "llm_output",
            "text": llm_text,
            **(metadata or {})
        })
        
        # Evolucionar arquetipos
        evolution_result = self.evolve_archetypes()
        
        return {
            "input_tensor_id": input_id,
            "output_tensor_id": output_id,
            "synthesis": synthesis,
            "evolution": evolution_result,
            "kb_size": len(self.knowledge_base),
            "archetypes_count": len(self.archetypes)
        }
    
    # ========== UTILIDADES ==========
    def get_kb_summary(self) -> Dict:
        """Resumen del estado de la Knowledge Base"""
        return {
            "total_tensors": len(self.knowledge_base),
            "total_archetypes": len(self.archetypes),
            "total_dynamics": len(self.dynamics),
            "latest_archetype": list(self.archetypes.keys())[-1] if self.archetypes else None
        }
    
    def visualize_tensor(self, tensor: FractalTensor) -> str:
        """Representación legible de un tensor"""
        lines = ["=== Fractal Tensor ==="]
        lines.append(f"Level 3 (Main): {tensor.level_3}")
        lines.append(f"Level 9 (Sub):  {tensor.level_9}")
        lines.append(f"Level 27 (Detail): [Showing first sub-level]")
        lines.append(f"  {tensor.level_27[0]}")
        
        # Etiquetas semánticas
        lines.append("\n--- Semantic Labels (Level 3) ---")
        for i, val in enumerate(tensor.level_3):
            label = tensor.get_value_label(i, 0, 0, val)
            lines.append(f"  Axis {i}: {label}")
        
        return "\n".join(lines)


# ========== DEMO ==========
if __name__ == "__main__":
    print("🌌 Aurora Pipeline - Proyecto Genesis\n")
    
    # Inicializar pipeline
    pipeline = AuroraPipeline()
    
    # Simulación de conversación
    conversations = [
        ("¿Qué es la justicia?", "La justicia es el equilibrio entre derechos y deberes."),
        ("¿Y la verdad?", "La verdad es la correspondencia entre pensamiento y realidad."),
        ("¿Cómo se relacionan?", "Justicia sin verdad es arbitrariedad; verdad sin justicia es crueldad.")
    ]
    
    print("=== Procesando Conversaciones ===\n")
    for i, (user, llm) in enumerate(conversations, 1):
        print(f"--- Turno {i} ---")
        print(f"Usuario: {user}")
        print(f"LLM: {llm}")
        
        result = pipeline.process_conversation_turn(user, llm, {"turn": i})
        
        print(f"✓ Tensores almacenados: {result['input_tensor_id']}, {result['output_tensor_id']}")
        print(f"✓ Síntesis Ms: {result['synthesis']['Ms']}")
        print(f"✓ Arquetipos detectados: {result['archetypes_count']}")
        print(f"✓ Coherencia ética: {result['synthesis']['ethical_check']['message']}\n")
    
    # Resumen final
    print("=== Resumen Final ===")
    summary = pipeline.get_kb_summary()
    print(f"Total tensores en KB: {summary['total_tensors']}")
    print(f"Total arquetipos: {summary['total_archetypes']}")
    print(f"Último arquetipo: {summary['latest_archetype']}")
    
    # Visualizar primer tensor
    print("\n=== Ejemplo de Tensor (primer input) ===")
    first_tensor = pipeline.knowledge_base[0]["tensor"]
    print(pipeline.visualize_tensor(first_tensor))
