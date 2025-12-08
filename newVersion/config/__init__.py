"""
Configuración del sistema Aurora Genesis
TODO: Agregar configuración centralizada
"""

# Configuración por defecto
DEFAULT_CONFIG = {
    "trigate": {
        "use_luts": True,
    },
    "transcender": {
        "max_tries": 3,
        "check_reconstruction": True,
        "enforce_coherence": True,
    },
    "evolver": {
        "th_match": 2,
        "decay": 0.9,
    },
    "harmonizer": {
        "max_conflicts": 0,
        "max_null_fills": 3,
        "min_child_sim": 6,
    },
    "pipeline": {
        "enable_harmony": True,
        "verbose": True,
    }
}

__all__ = ["DEFAULT_CONFIG"]
