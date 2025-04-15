import os
import json
import asyncio
from typing import Dict, List
from .mcps.trello.trello_mcp import TrelloMCP
from .mcps.google_calendar.google_calendar_mcp import GoogleCalendarMCP

class MCPManager:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.base_path = self.config['base_path']
        self.mcp_handlers = {
            'trello': TrelloMCP(),
            'google-calendar': GoogleCalendarMCP()
        }
        
    def load_config(self, config_path: str) -> Dict:
        """Carga la configuración desde el archivo JSON."""
        with open(config_path, 'r') as f:
            return json.load(f)
            
    async def setup_all_mcps(self):
        """Configura todos los MCPs listados en la configuración."""
        # Crear directorio base si no existe
        os.makedirs(self.base_path, exist_ok=True)
        
        # Lista para guardar los MCPs instalados
        installed_mcps = []
        failed_mcps = []
        
        # Configurar cada MCP secuencialmente
        for repo in self.config['repositories']:
            try:
                # 1. Extraer información del repositorio
                repo_name = repo['url'].split('/')[-1].replace('.git', '')
                target_path = os.path.join(self.base_path, repo_name)
                
                # 2. Verificar si ya está configurado
                if os.path.exists(target_path):
                    print(f"MCP {repo_name} ya está configurado. Saltando...")
                    installed_mcps.append(repo_name)
                    continue
                
                print(f"\nConfigurando MCP en: {target_path}")
                
                # 3. Clonar repositorio
                print(f"Clonando repositorio: {repo['url']}")
                if not await self.clone_repository(repo['url'], target_path):
                    print(f"Error al clonar el repositorio {repo_name}. Saltando...")
                    failed_mcps.append(repo_name)
                    continue
                
                # 4. Verificar si el repositorio tiene una subcarpeta con el mismo nombre
                subfolder_path = os.path.join(target_path, repo_name)
                if os.path.exists(subfolder_path):
                    print(f"Configurando en subcarpeta: {subfolder_path}")
                    target_path = subfolder_path
                
                # 5. Determinar el tipo de MCP y configurarlo
                mcp_type = None
                if 'trello' in repo_name.lower():
                    mcp_type = 'trello'
                elif 'google-calendar' in repo_name.lower():
                    mcp_type = 'google-calendar'
                
                if mcp_type and mcp_type in self.mcp_handlers:
                    print(f"\nConfigurando MCP de {mcp_type}...")
                    if await self.mcp_handlers[mcp_type].setup(target_path, repo.get('env_vars', {})):
                        installed_mcps.append(repo_name)
                    else:
                        failed_mcps.append(repo_name)
                else:
                    print(f"No se pudo determinar el tipo de MCP para {repo_name}")
                    failed_mcps.append(repo_name)
                    
            except Exception as e:
                print(f"Error configurando MCP {repo_name}: {str(e)}")
                failed_mcps.append(repo_name)
                continue
                
        # Mostrar resumen de MCPs instalados
        if installed_mcps:
            print("\n=== Resumen de MCPs instalados ===")
            for mcp in installed_mcps:
                print(f"- {mcp}")
            print("================================")
            
            # Mostrar MCPs que fallaron
            if failed_mcps:
                print("\n=== MCPs que fallaron ===")
                for mcp in failed_mcps:
                    print(f"- {mcp}")
                print("================================")
                print("\nNo se actualizará el archivo de configuración hasta que todos los MCPs se configuren correctamente.")
            else:
                print("\nTodas las MCPs se han configurado correctamente.")
                print("Actualizando archivo de configuración para Claude Desktop...")
                self.create_claude_desktop_config(installed_mcps)
                
    async def clone_repository(self, url: str, path: str) -> bool:
        """Clona un repositorio Git."""
        try:
            if os.path.exists(path):
                print(f"El directorio {path} ya existe. Saltando clonación...")
                return True
                
            command = f"git clone {url} {path}"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_message = stderr.decode().strip()
                if "already exists" in error_message:
                    print(f"El repositorio ya existe en {path}")
                    return True
                else:
                    print(f"Error al clonar el repositorio: {error_message}")
                    return False
                    
            output = stdout.decode().strip()
            if output:
                print(output)
                
            return True
            
        except Exception as e:
            print(f"Error al clonar el repositorio: {str(e)}")
            return False
            
    def create_claude_desktop_config(self, installed_mcps: List[str]):
        """Crea o actualiza el archivo de configuración para Claude Desktop."""
        try:
            config = {
                "mcpServers": {}
            }
            
            for mcp_name in installed_mcps:
                mcp_path = os.path.join(self.base_path, mcp_name)
                
                # Verificar si existe una subcarpeta con el mismo nombre
                subfolder_path = os.path.join(mcp_path, mcp_name)
                if os.path.exists(subfolder_path):
                    mcp_path = subfolder_path
                
                # Determinar el tipo de MCP
                mcp_type = None
                if 'trello' in mcp_name.lower():
                    mcp_type = 'trello'
                elif 'google-calendar' in mcp_name.lower():
                    mcp_type = 'google-calendar'
                
                if mcp_type and mcp_type in self.mcp_handlers:
                    mcp_config = self.mcp_handlers[mcp_type].get_config()
                    mcp_config['args'][0] = os.path.join(mcp_path, mcp_config['args'][0]).replace("\\", "/")
                    
                    # Obtener las variables de entorno del repositorio
                    for repo in self.config['repositories']:
                        repo_name = repo['url'].split('/')[-1].replace('.git', '')
                        if repo_name == mcp_name and 'env_vars' in repo:
                            mcp_config['env'] = repo['env_vars']
                            break
                    
                    config["mcpServers"][mcp_type] = mcp_config
            
            # Obtener la ruta del directorio actual del script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir un nivel para llegar a la raíz del proyecto
            project_root = os.path.dirname(current_dir)
            # Definir la ruta del archivo de configuración
            config_path = os.path.join(project_root, "claude_desktop_config.json")
            
            # Asegurarse de que el directorio existe
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Crear o actualizar el archivo
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            # Verificar que el archivo se creó correctamente
            if os.path.exists(config_path):
                print("Archivo de configuración creado exitosamente.")
                print("\nPor favor, copia el archivo 'claude_desktop_config.json' en donde tengas instalado Claude Desktop")
            else:
                print("Error: No se pudo crear el archivo de configuración.")
                
        except Exception as e:
            print(f"Error al crear/actualizar el archivo de configuración: {str(e)}") 