#!/bin/bash
# Script para instalar dependencias necesarias
echo "Instalando dependencias necesarias..."

# Actualizar repositorios
sudo apt-get update

# Instalar paquetes esenciales
sudo apt-get install -y git vim python3 python3-pip

# Instalar Docker
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    sudo usermod -aG docker $USER
    echo "Docker instalado correctamente"
else
    echo "Docker ya está instalado"
fi

# Instalar AWS CLI
if ! command -v aws &> /dev/null; then
    echo "Instalando AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    echo "AWS CLI instalado correctamente"
else
    echo "AWS CLI ya está instalado"
fi

# Instalar dependencias de Python
pip3 install boto3 pytest

echo "Todas las dependencias han sido instaladas correctamente"
