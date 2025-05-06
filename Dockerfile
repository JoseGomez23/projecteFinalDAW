# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Instala libgdiplus y dependencias del sistema
RUN apt-get update && \
    apt-get install -y libgdiplus fonts-dejavu-core && \
    ln -s /usr/lib/libgdiplus.so /usr/lib/gdiplus.dll && \
    apt-get clean

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto en el que correrá Django
EXPOSE 8000

# Comando para ejecutar el servidor (ajústalo si usas gunicorn u otro)
CMD ["gunicorn", "tu_proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
