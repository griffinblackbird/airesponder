from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
sys.path.append('/opt/airflow')

from train import retrainBugReportKB

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'bug_kb_retrain',
    default_args=default_args,
    description='Retrain bug report knowledge base every 2 minutes',
    schedule_interval=timedelta(minutes=1),
    catchup=False,
    tags=['RAG', 'Bug Report'],
)

def retrain_task():
    """Task to retrain the bug report knowledge base"""
    print("Starting bug report KB retraining...")
    retrainBugReportKB()
    print("Bug report KB retraining completed!")

retrain_bug_kb = PythonOperator(
    task_id='retrain_bug_kb',
    python_callable=retrain_task,
    dag=dag,
)
