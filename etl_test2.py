#import needed libraries
from sqlalchemy import create_engine
import pandas as pd

# mysql db details
server1 = "ahosan2"
database1 = "etl_test"
user1 = "etl_test"
passwd1 = "etl_test"

mydb = create_engine(f'mysql+pymysql://{user1}:{passwd1}@{server1}/{database1}')
df = pd.read_sql_query(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'etl_test';", mydb)
tbl_dict = df

#print(tbl_dict.columns.tolist())
print(tbl_dict['TABLE_NAME'].items())

