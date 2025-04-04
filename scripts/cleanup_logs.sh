#!/bin/bash

# Script para limpiar archivos de log antiguos
echo "Limpiando logs antiguos..."

# Directorio de logs (ajustar según sea necesario)
LOG_DIR="/var/log"

# Eliminar logs más antiguos que 7 días
find $LOG_DIR -name "*.log" -type f -mtime +7 -exec rm {} \;
find $LOG_DIR -name "*.gz" -type f -mtime +7 -exec rm {} \;

echo "Limpieza de logs completada"
