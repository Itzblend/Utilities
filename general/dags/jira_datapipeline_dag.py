from datetime import datetime, timedelta
import json
import os
import shutil
import logging.config


from airflow.hooks import HttpHook, PostgresHook
from airflow.operators import PythonOperator
from airflow.models import DAG

def get_issues(num_hours, **kwargs):
    # Using predefined connection under Admin/Connections
    api_hook = HttpHook(http_conn_id='jira_issues', method='GET')

    delta = datetime.strftime(datetime.now() - timedelta(hours = num_hours), '%Y-%m-%d %H:%M') # 2020-04-24T17:20:26.000+0000
    print(f'HERE IS DELTA{delta}')

    resp = api_hook.run(f'/rest/api/2/search?jql=updated>"{delta}"')
    data = json.loads(resp.text)

    save_folder = 'dag_data'

    file_prefix = os.path.join(save_folder)
    shutil.rmtree(file_prefix, ignore_errors=True)
    os.makedirs(file_prefix, exist_ok=False)

    filename = os.path.join(file_prefix, f'dag_jira_data.json')
    logging.info(f'Saving {filename}')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file)

def query_db(ds, **kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_jira')
    
    query = """ SELECT issue_key FROM kafka.jira_issues;
    """

    data = pg_hook.get_records(query)
    print(data)


args = {
    'owner': 'Magalorian',
    'depends_on_past': False,
    'start_date': datetime(2020, 7, 25, 16, 10),
}


dag = DAG(dag_id='test_jira',
          default_args=args,
          schedule_interval='* * * * *',
          dagrun_timeout=timedelta(minutes=5))



t1 = PythonOperator(task_id='get_issues',
                   provide_context=True,
                   python_callable=get_issues,
           op_kwargs={'num_hours': 168},
                   dag=dag)


t2 = PythonOperator(task_id='query_db',
                   provide_context=True,
                   python_callable=query_db,
                   dag=dag)


