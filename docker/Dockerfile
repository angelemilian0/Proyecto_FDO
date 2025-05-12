# Imagen base
FROM python:3.8-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY app.py /app/
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]

