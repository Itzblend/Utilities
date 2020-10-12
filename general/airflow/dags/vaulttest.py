from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2020, 7, 25, 7, 50),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(dag_id='vault_test',
          default_args=default_args,
          schedule_interval='* * * * *',
          dagrun_timeout=timedelta(seconds=120))

# Step 1 - Dump data from postgres databases

t1 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='pwd1',
    command='pwd > ~/pwd1.txt',
    dag=dag)

t2 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='pwd2',
    command='cd ~/repos && pwd > ~/pwd2.txt',
    dag=dag)

t3 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='pwd3',
    command='pwd > ~/pwd3.txt',
    dag=dag)
