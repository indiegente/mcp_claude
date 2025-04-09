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
- Python 3.8 o superior
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
- Python (última versión estable)
- Git
- Homebrew (solo macOS)
- Command Line Tools (solo macOS)
- Chocolatey (solo Windows)

3. Verificar la instalación:
```bash
# Verificar Python
python --version  # Windows
python3 --version  # macOS/Linux

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

### Verificación de la Instalación

Después de ejecutar los scripts de instalación, puedes verificar que todo se instaló correctamente:

```bash
# Verificar componentes instalados
python --version  # o python3 --version en macOS
git --version
npm --version     # Si se instaló Node.js
pyenv --version   # Si se instaló pyenv
nvm --version     # Si se instaló nvm

# Verificar permisos y rutas
echo $PATH        # En macOS/Linux
echo %PATH%       # En Windows
```

Si encuentras algún problema, consulta la sección [Solución de Problemas](#solución-de-problemas).

## ⚙️ Configuración

### 1. GitHub Token

Necesitarás un token de acceso personal de GitHub con los siguientes permisos:
- `repo` (acceso completo)
- `read:org`

Para generar un token:
1. Ve a [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Haz clic en "Generate new token"
3. Selecciona los permisos mencionados
4. Copia el token generado

El token puede ser configurado de tres formas:
```bash
# 1. Variable de entorno
export GITHUB_TOKEN=your_token_here

# 2. Archivo de configuración
mkdir -p ~/.mcp
echo "your_token_here" > ~/.mcp/github_token

# 3. Interactivamente durante la ejecución del script
# (el script te pedirá el token si no lo encuentra configurado)
```

### 2. Configuración de Repositorios

Revisa y ajusta el archivo `config/repositories.json` según tus necesidades:

```json
{
  "repositories": [
    {
      "name": "linkedin-extract",
      "url": "https://github.com/your-org/linkedin-extract",
      "type": "node",
      "required_env": ["LINKEDIN_API_KEY"]
    },
    // ... otros repositorios
  ]
}
```

### 3. Variables de Entorno

Prepara las variables de entorno necesarias para cada repositorio. Puedes:
1. Configurarlas en tu sistema
2. Crear un archivo `.env` en cada repositorio
3. Dejar que el script las solicite interactivamente

## 📦 Uso

### Ejecución Básica

```bash
# Windows (como administrador)
python setup.py

# macOS/Linux
python3 setup.py
```

### Proceso de Ejecución

El script realizará las siguientes acciones:

1. **Verificación de Prerrequisitos**
   - Comprueba versiones de Python y Git
   - Verifica permisos necesarios

2. **Configuración de GitHub**
   - Valida/solicita token de GitHub
   - Configura credenciales de Git

3. **Instalación de Gestores de Paquetes**
   - Instala/actualiza nvm (Node.js)
   - Instala/actualiza pyenv (Python)

4. **Por cada repositorio**:
   - Clona/actualiza el repositorio
   - Instala dependencias
   - Configura variables de entorno
   - Ejecuta pruebas

5. **Configuración de Claude Desktop**
   - Genera archivo de configuración
   - Lo coloca en la ubicación correcta

### Opciones de Ejecución

```bash
python setup.py --help  # Muestra opciones disponibles
python setup.py --verbose  # Modo verboso
python setup.py --skip-tests  # Omite ejecución de pruebas
```


# Configurar el repositorio remoto (asumiendo que ya está creado en GitHub)
# git remote add origin https://github.com/your-org/mcp-setup.git
# git push -u origin develop 