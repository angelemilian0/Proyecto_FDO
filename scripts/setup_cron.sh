#!/bin/bash

# Script para configurar tareas cron para limpieza de logs

echo "Configurando tarea cron para limpieza diaria de logs..."

# Ruta al script de limpieza de logs
SCRIPT_PATH="$PWD/scripts/cleanup_logs.sh"

# Comprobar si el script existe
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: El script de limpieza de logs no existe en $SCRIPT_PATH"
    exit 1
fi

# Crear entrada de cron para ejecutar diariamente a las 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * $SCRIPT_PATH > /tmp/cleanup_logs.log 2>&1") | crontab -

echo "Tarea cron configurada correctamente"
