import time
from datetime import datetime
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.base_hook import BaseHook
import pandas as pd
from sqlalchemy import create_engine

#extract tasks
@task()
def get_src_tables():
    #hook = MsSqlHook(mssql_conn_id="sqlserver")
    hook = MySqlHook(mysql_conn_id="MySQL_ETL")
    sql = """ SELECT table_name FROM information_schema.tables WHERE table_schema = 'etl_test'; """
    df = hook.get_pandas_df(sql)
    print(df)
    tbl_dict = df.to_dict('dict')
    return tbl_dict
#load tasks
@task()
def load_src_data(tbl_dict: dict):
    conn = BaseHook.get_connection('PostGreS_ETL')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    all_tbl_name = []
    start_time = time.time()
    #access the table_name element in dictionaries
    for k, v in tbl_dict['TABLE_NAME'].items():
        #print(v)
        all_tbl_name.append(v)
        rows_imported = 0
        sql = f'select * FROM {v}'
        #hook = MySqlHook(mysql_conn_id="MySQL_ETL")
        hook = MySqlHook(mysql_conn_id="MySQL_ETL")
        df = hook.get_pandas_df(sql)
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {v} ')
        df.to_sql(f'src_{v}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
    print("Data imported successful")
    return all_tbl_name

# [START how_to_task_group]
with DAG(dag_id="ahosan_etl_dag",schedule_interval="0 9 * * *", start_date=datetime(2022, 3, 5),catchup=False,  tags=["product_model"]) as dag:

    with TaskGroup("extract_dimProudcts_load", tooltip="Extract and load source data") as extract_load_src:
        src_product_tbls = get_src_tables()
        load_dimProducts = load_src_data(src_product_tbls)
        #define order
        src_product_tbls >> load_dimProducts

    extract_load_src
