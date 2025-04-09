import asyncio
from typing import Optional
from .logger import Logger

class CommandRunner:
    """
    Ejecuta comandos del sistema.
    Single Responsibility: Manejar la ejecución de comandos.
    """
    def __init__(self):
        self.logger = Logger()

    async def run(self, command: str, cwd: Optional[str] = None) -> str:
        """Ejecuta un comando y retorna su salida."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise RuntimeError(f"Command failed: {stderr.decode()}")
            
            return stdout.decode()
        except Exception as e:
            self.logger.error(f"Error running command '{command}': {str(e)}")
            raise 