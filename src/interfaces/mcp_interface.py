from abc import ABC, abstractmethod
from typing import Dict, Optional

class MCPInterface(ABC):
    """Interfaz base para todos los MCPs."""
    
    @abstractmethod
    async def setup(self, path: str, env_vars: Dict) -> bool:
        """Configura el MCP con las variables de entorno proporcionadas."""
        pass
    
    @abstractmethod
    async def verify_server(self, path: str) -> bool:
        """Verifica que el servidor del MCP funcione correctamente."""
        pass
    
    @abstractmethod
    def get_config(self) -> Dict:
        """Obtiene la configuración específica del MCP para Claude Desktop."""
        pass 