# AI Responder - Bug Report KB Retraining

This project uses Apache Airflow to automatically retrain the bug report knowledge base every 2 minutes.

## Setup and Run

1. **Start the services:**
   ```bash
   docker-compose up -d
   ```

2. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

3. **The DAG will automatically run every 2 minutes**
   - DAG name: `bug_kb_retrain`
   - Schedule: Every 2 minutes
   - The DAG is set to auto-start (not paused)

## Stop Services

```bash
docker-compose down
```

## View Logs

```bash
docker-compose logs -f airflow-scheduler
```

## Architecture

- **PostgreSQL**: Airflow metadata database
- **Airflow Webserver**: UI on port 8080
- **Airflow Scheduler**: Runs DAGs on schedule
- **DAG**: Located in `dags/bug_retrain_dag.py`

The DAG calls `retrainBugReportKB()` from `train.py` every 2 minutes.
