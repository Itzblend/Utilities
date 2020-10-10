
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator

project_name = 'test_project

default_args = {
    "owner" : 'airflow',
    "depends_on_past" : False,
    "schedule_interval" : None,
    "start_date" : "2019-05-13",
    "email" : [ 'testaccount@dummycompany.com' ],
    "email_on_failure" : True,
    "email_on_retry" : False,
    "retries" : 1,
    "retry_delay" : timedelta(minutes=1)
}


main_dag = DAG(
    project_name,
    default_args = default_args,
    schedule_interval= get_schedule()
)


start = DummyOperator (
    dag             = main_dag,
    task_id         = project_name
)

DAGS = [ main_dag ]
        
