# Imagen base oficial de Python
FROM python:3.10-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias del sistema necesarias para psycopg2
RUN apt-get update \
    && apt-get install -y gcc python3-dev libpq-dev

# Copiar el archivo de requerimientos
COPY requirements.txt requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Defino las variables de entorno Flask
ENV FLASK_APP=src.app:create_app
ENV FLASK_ENV=development

# Exponer el puerto 5000 para que Flask esté disponible
EXPOSE 5000

# Comando para iniciar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]