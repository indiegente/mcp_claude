# Ocultar la salida del código
$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = "SilentlyContinue"

# Función para leer propiedades
function Get-PropertyValue {
    param (
        [string]$filePath,
        [string]$propertyName
    )
    $content = Get-Content $filePath
    $line = $content | Where-Object { $_ -match "^$propertyName\s*=\s*(.+)$" }
    if ($line) {
        return $matches[1]
    }
    return $null
}

# Leer configuraciones de default.properties
$configPath = "config/default.properties"
$nodeVersion = Get-PropertyValue -filePath $configPath -propertyName "node_version"
$repositoriesPath = Get-PropertyValue -filePath $configPath -propertyName "REPOSITORIES_BASE_PATH"

# Verificar si se está ejecutando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Por favor, ejecuta este script como administrador"
    exit 1
}

# Función para actualizar el PATH
function Update-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# Función para verificar si nvm está instalado
function Test-NvmInstalled {
    try {
        $nvmVersion = nvm version
        return $true
    } catch {
        return $false
    }
}

# Función para verificar la versión de Node.js
function Test-NodeVersion {
    try {
        $nodeVersion = node --version
        $versionNumber = [version]($nodeVersion -replace 'v', '')
        $minVersion = [version]"18.0.0"
        return $versionNumber -ge $minVersion
    } catch {
        return $false
    }
}

# Función para reinstalar Chocolatey
function Reinstall-Chocolatey {
    Write-Host "Reinstalando Chocolatey..."
    Remove-Item -Path "$env:ChocolateyInstall" -Recurse -Force -ErrorAction SilentlyContinue
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Update-Path
}

# Verificar e instalar Chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    Update-Path
}

# Verificar si nvm está instalado y tiene Node.js
$nvmInstalled = Test-NvmInstalled
$nodeVersionOk = Test-NodeVersion

if ($nvmInstalled) {
    Write-Host "nvm detectado. Usando nvm para gestionar Node.js..."
    
    if (-not $nodeVersionOk) {
        Write-Host "Instalando Node.js 18.17.0 con nvm..."
        nvm install 18.17.0
        nvm use 18.17.0
        nvm alias default 18.17.0
        Update-Path
        refreshenv
    } else {
        Write-Host "Node.js versión compatible detectada con nvm"
    }
} else {
    Write-Host "nvm no detectado. Usando Chocolatey para instalar Node.js..."
    
    # Verificar e instalar Node.js
    Write-Host "Verificando Node.js..."
    $currentNodeVersion = node -v
    if (-not $currentNodeVersion) {
        Write-Host "Node.js no detectado. Instalando Node.js $nodeVersion..."
        
        # Limpiar la caché de Chocolatey
        Write-Host "Limpiando caché de Chocolatey..."
        choco cache remove --all -y
        
        # Instalar Node.js con parámetros específicos
        Write-Host "Instalando Node.js..."
        try {
            choco install nodejs --version=$nodeVersion -y --force --install-arguments="'/l*v c:\nodejs_install.log'"
        } catch {
            Write-Host "Error al instalar Node.js. Reinstalando Chocolatey..."
            Reinstall-Chocolatey
            choco install nodejs --version=$nodeVersion -y --force --install-arguments="'/l*v c:\nodejs_install.log'"
        }
        
        # Actualizar PATH
        Update-Path
        refreshenv
        
        # Verificar instalación
        $currentNodeVersion = node -v
        if (-not $currentNodeVersion) {
            Write-Host "Error: No se pudo instalar Node.js. Intentando método alternativo..."
            
            # Intentar con nodejs.install
            Write-Host "Intentando con nodejs.install..."
            try {
                choco install nodejs.install --version=$nodeVersion -y --force --install-arguments="'/l*v c:\nodejs_install.log'"
            } catch {
                Write-Host "Error al instalar Node.js.install. Reinstalando Chocolatey..."
                Reinstall-Chocolatey
                choco install nodejs.install --version=$nodeVersion -y --force --install-arguments="'/l*v c:\nodejs_install.log'"
            }
            
            # Actualizar PATH nuevamente
            Update-Path
            refreshenv
            
            # Verificar instalación nuevamente
            $currentNodeVersion = node -v
            if (-not $currentNodeVersion) {
                Write-Host "Error: No se pudo instalar Node.js. Por favor:"
                Write-Host "1. Reinicia tu computadora"
                Write-Host "2. Abre PowerShell como administrador"
                Write-Host "3. Ejecuta: choco install nodejs --version=$nodeVersion -y"
                exit 1
            }
        }
    } else {
        Write-Host "Node.js versión $currentNodeVersion detectada (OK)"
    }
}

# Verificar e instalar npm
Write-Host "`nVerificando npm..."
$npmVersion = npm -v
if (-not $npmVersion) {
    Write-Host "npm no detectado. Intentando reinstalar Node.js..."
    
    # Reinstalar Node.js
    Write-Host "Desinstalando Node.js..."
    choco uninstall nodejs -y --force
    Write-Host "Instalando Node.js nuevamente..."
    choco install nodejs --version=20.11.1 -y --force
    
    # Actualizar PATH
    Update-Path
    refreshenv
    
    # Verificar npm nuevamente
    $npmVersion = npm -v
    if (-not $npmVersion) {
        Write-Host "Error: No se pudo instalar npm. Por favor:"
        Write-Host "1. Reinicia tu computadora"
        Write-Host "2. Abre PowerShell como administrador"
        Write-Host "3. Ejecuta: choco install nodejs --version=20.11.1 -y"
        exit 1
    }
} else {
    Write-Host "npm versión $npmVersion detectada (OK)"
}

# Instalar Python si no está instalado
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando Python..."
    
    # Instalar Python usando el instalador oficial
    $pythonUrl = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    Write-Host "Descargando instalador de Python..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
    
    Write-Host "Instalando Python..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    
    # Limpiar el instalador
    Remove-Item $installerPath -Force
    
    # Actualizar PATH
    Update-Path
    Start-Sleep -Seconds 10
}

# Crear y configurar entorno virtual de Python
Write-Host "`nConfigurando entorno virtual de Python..." -ForegroundColor Cyan
$venv_path = "venv"
if (-not (Test-Path $venv_path)) {
    Write-Host "Creando entorno virtual en $venv_path..."
    python -m venv $venv_path
}

# Activar el entorno virtual
Write-Host "Activando entorno virtual..."
& "$venv_path\Scripts\Activate.ps1"

# Instalar dependencias de Python
Write-Host "Instalando dependencias de Python..."
pip install -r requirements.txt

# Verificar instalaciones
Write-Host "`nVerificando instalaciones..." -ForegroundColor Cyan
Write-Host "Git version: $(git --version)"
Write-Host "Node.js version: $(node --version)"
Write-Host "npm version: $(npm -v)"
Write-Host "Python version: $(python --version)"
Write-Host "Chocolatey version: $(choco --version)"

Write-Host "`nIMPORTANTE: Si ves algún error, por favor:"
Write-Host "1. Cierra esta ventana de PowerShell"
Write-Host "2. Abre una nueva ventana de PowerShell como administrador"
Write-Host "3. Ejecuta el script nuevamente"
