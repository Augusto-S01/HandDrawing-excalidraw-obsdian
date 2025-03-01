# Usa a imagem oficial do Python como base
FROM python:3.10

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY app.py .

# Instala dependências do sistema necessárias para OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
