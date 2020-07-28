from datetime import datetime, timedelta
import json
from io import StringIO
import sys
import os
import logging
import shutil
from contextlib import contextmanager


from airflow.hooks import HttpHook, PostgresHook
from airflow.operators import PythonOperator
from airflow.models import DAG

@contextmanager
def pg_cursor():
    pg_hook = PostgresHook(postgres_conn_id='postgres_jira')
    conn = pg_hook.get_conn()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except psycopg2.DatabaseError:
        raise
    finally:
        cur.close()
        conn.close()

def format_query(filename: str, kwargs: Dict[str, str]) -> str:
    """ Read an sql file and format it with values from kwargs.
    """

    with open(filename, 'r') as file:
        query = file.read()

    return query.format(**kwargs)


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

def load_issues(directory, **kwargs):

    data_files = []
    # Collect the files in the directory into a list
    for dirpath, _, files in os.walk(directory):
        for filename in files:
            data_files.append(os.path.join(dirpath, filename))


    for filename in data_files:
        with open(filename, 'r') as file:
            data = json.load(file)
        # Convert json into newline delimited json format so that after insertion
        # Each row in the db_tables corresponds to one revision
        json_data_rows = [json.dumps(x) for x in data['issues']]
        insertion_data = StringIO('\n'.join(json_data_rows))
        
        with db_cursor(CONNECTION_STRING) as cur:
            startTime = datetime.now()
            cur.execute('CREATE TEMP TABLE staging(DATA JSONB) ON COMMIT DROP;')
            cur.copy_expert("COPY staging FROM STDIN WITH CSV quote e'\x01' delimiter e'\x02'", insertion_data)
            cur.execute(format_query('sql/load_jira_issues.sql', SQL_CONFIG))
            print(f'Insertion took {datetime.now() - startTime} seconds')



def query_db(ds, **kwargs):

    query = """ SELECT issue_key FROM kafka.jira_issues;
    """

    with pg_cursor() as cur:
        cur.execute(query)
        print(cur.fetchall())

args = {
    'owner': 'Magalorian',
    'depends_on_past': False,
    'start_date': datetime(2020, 7, 25, 16, 10)
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

t2 = PythonOperator(task_id='load_issues',
                    provide_context=True,
                    python_callable=load_issues,
                    op_kwargs={'directory': 'dag_data'},
                    dag=dag
                    )


t3 = PythonOperator(task_id='query_db',
                   provide_context=True,
                   python_callable=query_db,
                   dag=dag)


