from typing import Dict, Type
from .node_manager import NodePackageManager
from .python_manager import PythonPackageManager
from ..utils import Logger

class PackageManagerFactory:
    """
    Factory para crear gestores de paquetes.
    Open/Closed Principle: Fácil de extender para nuevos tipos de paquetes.
    """
    def __init__(self):
        self.logger = Logger()
        self.managers: Dict[str, Type] = {
            'node': NodePackageManager,
            'python': PythonPackageManager
        }

    def create(self, repo_type: str):
        """Crea una instancia del gestor de paquetes apropiado."""
        manager_class = self.managers.get(repo_type.lower())
        if not manager_class:
            raise ValueError(f"Unsupported repository type: {repo_type}")
        return manager_class() 