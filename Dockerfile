# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]