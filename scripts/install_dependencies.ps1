# Requiere ejecutarse como administrador
Set-ExecutionPolicy Bypass -Scope Process -Force

# Instalar Chocolatey si no está instalado
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Instalar Python si no está instalado
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    choco install python -y
}

# Instalar Git si no está instalado
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    choco install git -y
} 