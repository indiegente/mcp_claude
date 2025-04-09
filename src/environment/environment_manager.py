from typing import Dict
from ..utils import Logger, PathResolver
from .env_file_handler import EnvFileHandler

class EnvironmentManager:
    """
    Gestiona las variables de entorno y archivos de configuración.
    Single Responsibility: Manejar la configuración del entorno.
    """
    def __init__(self):
        self.logger = Logger()
        self.path_resolver = PathResolver()
        self.env_handler = EnvFileHandler()

    async def configure(self, repo_config: Dict):
        """Configura el entorno para un repositorio."""
        repo_path = self.path_resolver.get_repo_path(repo_config['name'])
        await self.env_handler.setup_env_file(repo_path, repo_config)
        await self._verify_required_env_vars(repo_config) 