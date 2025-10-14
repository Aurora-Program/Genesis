"""
Resilient MCP Client - Circuit Breaker Pattern
===============================================
Cliente robusto con retry logic, circuit breaker y fallback strategies
para servicios MCP críticos.

Características:
- Circuit Breaker de 3 estados (CLOSED, OPEN, HALF_OPEN)
- Retry exponential backoff
- Fallback strategies por servicio
- Métricas de latencia y tasa de fallos
"""

import time
import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Estados del circuit breaker"""
    CLOSED = "closed"        # Funcionamiento normal
    OPEN = "open"            # Circuito abierto (muchos fallos)
    HALF_OPEN = "half_open"  # Prueba de recuperación


@dataclass
class CircuitBreakerConfig:
    """Configuración del circuit breaker"""
    failure_threshold: int = 5          # Fallos antes de abrir circuito
    recovery_timeout: float = 30.0      # Segundos antes de intentar recuperar
    success_threshold: int = 2          # Éxitos para cerrar circuito
    timeout: float = 2.0                # Timeout por llamada
    
    # Ventana deslizante para tasa de fallos
    window_size: int = 10
    failure_rate_threshold: float = 0.5  # 50% de fallos


@dataclass
class ServiceMetrics:
    """Métricas de rendimiento del servicio"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    circuit_opens: int = 0
    
    # Latencias recientes (ms)
    recent_latencies: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def record_success(self, latency_ms: float):
        """Registra llamada exitosa"""
        self.total_calls += 1
        self.successful_calls += 1
        self.recent_latencies.append(latency_ms)
    
    def record_failure(self):
        """Registra llamada fallida"""
        self.total_calls += 1
        self.failed_calls += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas consolidadas"""
        if not self.recent_latencies:
            avg_latency = 0.0
            p95_latency = 0.0
        else:
            sorted_lat = sorted(self.recent_latencies)
            avg_latency = sum(sorted_lat) / len(sorted_lat)
            p95_index = int(len(sorted_lat) * 0.95)
            p95_latency = sorted_lat[p95_index] if p95_index < len(sorted_lat) else sorted_lat[-1]
        
        success_rate = (self.successful_calls / self.total_calls * 100) if self.total_calls > 0 else 0.0
        
        return {
            "total_calls": self.total_calls,
            "success_rate": f"{success_rate:.1f}%",
            "failed_calls": self.failed_calls,
            "circuit_opens": self.circuit_opens,
            "avg_latency_ms": f"{avg_latency:.2f}",
            "p95_latency_ms": f"{p95_latency:.2f}"
        }


class CircuitBreaker:
    """
    Circuit Breaker para prevenir cascadas de fallos.
    
    Estados:
    - CLOSED: Normal, todas las llamadas pasan
    - OPEN: Demasiados fallos, rechaza llamadas inmediatamente
    - HALF_OPEN: Prueba de recuperación, permite llamadas limitadas
    """
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        
        # Ventana deslizante de resultados
        self.recent_results: deque = deque(maxlen=config.window_size)
        
        self.metrics = ServiceMetrics()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecuta función protegida por circuit breaker.
        
        Raises:
            CircuitOpenError: Si el circuito está abierto
            Exception: Errores propagados de la función
        """
        # Verificar si podemos intentar la llamada
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info("Circuit breaker: Transitioning to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(f"Circuit breaker is OPEN (recovery in {self._time_until_retry():.1f}s)")
        
        # Intentar la llamada
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_ms = (time.time() - start_time) * 1000
            
            self._on_success(elapsed_ms)
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self, latency_ms: float):
        """Maneja llamada exitosa"""
        self.metrics.record_success(latency_ms)
        self.recent_results.append(True)
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                logger.info(f"Circuit breaker: Transitioning to CLOSED after {self.success_count} successes")
                self._reset()
        
        # Resetear contadores de fallo
        self.failure_count = 0
    
    def _on_failure(self):
        """Maneja llamada fallida"""
        self.metrics.record_failure()
        self.recent_results.append(False)
        self.last_failure_time = time.time()
        self.failure_count += 1
        
        # Calcular tasa de fallos en ventana deslizante
        if len(self.recent_results) >= self.config.window_size:
            failure_rate = sum(1 for r in self.recent_results if not r) / len(self.recent_results)
            
            if failure_rate >= self.config.failure_rate_threshold:
                self._trip()
        
        # O si excedemos threshold absoluto
        elif self.failure_count >= self.config.failure_threshold:
            self._trip()
        
        # En HALF_OPEN, un fallo abre de nuevo
        if self.state == CircuitState.HALF_OPEN:
            logger.warning("Circuit breaker: Failure in HALF_OPEN, reopening circuit")
            self._trip()
    
    def _trip(self):
        """Abre el circuito"""
        if self.state != CircuitState.OPEN:
            logger.error(f"Circuit breaker: OPENING (failures: {self.failure_count})")
            self.state = CircuitState.OPEN
            self.metrics.circuit_opens += 1
            self.last_failure_time = time.time()
    
    def _reset(self):
        """Resetea el circuito a estado normal"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.recent_results.clear()
    
    def _should_attempt_reset(self) -> bool:
        """Verifica si es hora de intentar recuperación"""
        if self.last_failure_time is None:
            return True
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.config.recovery_timeout
    
    def _time_until_retry(self) -> float:
        """Tiempo hasta próximo intento de recuperación"""
        if self.last_failure_time is None:
            return 0.0
        elapsed = time.time() - self.last_failure_time
        return max(0.0, self.config.recovery_timeout - elapsed)
    
    def get_state(self) -> Dict[str, Any]:
        """Estado actual del circuit breaker"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "time_until_retry": self._time_until_retry() if self.state == CircuitState.OPEN else 0.0,
            "metrics": self.metrics.get_stats()
        }


