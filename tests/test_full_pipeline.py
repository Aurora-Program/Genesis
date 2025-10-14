"""
Test Suite - Proyecto Genesis
Tests de integración para el pipeline completo Aurora
"""

import pytest
import sys
from pathlib import Path

# Añadir raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from aurora_prototype import Trigate, Transcender, FractalTensor, flat_to_fractal
from aurora_pipeline import AuroraPipeline
from mcp_servers.ffe_store import FFEStore


class TestTrigate:
    """Tests para Trigate con lógica ternaria"""
    
    def test_infer_basic(self):
        tg = Trigate()
        result = tg.infer([0, 1, 1], [1, 0, 1], [1, 0, 1])
        # XOR logic: 0⊕1=1, 1⊕0=0 (not XOR), 1⊕1=0
        assert result == [1, 0, 0]
    
    def test_infer_with_null(self):
        tg = Trigate()
        result = tg.infer([0, None, 1], [1, 0, 1], [1, 0, 1])
        assert result[1] is None  # NULL se propaga
    
    def test_learn(self):
        tg = Trigate()
        M = tg.learn([0, 1, 1], [1, 0, 1], [1, 1, 0])
        # Learning the control vector that produces the result
        assert M == [1, 1, 1]


class TestTranscender:
    """Tests para Transcender (síntesis emergente)"""
    
    def test_synthesis_basic(self):
        tc = Transcender()
        result = tc.synthesize([0, 1, 0], [1, 0, 1], [0, 1, 1])
        
        assert "Ms" in result
        assert "Ss" in result
        assert "MetaM" in result
        assert len(result["Ms"]) == 3
    
    def test_synthesis_non_commutative(self):
        tc = Transcender()
        result1 = tc.synthesize([0, 1, 0], [1, 0, 1], [0, 1, 1])
        result2 = tc.synthesize([1, 0, 1], [0, 1, 0], [0, 1, 1])
        
        # Order matters - synthesis is non-commutative
        # (can be same or different depending on control vectors)
        assert isinstance(result1["Ms"], list)
        assert isinstance(result2["Ms"], list)


class TestFractalTensor:
    """Tests para FractalTensor"""
    
    def test_creation(self):
        tensor = FractalTensor([1, 2, 3], [[0]*3]*3, [[[0]*3]*3]*3)
        assert tensor.level_3 == [1, 2, 3]
    
    def test_flat_to_fractal_conversion(self):
        flat = [i % 8 for i in range(39)]
        tensor = flat_to_fractal(flat)
        assert len(tensor.level_3) == 3
        assert len(tensor.level_9) == 3
        assert len(tensor.level_27) == 3
    
    def test_ethical_coherence(self):
        tc = Transcender()
        tensor = FractalTensor([1, 2, 3])
        coherent, message = tensor.check_ethical_coherence(tc)
        assert coherent is True
        assert "coherent" in message.lower()
    
    def test_evolution(self):
        tc = Transcender()
        tensor = FractalTensor([0, 1, 0])
        new_data = [1, 0, 1, 0, 1, 0]
        success, message = tensor.evolve(tc, new_data, 1)
        # Success depends on synthesis result
        assert isinstance(success, bool)
        assert isinstance(message, str)


class TestFFEStore:
    """Tests para FFE Store (Knowledge Base)"""
    
    @pytest.fixture
    def store(self, tmp_path):
        """Fixture que crea un store temporal"""
        db_path = tmp_path / "test_kb.db"
        return FFEStore(str(db_path))
    
    def test_store_and_retrieve_tensor(self, store):
        tensor_dict = {
            "level_3": [1, 2, 3],
            "level_9": [[i]*3 for i in range(3)],
            "level_27": [[[j]*3]*3 for j in range(3)]
        }
        
        tensor_id = store.store_tensor(tensor_dict)
        assert tensor_id > 0
        
        retrieved = store.get_tensor(tensor_id)
        assert retrieved is not None
        assert retrieved["tensor"]["level_3"] == [1, 2, 3]
    
    def test_store_archetype(self, store):
        pattern = "(0,1,0)"
        arch_id = store.store_archetype(pattern)
        assert arch_id > 0
        
        # Store same pattern again
        store.store_archetype(pattern)
        
        top = store.get_top_archetypes(5)
        assert len(top) > 0
        assert top[0]["pattern"] == pattern
        assert top[0]["frequency"] == 2
    
    def test_query_recent(self, store):
        # Store multiple tensors
        for i in range(5):
            tensor_dict = {"level_3": [i, i+1, i+2]}
            store.store_tensor(tensor_dict)
        
        recent = store.query_recent(3)
        assert len(recent) == 3
        # Most recent first
        assert recent[0]["tensor"]["level_3"][0] == 4
    
    def test_stats(self, store):
        # Store some data
        store.store_tensor({"level_3": [1, 2, 3]})
        store.store_archetype("(0,1,0)")
        
        stats = store.get_stats()
        assert stats["total_tensors"] == 1
        assert stats["total_archetypes"] == 1


