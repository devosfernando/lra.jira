FROM python:alpine3.18

# Instalara git
RUN apk add git

# Creamos directorio de trabajo
RUN mkdir /app

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo Python al contenedor
RUN git clone https://github.com/devosfernando/lra.jira.git

# Establece el directorio de trabajo en el contenedor
WORKDIR /app/lra.jira

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Define el comando que se ejecutará cuando el contenedor arranque
CMD ["python", "./jira.py"]