from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.hooks import SSHHook
sshHook = SSHHook(conn_id='hetzner_airflow')

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'magalorian',
    'depends_on_past': False,
    'start_date': datetime(2020, 7, 21),
    'email': ['huhta.lauri@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('sshtest', default_args=default_args)

# t1, t2, t3 and t4 are examples of tasks created using operators

t1 = SSHExecuteOperator(
    task_id="task1",
    bash_command='echo "im from ssh" > ~/sshtest.txt',
    ssh_hook=sshHook,
    dag=dag)