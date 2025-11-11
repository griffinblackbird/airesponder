FROM apache/airflow:2.10.4-python3.11

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy application files
COPY train.py /opt/airflow/train.py
COPY bug_reports.csv /opt/airflow/bug_reports.csv
COPY dags/ /opt/airflow/dags/

# Create necessary directories
RUN mkdir -p /opt/airflow/bugKB /opt/airflow/tmp/chromadb
