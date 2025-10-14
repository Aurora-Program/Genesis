"""
MCP Server: FFE Store
Servidor de almacenamiento para tensores fractales FFE en la Knowledge Base.

Protocolo MCP: https://modelcontextprotocol.io/
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class FFEStore:
    """
    Knowledge Base fractal para almacenar tensores FFE.
    
    Tabla principal:
    - id: Identificador único
    - tensor_data: JSON con estructura {3,9,27}
    - synthesis_data: JSON con Ms, Ss, MetaM
    - metadata: JSON con información contextual
    - timestamp: Momento de creación
    """
    
    def __init__(self, db_path: str = "data/ffe_knowledge_base.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tensors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tensor_data TEXT NOT NULL,
                synthesis_data TEXT,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archetypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_key TEXT UNIQUE NOT NULL,
                frequency INTEGER DEFAULT 1,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON tensors(timestamp)
        """)
        
        conn.commit()
        conn.close()
    
    def store_tensor(
        self, 
        tensor_dict: Dict, 
        synthesis: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Almacena un tensor fractal en la KB.
        
        Args:
            tensor_dict: Dict con level_3, level_9, level_27
            synthesis: Dict con Ms, Ss, MetaM (opcional)
            metadata: Información adicional (opcional)
            
        Returns:
            ID del tensor almacenado
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tensors (tensor_data, synthesis_data, metadata)
            VALUES (?, ?, ?)
        """, (
            json.dumps(tensor_dict),
            json.dumps(synthesis) if synthesis else None,
            json.dumps(metadata) if metadata else None
        ))
        
        tensor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return tensor_id
    
    def get_tensor(self, tensor_id: int) -> Optional[Dict]:
        """Recupera un tensor por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, tensor_data, synthesis_data, metadata, timestamp
            FROM tensors WHERE id = ?
        """, (tensor_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "id": row[0],
            "tensor": json.loads(row[1]),
            "synthesis": json.loads(row[2]) if row[2] else None,
            "metadata": json.loads(row[3]) if row[3] else None,
            "timestamp": row[4]
        }
    
    def query_recent(self, limit: int = 10) -> List[Dict]:
        """Recupera los últimos N tensores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, tensor_data, synthesis_data, metadata, timestamp
            FROM tensors
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "tensor": json.loads(row[1]),
                "synthesis": json.loads(row[2]) if row[2] else None,
                "metadata": json.loads(row[3]) if row[3] else None,
                "timestamp": row[4]
            }
            for row in rows
        ]
    
    def store_archetype(self, pattern_key: str) -> int:
        """
        Almacena o actualiza un arquetipo.
        
        Args:
            pattern_key: Clave del patrón (e.g., tuple de Ms)
            
        Returns:
            ID del arquetipo
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Intentar actualizar si existe
        cursor.execute("""
            UPDATE archetypes
            SET frequency = frequency + 1, last_seen = CURRENT_TIMESTAMP
            WHERE pattern_key = ?
        """, (pattern_key,))
        
        if cursor.rowcount == 0:
            # Insertar nuevo
            cursor.execute("""
                INSERT INTO archetypes (pattern_key)
                VALUES (?)
            """, (pattern_key,))
        
        archetype_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return archetype_id
    
    def get_top_archetypes(self, limit: int = 10) -> List[Dict]:
        """Recupera los arquetipos más frecuentes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, pattern_key, frequency, first_seen, last_seen
            FROM archetypes
            ORDER BY frequency DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "pattern": row[1],
                "frequency": row[2],
                "first_seen": row[3],
                "last_seen": row[4]
            }
            for row in rows
        ]
    
    def get_stats(self) -> Dict:
        """Estadísticas de la Knowledge Base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tensors")
        total_tensors = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM archetypes")
        total_archetypes = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT SUM(frequency) FROM archetypes
        """)
        total_pattern_occurrences = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_tensors": total_tensors,
            "total_archetypes": total_archetypes,
            "total_pattern_occurrences": total_pattern_occurrences,
            "db_path": str(self.db_path)
        }


# ========== MCP SERVER INTERFACE ==========
# TODO: Implementar interfaz MCP cuando se integre con Claude/VS Code
# Ver: https://modelcontextprotocol.io/docs

class FFEStoreMCPServer:
    """
    Interfaz MCP para FFE Store.
    Expone herramientas para que LLMs interactúen con la KB.
    """
    
    def __init__(self):
        self.store = FFEStore()
    
    def get_tools(self) -> List[Dict]:
        """Define las herramientas MCP disponibles"""
        return [
            {
                "name": "ffe_store_tensor",
                "description": "Almacena un tensor fractal FFE en la Knowledge Base",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tensor": {"type": "object"},
                        "synthesis": {"type": "object"},
                        "metadata": {"type": "object"}
                    },
                    "required": ["tensor"]
                }
            },
            {
                "name": "ffe_query_recent",
                "description": "Recupera los últimos tensores almacenados",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "default": 10}
                    }
                }
            },
            {
                "name": "ffe_get_stats",
                "description": "Obtiene estadísticas de la Knowledge Base",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    def call_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Ejecuta una herramienta MCP"""
        if tool_name == "ffe_store_tensor":
            tensor_id = self.store.store_tensor(
                arguments["tensor"],
                arguments.get("synthesis"),
                arguments.get("metadata")
            )
            return {"success": True, "tensor_id": tensor_id}
        
        elif tool_name == "ffe_query_recent":
            tensors = self.store.query_recent(arguments.get("limit", 10))
            return {"success": True, "tensors": tensors}
        
        elif tool_name == "ffe_get_stats":
            stats = self.store.get_stats()
            return {"success": True, "stats": stats}
        
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}


# ========== DEMO ==========
if __name__ == "__main__":
    print("🗄️ FFE Store - Knowledge Base Fractal\n")
    
    # Crear store
    store = FFEStore("data/test_ffe_kb.db")
    
    # Almacenar tensores de prueba
    print("=== Almacenando tensores de prueba ===")
    for i in range(5):
        tensor_dict = {
            "level_3": [i % 8, (i+1) % 8, (i+2) % 8],
            "level_9": [[j % 8 for j in range(3)] for _ in range(3)],
            "level_27": [[[k % 8 for k in range(3)] for _ in range(3)] for _ in range(3)]
        }
        synthesis = {
            "Ms": [(i+j) % 2 for j in range(3)],
            "Ss": [i % 2, (i+1) % 2, (i+2) % 2]
        }
        metadata = {"test_id": i, "source": "demo"}
        
        tensor_id = store.store_tensor(tensor_dict, synthesis, metadata)
        print(f"  ✓ Tensor {i} almacenado con ID: {tensor_id}")
    
    # Almacenar arquetipos
    print("\n=== Almacenando arquetipos ===")
    patterns = ["(0,1,0)", "(1,0,1)", "(0,1,0)", "(1,1,0)", "(0,1,0)"]
    for pattern in patterns:
        store.store_archetype(pattern)
    print(f"  ✓ {len(set(patterns))} arquetipos únicos registrados")
    
    # Consultar estadísticas
    print("\n=== Estadísticas ===")
    stats = store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Consultar tensores recientes
    print("\n=== Últimos 3 tensores ===")
    recent = store.query_recent(3)
    for tensor in recent:
        print(f"  ID {tensor['id']}: level_3={tensor['tensor']['level_3']}, metadata={tensor['metadata']}")
    
    # Consultar top arquetipos
    print("\n=== Top arquetipos ===")
    top = store.get_top_archetypes(5)
    for arch in top:
        print(f"  {arch['pattern']}: frecuencia={arch['frequency']}")
