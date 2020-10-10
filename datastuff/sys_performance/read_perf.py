import psutil
import logging
import json
import time
import psycopg2
from io import StringIO
import os

dbhost = os.popen("vault kv get -field=dbhost kv/postgres").read()
dbname = 'sys_data'
dbuser = os.popen("vault kv get -field=dbuser kv/postgres").read()
password = os.popen("vault kv get -field=password kv/postgres").read()
port = os.popen("vault kv get -field=port kv/postgres").read()

global CONNECTION_STRING
CONNECTION_STRING = f'dbname={dbname} user={dbuser} password={password} host={dbhost} port={port}'


def init_db():
    
    conn = psycopg2.connect(CONNECTION_STRING)
    with conn.cursor() as cur:
        cur.execute(""" CREATE SCHEMA IF NOT EXISTS system_data_t;
                    """)
        cur.execute(open('sql/sys_info_t.sql', 'r').read())

        conn.commit()
        conn.close()
    

def _pg_load_data(insertion_data):
    insertion_data = str(insertion_data)
    conn = psycopg2.connect(CONNECTION_STRING)
    with conn.cursor() as cur:
        cur.execute('CREATE TEMP TABLE staging(DATA json) ON COMMIT DROP;')
        cur.execute(f"""INSERT INTO staging (DATA) VALUES ('{insertion_data}')""")
        cur.execute(open('sql/insert_sys_info.sql', 'r').read())

        conn.commit()
        conn.close()


def read_cpu():
    while True:
        cpu_stats = {}
        cpu_stats['cpu_percent'] = psutil.cpu_percent()
        cpu_stats['cpu_freq'] = psutil.cpu_freq()[0]
        cpu_stats['disk_usage'] = psutil.disk_usage('/')
        cpu_stats['disk_total'] = cpu_stats['disk_usage'][0]
        cpu_stats['disk_used'] = cpu_stats['disk_usage'][1]
        cpu_stats['disk_free'] = cpu_stats['disk_usage'][2]
        cpu_stats['disk_percent'] = cpu_stats['disk_usage'][3]
        

        _pg_load_data(insertion_data=json.dumps(cpu_stats))



read_cpu()
#init_db()