#!/usr/bin/env python3
import asyncio
import os
import sys
import subprocess
from src.mcp_manager import MCPManager

def check_dependencies():
    """Verifica que todas las dependencias necesarias estén instaladas."""
    required_commands = {
        'git': 'git --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'python': 'python --version'
    }
    missing = []
    
    for cmd, check_cmd in required_commands.items():
        try:
            # Intentar ejecutar el comando completo
            result = subprocess.run(check_cmd.split(), 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 shell=True,
                                 check=True)
            # Si llegamos aquí, el comando existe
            print(f"{cmd} encontrado: {result.stdout.decode().strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(cmd)
            
    if missing:
        print("\nError: Las siguientes dependencias no están instaladas:")
        for cmd in missing:
            print(f"- {cmd}")
        print("\nPor favor, ejecuta el script de instalación de dependencias:")
        print(".\scripts\install_dependencies.ps1")
        return False
    return True

async def main():
    try:
        # Verificar dependencias
        if not check_dependencies():
            return 1
            
        # Ruta al archivo de configuración
        config_path = "config/repositories.json"
        
        # Crear instancia del MCPManager
        manager = MCPManager(config_path)
        
        # Configurar todos los MCPs
        await manager.setup_all_mcps()
        
    except Exception as e:
        print(f"Error durante la configuración: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 