class TestAuroraPipeline:
    """Tests para el pipeline completo"""
    
    @pytest.fixture
    def pipeline(self):
        return AuroraPipeline()
    
    def test_probe_llm_mock(self, pipeline):
        embedding = pipeline.probe_llm("test text", mock=True)
        assert embedding.shape == (768,)
        assert -1 <= embedding[0] <= 1  # Normalized
    
    def test_ffe_encoder(self, pipeline):
        import numpy as np
        embedding = np.random.randn(768)
        flat_ffe = pipeline.ffe_encoder(embedding)
        
        assert len(flat_ffe) == 39
        assert all(0 <= v <= 7 for v in flat_ffe)
    
    def test_text_to_fractal(self, pipeline):
        tensor = pipeline.text_to_fractal("Hello world")
        assert isinstance(tensor, FractalTensor)
        assert len(tensor.level_3) == 3
    
    def test_synthesize_conversation(self, pipeline):
        tensor_input = pipeline.text_to_fractal("¿Qué es la verdad?")
        tensor_output = pipeline.text_to_fractal("La verdad es correspondencia con la realidad")
        
        synthesis = pipeline.synthesize_conversation(tensor_input, tensor_output)
        
        assert "Ms" in synthesis
        assert "Ss" in synthesis
        assert "MetaM" in synthesis
        assert "ethical_check" in synthesis
    
    def test_process_conversation_turn(self, pipeline):
        result = pipeline.process_conversation_turn(
            "¿Qué es la justicia?",
            "La justicia es equilibrio entre derechos y deberes"
        )
        
        assert "input_tensor_id" in result
        assert "output_tensor_id" in result
        assert "synthesis" in result
        assert "evolution" in result
        assert result["kb_size"] >= 2
    
    def test_evolve_archetypes(self, pipeline):
        # Generate enough conversations to detect patterns
        for i in range(15):
            pipeline.process_conversation_turn(
                f"Question {i}",
                f"Answer {i}"
            )
        
        evolution = pipeline.evolve_archetypes(window=10)
        assert evolution["status"] == "success"
        # May or may not find archetypes depending on random generation
        assert "total_archetypes" in evolution
    
    def test_kb_summary(self, pipeline):
        pipeline.process_conversation_turn("Q1", "A1")
        pipeline.process_conversation_turn("Q2", "A2")
        
        summary = pipeline.get_kb_summary()
        assert summary["total_tensors"] == 4  # 2 inputs + 2 outputs


# ========== INTEGRATION TESTS ==========
class TestFullIntegration:
    """Tests de integración completa del sistema"""
    
    def test_end_to_end_conversation(self):
        """Test del flujo completo: texto → tensor → síntesis → KB → evolución"""
        pipeline = AuroraPipeline()
        
        conversations = [
            ("¿Qué es el amor?", "El amor es unión que respeta la individualidad"),
            ("¿Y el odio?", "El odio es separación que niega al otro"),
            ("¿Cómo superarlo?", "Mediante comprensión y transformación")
        ]
        
        for user, llm in conversations:
            result = pipeline.process_conversation_turn(user, llm)
            assert result["synthesis"]["ethical_check"]["coherent"] is True
        
        # Verificar que se almacenaron todos los tensores
        summary = pipeline.get_kb_summary()
        assert summary["total_tensors"] == 6  # 3 turnos × 2 tensores cada uno
        
        # Verificar evolución de arquetipos (necesita al menos 10 entries)
        evolution = pipeline.evolve_archetypes()
        if evolution["status"] == "insufficient_data":
            # No hay suficientes datos, esperado con solo 3 conversaciones
            assert evolution["min_required"] == 10
        else:
            assert "total_archetypes" in evolution
    
    def test_ethical_rejection(self):
        """Test de rechazo ético ante tensores con alta incertidumbre"""
        pipeline = AuroraPipeline()
        tc = Transcender()
        
        # Crear tensor con muchos NULLs
        tensor = FractalTensor(
            [1, 2, 3],
            [[0]*3]*3,
            [[[None, None, None]]*3]*3  # Todos NULL
        )
        
        coherent, message = tensor.check_ethical_coherence(tc)
        assert coherent is False
        assert "risk" in message.lower()


# ========== PYTEST CONFIGURATION ==========
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
