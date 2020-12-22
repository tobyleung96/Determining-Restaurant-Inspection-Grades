# Imports
import sys
import argparse
import pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import lit, when, col
from pyspark.sql.functions import to_date, to_timestamp
from pyspark.sql.types import DateType




def create_dataframe(filepath, format, spark):
    if format == 'json':
        spark_df = spark.read.json(filepath)

    if format == 'csv':
        spark_df = spark.read.csv(filepath)
    #spark_df.show()
    return spark_df


def transform_nhis_data(spark_df):

    permanent_table_name = "InputTable99"
    spark_df.write.format("parquet").saveAsTable(permanent_table_name)

    return spark_df








#spark-submit \Users\alena\Documents\FinalProject\test.py \Users\alena\Documents\FinalProject\DOHMH_New_York_City_Restaurant_Inspection_Results.csv \Users\alena\Documents\FinalProject\pluto_20v6.csv
#spark-submit \Users\alena\Documents\HW2\assignment1_p1_data\p1.py \Users\alena\Documents\HW2\assignment1_p1_data\brfss_input.json \Users\alena\Documents\HW2\assignment1_p1_data\nhis_input.csv False

if __name__ == '__main__':
    #inputting values from the command line
    input_file = sys.argv[1]
    input_file2 = sys.argv[2]

    spark = SparkSession.builder.getOrCreate()


    inp_fl = create_dataframe(input_file, 'csv', spark)
    pluto = create_dataframe(input_file2, 'csv', spark)
    
    joined_df2 = inp_fl.select("_c0", "_c1", "_c8")
    joined_df2 = joined_df2.na.drop()
    joined_df2  = inp_fl.withColumn("_c8", to_date(inp_fl["_c8"], 'MM/dd/yyyy'))
    
    joined_df2  = joined_df2.filter(col("_c8") >= "2017-01-01")

    joined_df2 = joined_df2.distinct()

    joined_df2 = joined_df2.toPandas()

    pluto = pluto.distinct()

    #pluto = pluto.na.drop()    
    pluto = pluto.toPandas()
    pluto = pluto[['_c70', '_c0', '_c34', '_c33', '_c35', '_c36', '_c40', '_c41', '_c37', '_c38', '_c39', '_c42', '_c60', '_c57', '_c58']]
    joined_df2 = joined_df2[['_c24', '_c0', '_c8', '_c14', '_c15', '_c13', '_c7', '_c10', '_c11']]



   
    joined_df2 = joined_df2.groupby('_c0').apply(lambda x: x.sort_values(['_c8'], ascending=False).head(3))




    joined_df2.columns = joined_df2.columns.map("_".join)
    joined_df2 = joined_df2.reset_index()

    joined_df2 = joined_df2.rename(columns = {'__c_2_4': 'BBL'})
    pluto = pluto.rename(columns = {'_c70':  'BBL'})
    joined_df2 = pd.merge(joined_df2, pluto, how="left", on=["BBL"])



    gfg_csv_data = joined_df2.to_csv("output3.csv", index = True) 
    #gfg_csv_data = joined_df2.to_csv("\\Users\\alena\\Documents\\FinalProject\\output3.csv", index = True) 
    #print('\nCSV String:\n', gfg_csv_data)
    
    spark.stop()




