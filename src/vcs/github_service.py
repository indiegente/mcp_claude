from typing import Optional
from ..utils import Logger, CommandRunner

class GithubService:
    """
    Maneja la interacción con GitHub.
    Single Responsibility: Gestionar la autenticación y operaciones de GitHub.
    """
    def __init__(self):
        self.logger = Logger()
        self.command_runner = CommandRunner()
        self.token: Optional[str] = None

    async def configure(self):
        """Configura la autenticación de GitHub."""
        self.token = await self._get_token()
        await self._verify_token()
        await self._configure_git()

    async def get_clone_url(self, repo_url: str) -> str:
        """Retorna la URL de clonado con autenticación."""
        if not self.token:
            await self.configure()
        return repo_url.replace(
            'https://github.com',
            f'https://{self.token}@github.com'
        ) 