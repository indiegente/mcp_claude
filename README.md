# MCP Setup Tool

Una herramienta multiplataforma para automatizar la configuración del entorno de desarrollo para los repositorios MCP (Model-Claude-Protocol) que se integran con Claude Desktop.

## 📋 Tabla de Contenidos

- [Prerrequisitos](#prerrequisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Solución de Problemas](#solución-de-problemas)
- [Contribuir](#contribuir)

## 🔧 Prerrequisitos

### Requisitos Mínimos del Sistema

#### Para Windows
- Windows 10 o superior
- PowerShell 5.0 o superior
- Permisos de administrador
- Conexión a Internet

#### Para macOS
- macOS 10.15 (Catalina) o superior
- Terminal
- Permisos de administrador
- Conexión a Internet

### Nota sobre la Instalación Automática
Los siguientes componentes se instalarán automáticamente mediante los scripts de instalación:
- Python 3.10 o superior
- Node.js 18.0.0 o superior
- Git
- Homebrew (macOS)
- Command Line Tools (macOS)
- Chocolatey (Windows)

Si ya tienes instalados algunos de estos componentes, los scripts verificarán las versiones y solo actualizarán si es necesario.

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/your-org/mcp-setup.git
cd mcp-setup
```

2. Ejecutar el script de instalación de dependencias según tu sistema operativo:

```bash
# Windows (ejecutar PowerShell como administrador)
.\scripts\install_dependencies.ps1

# macOS/Linux
chmod +x ./scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

Este paso instalará:
- Python 3.10 o superior
- Node.js 18.0.0 o superior
- Git
- Homebrew (solo macOS)
- Command Line Tools (solo macOS)
- Chocolatey (solo Windows)

3. Verificar la instalación:
```bash
# Verificar Python
python --version  # Windows
python3 --version  # macOS/Linux

# Verificar Node.js
node --version

# Verificar Git
git --version
```

4. Crear y activar un entorno virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

5. Instalar dependencias de Python:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. Configurar el archivo `config/repositories.json`:
```json
{
    "base_path": "/path/to/your/mcp/servers",
    "repositories": [
        {
            "url": "https://github.com/your-org/mcp-server-trello.git",
            "env_vars": {
                "TRELLO_API_KEY": "your-api-key",
                "TRELLO_TOKEN": "your-token",
                "TRELLO_BOARD_ID": "your-board-id"
            }
        },
        {
            "url": "https://github.com/your-org/mcp-google-calendar.git",
            "env_vars": {
                "GOOGLE_CLIENT_ID": "your-client-id",
                "GOOGLE_CLIENT_SECRET": "your-client-secret",
                "GOOGLE_REFRESH_TOKEN": "your-refresh-token"
            }
        }
    ]
}
```

2. Configurar las variables de entorno necesarias para cada MCP:
   - Para Trello: API Key, Token y Board ID
   - Para Google Calendar: Client ID, Client Secret y Refresh Token

## 🛠️ Uso

1. Iniciar el setup:
```bash
python -m setup
```

2. Seguir las instrucciones para cada MCP:
   - Para Trello: Se configurará automáticamente con las credenciales proporcionadas
   - Para Google Calendar: 
     - Se creará un archivo `.env` con las credenciales
     - Se configurará el refresh token en `index.js`
     - Si no hay refresh token, se guiará al usuario para obtenerlo

## 📁 Estructura del Proyecto

```
mcp-setup/
├── config/
│   ├── default.properties
│   └── repositories.json
├── scripts/
│   ├── install_dependencies.ps1
│   └── install_dependencies.sh
├── src/
│   ├── core/
│   │   ├── base_mcp.py
│   │   └── setup_orchestrator.py
│   ├── mcps/
│   │   ├── google_calendar/
│   │   │   └── google_calendar_mcp.py
│   │   └── trello/
│   │       └── trello_mcp.py
│   └── utils/
│       └── file_utils.py
├── requirements.txt
└── README.md
```

## 🔍 Solución de Problemas

### Problemas Comunes

1. **Error de permisos**
   - Asegúrate de ejecutar los scripts como administrador
   - Verifica los permisos de escritura en el directorio base

2. **Error de dependencias**
   - Verifica que Python 3.10+ y Node.js 18+ estén instalados
   - Reinstala las dependencias si es necesario

3. **Error de autenticación**
   - Verifica que las credenciales en `repositories.json` sean correctas
   - Para Google Calendar, sigue el proceso de autenticación manual si es necesario

### Logs y Depuración

- Los logs se guardan en el directorio `logs/`
- Cada MCP tiene su propio archivo de log
- Los errores se muestran en la consola con detalles

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 