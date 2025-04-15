import os
import json
import asyncio
import subprocess
import time
from typing import Dict
from ..interfaces.mcp_interface import MCPInterface

class BaseMCP(MCPInterface):
    """Clase base que implementa funcionalidades comunes para todos los MCPs."""
    
    def __init__(self, name: str):
        self.name = name
        
    def create_env_file(self, path: str, env_vars: Dict):
        """Crea el archivo .env con las variables de entorno."""
        env_path = os.path.join(path, '.env')
        with open(env_path, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
                
    async def run_command(self, command: str) -> bool:
        """Ejecuta un comando en la terminal y muestra la salida en tiempo real."""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    
            stderr = process.stderr.read()
            if stderr:
                print(f"Error: {stderr}")
                
            return process.returncode == 0
            
        except Exception as e:
            print(f"Error ejecutando comando: {str(e)}")
            return False
            
    def clean_file(self, file_path: str):
        """Limpia un archivo de caracteres especiales."""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                content = content.strip()
                
                if file_path.endswith('.json'):
                    if content.startswith('@"'):
                        content = content[2:]
                    if content.startswith('@'):
                        content = content[1:]
                    if '"@ | Out-File -FilePath' in content:
                        content = content.split('"@ | Out-File -FilePath')[0]
                    if content.endswith('"@'):
                        content = content[:-2]
                    if not content.strip().startswith('{'):
                        content = content[content.find('{'):]
                    if not content.strip().endswith('}'):
                        content = content[:content.rfind('}')+1]
                        
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"Error al limpiar {os.path.basename(file_path)}: {str(e)}")
                
    async def verify_server(self, path: str) -> bool:
        """Verifica que el servidor funcione correctamente."""
        try:
            process = subprocess.Popen(
                "npm start",
                cwd=path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            time.sleep(2)
            
            if process.poll() is None:
                print("Servidor iniciado correctamente!")
                print("Consejo: Para ver la salida completa del servidor, ejecuta 'npm start' en el CMD")
                
                try:
                    process.terminate()
                    time.sleep(1)
                    if process.poll() is None:
                        process.kill()
                    time.sleep(1)
                except Exception:
                    pass
                    
                return True
            else:
                print("Error: El servidor no pudo iniciar correctamente")
                return False
                
        except Exception as e:
            print(f"Error al verificar el servidor: {str(e)}")
            return False 