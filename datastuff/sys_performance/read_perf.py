import psutil
import logging
import json
import time
import psycopg2
from io import StringIO
import os
from psycopg2 import OperationalError, errorcodes, errors


dbhost = os.popen("vault kv get -field=dbhost kv/postgres").read()
dbname = 'sys_info'
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

    try:
        with conn.cursor() as cur:
            cur.execute('CREATE TEMP TABLE staging(DATA json) ON COMMIT DROP;')
            cur.execute(f"""INSERT INTO staging (DATA) VALUES ('{insertion_data}')""")
            cur.execute(open('sql/insert_sys_info.sql', 'r').read())
    except psycopg2.Error as err:
        print(err)
        pass

    finally:
        conn.commit()
        conn.close()
        time.sleep(30)


def read_cpu():
    while True:
        system_stats = {}
        system_stats['cpu_percent'] = psutil.cpu_percent()
        system_stats['cpu_freq'] = psutil.cpu_freq()[0]
        system_stats['disk_usage'] = psutil.disk_usage('/')
        system_stats['disk_total'] = system_stats['disk_usage'][0]
        system_stats['disk_used'] = system_stats['disk_usage'][1]
        system_stats['disk_free'] = system_stats['disk_usage'][2]
        system_stats['disk_percent'] = system_stats['disk_usage'][3]
        system_stats['ram_used'] = psutil.virtual_memory()[3]
        system_stats['ram_free'] = psutil.virtual_memory()[1]
        system_stats['ram_percent'] = psutil.virtual_memory()[2]
        
        # Network stats
        psutil_network = psutil.net_io_counters()

        system_stats['bytes_sent'] = psutil_network[0]
        system_stats['bytes_recv'] = psutil_network[1]
        system_stats['packets_sent'] = psutil_network[2]
        system_stats['packets_recv'] = psutil_network[3]

        _pg_load_data(insertion_data=json.dumps(system_stats))



if __name__ == '__main__':
    #read_cpu()
    init_db()
