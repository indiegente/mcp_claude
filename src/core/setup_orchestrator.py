from typing import List
from ..config import ConfigManager
from ..vcs import RepositoryManager
from ..package_managers import PackageManagerFactory
from ..environment import EnvironmentManager
from ..testing import TestRunner
from ..utils import Logger

class SetupOrchestrator:
    """
    Clase principal que orquesta el proceso de configuración.
    Single Responsibility: Coordinar el flujo de configuración.
    """
    def __init__(self):
        self.config_manager = ConfigManager()
        self.repo_manager = RepositoryManager()
        self.package_manager_factory = PackageManagerFactory()
        self.env_manager = EnvironmentManager()
        self.test_runner = TestRunner()
        self.logger = Logger()

    async def setup(self):
        """Ejecuta el proceso de configuración completo."""
        try:
            await self.config_manager.load()
            await self.repo_manager.initialize()
            await self.setup_repositories()
            await self.configure_claude_desktop()
            self.logger.info("Setup completed successfully!")
        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            raise

    async def setup_repositories(self):
        """Configura todos los repositorios definidos."""
        repos = self.config_manager.get_repositories()
        for repo in repos:
            await self.setup_single_repository(repo)

    async def setup_single_repository(self, repo_config: dict):
        """Configura un repositorio individual."""
        try:
            await self.repo_manager.clone_or_update(repo_config)
            package_manager = self.package_manager_factory.create(repo_config['type'])
            await package_manager.install_dependencies(repo_config)
            await self.env_manager.configure(repo_config)
            await self.test_runner.run(repo_config)
        except Exception as e:
            self.logger.error(f"Failed to setup {repo_config['name']}: {str(e)}")
            raise 