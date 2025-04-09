#!/bin/bash

# Instalar Homebrew si no está instalado
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Instalar Python si no está instalado
if ! command -v python3 &> /dev/null; then
    brew install python
fi

# Instalar Git si no está instalado
if ! command -v git &> /dev/null; then
    brew install git
fi 