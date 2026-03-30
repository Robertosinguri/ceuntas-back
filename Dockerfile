# Usa la imagen oficial de Python ligera
FROM python:3.11-slim

# Crea el directorio de trabajo
WORKDIR /app

# Copia los requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente y las credenciales al contenedor
COPY . .

# Expone el puerto por defecto de la aplicación
EXPOSE 8000

# Comando para ejecutar FastAPI usando uvicorn con soporte para proxy (Cloudflare)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips='*'"]
