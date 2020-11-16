import datetime
import psycopg2
import os

dbhost = os.popen("vault kv get -field=dbhost kv/postgres").read()
dbname = 'sys_data'
dbuser = os.popen("vault kv get -field=dbuser kv/postgres").read()
password = os.popen("vault kv get -field=password kv/postgres").read()
port = os.popen("vault kv get -field=port kv/postgres").read()

global CONNECTION_STRING
CONNECTION_STRING = f'dbname={dbname} user={dbuser} password={password} host={dbhost} port={port}'



def create_partitions():
    conn = psycopg2.connect(CONNECTION_STRING)
    with conn.cursor() as cur:
        cur.execute('SELECT MIN(timestamp) FROM system_data_t.system_info_t;')
        min_timestamp = cur.fetchone()[0]



        max_timestamp = min_timestamp + datetime.timedelta(days=30)



        temp_partition = min_timestamp
        while temp_partition < max_timestamp:

            top_partition = temp_partition + datetime.timedelta(days=7)

            min_partition = temp_partition.strftime('%Y-%m-%d')
            max_partition = top_partition.strftime('%Y-%m-%d')

            min_name = min_partition.replace('-', '_')
            max_name = max_partition.replace('-', '_')

            print(min_partition, '\t', max_partition)

            cur.execute(f"""CREATE TABLE system_data_t.system_info_t_{min_name}_to_{max_name} PARTITION OF system_data_t.system_info_t
                        FOR VALUES FROM ('{min_partition}') TO ('{max_partition}');""")

            temp_partition = top_partition



        min_partition = min_timestamp.strftime('%Y-%m-%d %H:%M')
        max_partition = max_timestamp.strftime('%Y-%m-%d %H:%M')

        #print(min_partition)
        #print(max_partition)

create_partitions()