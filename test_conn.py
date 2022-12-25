import mysql.connector
from sqlalchemy import create_engine

#mysql db connection
mydb = mysql.connector.connect(
  host="192.168.161.129",
  user="etl_test",
  password="etl_test",
  database="etl_test")
mycursor = mydb.cursor()
mycursor.execute(""" SELECT table_name FROM information_schema.tables WHERE table_schema = 'etl_test'; """)
src_tables = mycursor.fetchall()
for tbl in src_tables:
    #query and load save data to dataframe
    print(tbl[0])

#Postgresql connection
server = "ahosan1"
database = "etl_test"
user = "etl_test"
passwd = "etl_test"
engine = create_engine(f'postgresql+psycopg2://{user}:{passwd}@{server}/{database}')
#Read
result_set = engine.execute("SELECT * FROM public.phonebook")
for r in result_set:
    print(r)
