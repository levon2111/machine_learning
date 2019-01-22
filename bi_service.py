import zipfile

import StringIO
import requests

source = requests.get("https://resources.lendingclub.com/LoanStats3d.csv.zip", verify=False)
stringio = StringIO.StringIO(source.content)
unzipped = zipfile.ZipFile(stringio)
import pandas as pd
from pywebhdfs.webhdfs import PyWebHdfsClient

subselection_csv = pd.read_csv(unzipped.open('LoanStats3d.csv'), skiprows=1, skipfooter=2, engine='python')
stored_csv = subselection_csv.to_csv('./stored_csv.csv')
hdfs = PyWebHdfsClient(user_name="hdfs", port=50070, host="sandbox")
hdfs.make_dir('chapter5')
with open('./stored_csv.csv') as file_data:
    hdfs.create_file('chapter5/LoanStats3d.csv', file_data, overwrite=True)
print(hdfs.get_file_dir_status('chapter5/LoanStats3d.csv'))

from pyspark.sql import HiveContext

# sc = SparkContext()
sqlContext = HiveContext(sc)
data = sc.textFile("/chapter5/LoanStats3d.csv")
parts = data.map(lambda r: r.split(','))
firstline = parts.first()
datalines = parts.filter(lambda x: x != firstline)


def cleans(row):
    row[7] = str(float(row[7][:-1]) / 100)
    return [s.encode('utf8').replace(r"_", " ").lower() for s in row]


datalines = datalines.map(lambda x: cleans(x))

from pyspark.sql.types import *

fields = [StructField(field_name, StringType(), True) for field_name in firstline]
schema = StructType(fields)
schemaLoans = sqlContext.createDataFrame(datalines, schema)
schemaLoans.registerTempTable("loans")

sqlContext.sql("drop table if exists LoansByTitle")
sql = '''create table LoansByTitle stored as parquet as select title, count(1) as number from loans group by title order by number desc'''
sqlContext.sql(sql)

sqlContext.sql('drop table if exists raw')
sql = '''create table raw stored as parquet as select title, emp_title,grade,home_ownership,int_rate,recoveries,collection_recovery_fee,loan_amnt,term from loans'''
sqlContext.sql(sql)
