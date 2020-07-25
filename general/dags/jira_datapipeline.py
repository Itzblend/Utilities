from datetime import timedelta, datetime
import airflow
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Magalorian',
    'depends_on_past': False,
    'email': ['huhta.lauri@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2020, 7, 25, 10, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(dag_id='jira_datapipeline',
          default_args=default_args,
          schedule_interval='* * * * *',
          dagrun_timeout=timedelta(minutes=20))


t1 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='fetch_jira_issues',
    command='cd /home/magalorian/repos/KafkaPOC/scripts && python3 fetch_jira.py fetch-latest-issues --save_folder data',
    dag=dag)

t2 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='upload_jiradata',
    command='cd /home/magalorian/repos/KafkaPOC/scripts && python3 jiradb.py upload-directory data',
    dag=dag)

t3 = SSHOperator(
    ssh_conn_id='hetzner_airflow',
    task_id='process_daily_statuses',
    command='cd /home/magalorian/repos/KafkaPOC/scripts && python3 jira_daily_statuses.py process-latest 3',
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t2)
