# Imagen base oficial de Python
FROM python:3.11-slim

# Instala libgdiplus y otras dependencias del sistema
RUN apt-get update && \
    apt-get install -y libgdiplus fonts-dejavu-core && \
    ln -s /usr/lib/libgdiplus.so /usr/lib/gdiplus.dll && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para iniciar la app en producción
CMD ["gunicorn", "projecteFinalDAW.wsgi:application", "--bind", "0.0.0.0:8000"]
