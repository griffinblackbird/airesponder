# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy dependency file first for better caching
COPY requirements.txt .

# Install dependencies using pip (system-level)
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your application
COPY . .

CMD ["python", "main.py"]
