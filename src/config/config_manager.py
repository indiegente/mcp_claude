from typing import Dict, Any
from ..utils import Logger
from .config_loader import ConfigLoader

class ConfigManager:
    """
    Gestiona la configuración del sistema.
    Single Responsibility: Manejar la configuración.
    """
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.logger = Logger()
        self.config: Dict[str, Any] = {}

    async def load(self):
        """Carga todas las configuraciones necesarias."""
        self.config = await self.config_loader.load_all()

    def get_repositories(self):
        """Retorna la lista de repositorios configurados."""
        return self.config.get('repositories', [])

    def get_claude_config_path(self):
        """Retorna la ruta de configuración de Claude Desktop."""
        return self.config.get('claude_config_path') 