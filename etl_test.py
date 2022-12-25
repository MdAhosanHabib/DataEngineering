#import needed libraries
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd

#extract data from mysql server
def extract():
    try:
        # mysql db details
        mydb = mysql.connector.connect(
            host="192.168.161.129",
            user="etl_test",
            password="etl_test",
            database="etl_test")

        # execute query
        mycursor = mydb.cursor()
        mycursor.execute(""" SELECT table_name FROM information_schema.tables WHERE table_schema = 'etl_test'; """)
        src_tables = mycursor.fetchall()
        for tbl in src_tables:
            #query and load save data to dataframe
            df = pd.read_sql_query(f'select * FROM {tbl[0]}', mydb)
            load(df, tbl[0])
    except Exception as e:
        print("Data extract error: " + str(e))
    finally:
        mydb.close()

#load data to postgres
def load(df, tbl):
    try:
        # postgresql db details
        server = "ahosan1"
        database = "etl_test"
        user = "etl_test"
        passwd = "etl_test"

        rows_imported = 0
        engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@{server}/{database}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {tbl}')
        # save df to postgres
        df.to_sql(f'ahosan_{tbl}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # add elapsed time to final print out
        print("Data imported successful")
    except Exception as e:
        print("Data load error: " + str(e))

try:
    #call extract function
    extract()
except Exception as e:
    print("Error while extracting data: " + str(e))
