import os
import json
from typing import Dict
from ...core.base_mcp import BaseMCP

class TrelloMCP(BaseMCP):
    """Implementación específica para el MCP de Trello."""
    
    def __init__(self):
        super().__init__("trello")
        
    async def setup(self, path: str, env_vars: Dict) -> bool:
        """Configura el MCP de Trello."""
        try:
            # 1. Verificar y modificar package.json
            package_json_path = os.path.join(path, 'package.json')
            if os.path.exists(package_json_path):
                with open(package_json_path, 'r') as f:
                    package_json = json.load(f)
                
                if 'scripts' in package_json and 'build' in package_json['scripts']:
                    package_json['scripts']['build'] = 'tsc'
                    with open(package_json_path, 'w') as f:
                        json.dump(package_json, f, indent=2)
                    print("Script de build modificado para Windows")
            
            # 2. Crear archivo .env
            self.create_env_file(path, env_vars)
            print(f"Creando archivo .env en: {os.path.join(path, '.env')}")
            
            # 3. Instalar dependencias incluyendo dotenv
            print("Instalando dependencias del proyecto MCP...")
            await self.run_command(f"cd {path} && npm install dotenv")
            await self.run_command(f"cd {path} && npm install")
            
            # 4. Ejecutar build
            print("Compilando el proyecto...")
            await self.run_command(f"cd {path} && npm run build")
            
            # 5. Agregar configuración de dotenv en index.js
            index_js_path = os.path.join(path, 'build', 'index.js')
            if os.path.exists(index_js_path):
                with open(index_js_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'import dotenv from' not in content:
                    if '#!/usr/bin/env node' in content:
                        content = content.replace('#!/usr/bin/env node', '#!/usr/bin/env node\nimport dotenv from \'dotenv\';\ndotenv.config();')
                    else:
                        content = "#!/usr/bin/env node\nimport dotenv from 'dotenv';\ndotenv.config();\n\n" + content
                    
                    with open(index_js_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print("Configuración de dotenv agregada en index.js")
            
            # 6. Verificar que el servidor funcione
            return await self.verify_server(path)
            
        except Exception as e:
            print(f"Error configurando Trello: {str(e)}")
            return False
            
    def get_config(self) -> Dict:
        """Obtiene la configuración específica de Trello para Claude Desktop."""
        return {
            "command": "node",
            "args": ["build/index.js"],
            "env": {
                "TRELLO_API_KEY": "",
                "TRELLO_TOKEN": "",
                "TRELLO_BOARD_ID": ""
            }
        } 