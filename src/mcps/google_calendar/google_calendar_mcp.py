import os
import json
import re
from typing import Dict
from ...core.base_mcp import BaseMCP

class GoogleCalendarMCP(BaseMCP):
    """Implementación específica para el MCP de Google Calendar."""
    
    def __init__(self):
        super().__init__("google-calendar")
        
    async def setup(self, path: str, env_vars: Dict) -> bool:
        """Configura el MCP de Google Calendar."""
        try:
            # 1. Limpiar archivos necesarios
            print("Limpiando archivos...")
            package_path = os.path.join(path, 'package.json')
            auth_path    = os.path.join(path, 'auth.js')
            index_path   = os.path.join(path, 'index.js')
            
            for file_path, name in {
                package_path: "package.json",
                auth_path:    "auth.js",
                index_path:   "index.js"
            }.items():
                if os.path.exists(file_path):
                    self.clean_file(file_path)
                    print(f"Archivo limpiado: {name}")
            
            # 2. Instalar dependencias
            print("\nInstalando dependencias del proyecto MCP...")
            await self.run_command(f"cd {path} && npm install")
            
            # 3. Verificar credenciales básicas
            required = ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET']
            missing = [v for v in required if v not in env_vars]
            empty   = [v for v in required if v in env_vars and not env_vars[v].strip()]
            
            if missing:
                print(f"Faltan variables de entorno: {', '.join(missing)}")
                print("Configura las credenciales en repositories.json y vuelve a ejecutar.")
                return False
            if empty:
                print(f"Variables vacías: {', '.join(empty)}")
                print("Configura las credenciales en repositories.json y vuelve a ejecutar.")
                return False
            
            # 4. Manejo del refresh token
            if env_vars.get('GOOGLE_REFRESH_TOKEN', '').strip():
                print("\nRefresh token encontrado, configurando...")
                self.create_env_file(path, env_vars)
                print(f"Creando archivo .env en: {os.path.join(path, '.env')}")
                
                # Leer y actualizar index.js
                if os.path.exists(index_path):
                    with open(index_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Prepend dotenv si falta
                    if "import { config } from 'dotenv';" not in content:
                        content = "import { config } from 'dotenv';\nconfig();\n" + content
                    
                    # Sustituir placeholder de refresh_token
                    content = re.sub(
                        r'refresh_token:\s*"YOUR_REFRESH_TOKEN_HERE"',
                        'refresh_token: ""',
                        content
                    )
                    content = re.sub(
                        r'refresh_token:\s*""',
                        f'refresh_token: "{env_vars["GOOGLE_REFRESH_TOKEN"]}"',
                        content
                    )
                    
                    # Escribir cambios y limpiar/reordenar
                    with open(index_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print("Token de actualización establecido en index.js")
                    self.clean_file(index_path)
                
                # 5. Verificar que el servidor funcione
                return await self.verify_server(path)
            
            else:
                print("\nNo se encontró refresh token.")
                print("Pasos a seguir:")
                print(" 1. npm run auth")
                print(" 2. Completa la autenticación")
                print(" 3. Copia el refresh token generado")
                print(" 4. Actualiza repositories.json")
                print(" 5. Elimina la carpeta del MCP y vuelve a setup")
                return False
                
        except Exception as e:
            print(f"Error configurando Google Calendar: {e}")
            return False
            
    def get_config(self) -> Dict:
        """Obtiene la configuración específica de Google Calendar para Claude Desktop."""
        return {
            "command": "node",
            "args":    ["index.js"],
            "env": {
                "GOOGLE_CLIENT_ID":     "",
                "GOOGLE_CLIENT_SECRET": "",
                "GOOGLE_REFRESH_TOKEN": ""
            }
        }

    def clean_file(self, file_path: str) -> None:
        """Limpia el contenido de package.json, auth.js o index.js de formato PowerShell
        y reordena index.js para que comience con shebang + dotenv."""
        try:
            if not os.path.exists(file_path):
                return
            name = os.path.basename(file_path)
            
            # Leer contenido
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1) Eliminar wrapper de PowerShell here-string si existe
            if content.startswith('@"\n') and '"@ | Out-File' in content:
                # Extraer entre @"\n y "@ | Out-File
                body = content.split('@"\n', 1)[1].split('"@ | Out-File', 1)[0]
                content = body.strip('\r\n') + '\n'
            
            # 2) Si es index.js, además reordenar
            if name == "index.js":
                lines = [ln for ln in content.split('\n') if ln.strip()]
                
                shebang_line  = None
                dotenv_import = None
                dotenv_config = None
                others        = []
                
                for ln in lines:
                    s = ln.strip()
                    if s == '#!/usr/bin/env node':
                        shebang_line = ln
                    elif s == "import { config } from 'dotenv';":
                        dotenv_import = ln
                    elif s == 'config();':
                        dotenv_config = ln
                    else:
                        others.append(ln)
                
                # Reconstruir en el orden:
                #   1) shebang
                #   2) import dotenv
                #   3) config()
                #   4) dos líneas en blanco
                #   5) resto
                new = []
                if shebang_line:
                    new.append(shebang_line)
                if dotenv_import:
                    new.append(dotenv_import)
                if dotenv_config:
                    new.append(dotenv_config)
                new.append('')
                new.append('')
                new.extend(others)
                
                content = '\n'.join(new) + '\n'
            
            # 3) Escribir de vuelta
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        except Exception as e:
            print(f"Error limpiando archivo {name}: {e}")
            raise