class CircuitOpenError(Exception):
    """Excepción cuando el circuito está abierto"""
    pass


class ResilientMCPClient:
    """
    Cliente MCP con resiliencia avanzada:
    - Circuit breaker por servicio
    - Retry con exponential backoff
    - Fallback strategies
    - Métricas consolidadas
    """
    
    def __init__(
        self,
        service_name: str,
        max_retries: int = 3,
        base_timeout: float = 2.0,
        circuit_config: Optional[CircuitBreakerConfig] = None
    ):
        self.service_name = service_name
        self.max_retries = max_retries
        self.base_timeout = base_timeout
        
        # Circuit breaker
        self.circuit = CircuitBreaker(circuit_config or CircuitBreakerConfig())
        
        # Estrategias de fallback por servicio
        self.fallback_strategies = {
            "probe_llm": self._fallback_embedding,
            "ffe_encoder": self._fallback_tensor,
            "transcender": self._fallback_synthesis,
            "evolver": self._fallback_evolution
        }
        
        logger.info(f"Initialized ResilientMCPClient for '{service_name}'")
    
    def call_service(self, service_func: Callable, payload: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Llama a servicio MCP con resiliencia completa.
        
        Args:
            service_func: Función del servicio a llamar
            payload: Payload del servicio
            **kwargs: Argumentos adicionales
        
        Returns:
            Respuesta del servicio o fallback
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Timeout exponencial backoff
                timeout = self.base_timeout * (2 ** attempt)
                
                # Llamar con circuit breaker
                result = self.circuit.call(
                    self._execute_with_timeout,
                    service_func,
                    payload,
                    timeout,
                    **kwargs
                )
                
                logger.info(f"{self.service_name}: Success on attempt {attempt + 1}")
                return result
                
            except CircuitOpenError as e:
                logger.warning(f"{self.service_name}: {e}")
                return self._get_fallback(payload)
                
            except Exception as e:
                last_exception = e
                logger.warning(f"{self.service_name}: Attempt {attempt + 1} failed - {e}")
                
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    sleep_time = 0.1 * (2 ** attempt)
                    time.sleep(sleep_time)
        
        # Todos los reintentos fallaron
        logger.error(f"{self.service_name}: All {self.max_retries} attempts failed")
        return self._get_fallback(payload, last_exception)
    
    def _execute_with_timeout(
        self,
        service_func: Callable,
        payload: Dict[str, Any],
        timeout: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Ejecuta función con timeout (simplificado para demo)"""
        # En producción: usar concurrent.futures.ThreadPoolExecutor con timeout
        return service_func(payload, **kwargs)
    
    def _get_fallback(self, payload: Dict[str, Any], exception: Optional[Exception] = None) -> Dict[str, Any]:
        """Obtiene respuesta de fallback según el servicio"""
        fallback_func = self.fallback_strategies.get(self.service_name)
        
        if fallback_func:
            logger.info(f"{self.service_name}: Using fallback strategy")
            return fallback_func(payload, exception)
        
        # Fallback genérico
        return {
            "status": "fallback",
            "service": self.service_name,
            "error": str(exception) if exception else "Circuit breaker open",
            "payload": payload
        }
    
    # Estrategias de fallback específicas por servicio
    
    def _fallback_embedding(self, payload: Dict[str, Any], exception: Optional[Exception]) -> Dict[str, Any]:
        """Fallback para probe_llm: embedding zero o cached"""
        logger.warning("probe_llm fallback: returning zero embedding")
        return {
            "embedding": [0.0] * 768,
            "metadata": {
                "length": len(payload.get("text", "")),
                "words": len(payload.get("text", "").split()),
                "language": "unknown",
                "sentiment": 0.0,
                "is_question": False,
                "topic_hint": "fallback"
            },
            "status": "fallback"
        }
    
    def _fallback_tensor(self, payload: Dict[str, Any], exception: Optional[Exception]) -> Dict[str, Any]:
        """Fallback para ffe_encoder: tensor neutral"""
        logger.warning("ffe_encoder fallback: returning neutral tensor")
        return {
            "ffe_tensor": {
                "level_1": [3, 3, 3],
                "level_2": [[3, 3, 3]] * 3,
                "level_3": [[[3, 3, 3]] * 3] * 3,
                "flat": [3] * 39,
                "hash": "fallback_neutral"
            },
            "status": "fallback"
        }
    
    def _fallback_synthesis(self, payload: Dict[str, Any], exception: Optional[Exception]) -> Dict[str, Any]:
        """Fallback para transcender: síntesis vacía"""
        logger.warning("transcender fallback: returning empty synthesis")
        return {
            "Ms": [None, None, None],
            "Ss": [None, None, None],
            "MetaM": [[None, None, None]] * 4,
            "C_meta": 0.0,
            "hash": "fallback_synthesis",
            "status": "fallback"
        }
    
    def _fallback_evolution(self, payload: Dict[str, Any], exception: Optional[Exception]) -> Dict[str, Any]:
        """Fallback para evolver: skip evolution"""
        logger.warning("evolver fallback: skipping evolution update")
        return {
            "archetypes": {"new_patterns": 0, "total_archetypes": 0},
            "relations": {"new_relations": 0, "total_relations": 0},
            "dynamics": {"delta_Cdyn": 0.0, "trend": "unknown"},
            "status": "fallback"
        }
    
    def get_health(self) -> Dict[str, Any]:
        """Estado de salud del cliente"""
        circuit_state = self.circuit.get_state()
        return {
            "service": self.service_name,
            "circuit_breaker": circuit_state,
            "max_retries": self.max_retries,
            "base_timeout": self.base_timeout
        }


# Factory para crear clientes resilientes
def create_resilient_clients() -> Dict[str, ResilientMCPClient]:
    """
    Crea clientes resilientes para todos los servicios MCP.
    
    Returns:
        Dict de clientes por nombre de servicio
    """
    # Configuraciones específicas por servicio
    configs = {
        "probe_llm": CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=30.0,
            timeout=2.0
        ),
        "ffe_encoder": CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=20.0,
            timeout=1.0
        ),
        "transcender": CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=15.0,
            timeout=0.5
        ),
        "evolver": CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=60.0,
            timeout=2.0
        )
    }
    
    clients = {}
    for service_name, config in configs.items():
        clients[service_name] = ResilientMCPClient(
            service_name=service_name,
            max_retries=3,
            base_timeout=config.timeout,
            circuit_config=config
        )
    
    logger.info(f"Created {len(clients)} resilient MCP clients")
    return clients


if __name__ == "__main__":
    # Demo de uso
    print("🔌 Resilient MCP Client Demo\n")
    
    # Crear clientes
    clients = create_resilient_clients()
    
    # Simular llamadas
    def mock_service_success(payload):
        return {"status": "ok", "result": "success"}
    
    def mock_service_failure(payload):
        raise Exception("Service temporarily unavailable")
    
    # Test con éxito
    print("1. Test exitoso:")
    client = clients["probe_llm"]
    result = client.call_service(mock_service_success, {"text": "test"})
    print(f"   Result: {result}")
    print(f"   Health: {client.get_health()}\n")
    
    # Test con fallos (activa circuit breaker)
    print("2. Test con fallos (activando circuit breaker):")
    for i in range(6):
        try:
            result = client.call_service(mock_service_failure, {"text": f"test_{i}"})
            print(f"   Attempt {i+1}: {result.get('status')}")
        except Exception as e:
            print(f"   Attempt {i+1}: Failed - {e}")
    
    print(f"\n   Final health: {client.get_health()}\n")
    
    print("✅ Demo completed")
