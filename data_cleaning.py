# Imports
import sys
import argparse
import pyspark
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

    permanent_table_name = "InputTable51"
    spark_df.write.format("parquet").saveAsTable(permanent_table_name)

        
    
    return spark_df


def calculate_statistics(joined_df):


    pass






#spark-submit \Users\alena\Documents\HW2\assignment1_p1_data\p1.py \Users\alena\Documents\HW2\assignment1_p1_data\brfss_input.json \Users\alena\Documents\HW2\assignment1_p1_data\nhis_input.csv False

if __name__ == '__main__':
    #inputting values from the command line
    input_file = sys.argv[1]
    '''nhis_file_arg = sys.argv[2]
    save_output_arg = sys.argv[3]
    if save_output_arg == "True":
        output_filename_arg = sys.argv[4]
    else:
        output_filename_arg = None

    '''
    # Start spark session
    #print("TEST!!!")
    spark = SparkSession.builder.getOrCreate()


    inp_fl = create_dataframe(input_file, 'csv', spark)
    #brfss_df = create_dataframe(brfss_file_arg, 'json', spark)
    #transformed = transform_nhis_data(inp_fl)
    
    #joined_df2 = inp_fl.select("_c0", "_c1", "_c8", "_c12", "_c13", "_c14", "_c15")
    #joined_df2 = inp_fl.filter(col("_c0") == "50057912")

    joined_df2  = inp_fl.withColumn("_c8", to_date(inp_fl["_c8"], 'MM/dd/yyyy'))
    joined_df2  = joined_df2.filter(col("_c8") >= "2019-01-01")
    #joined_df2  = joined_df2.groupBy("_c0").collect()
    #joined_df2  = joined_df2.dropDuplicates("_c0")
    joined_df2 = joined_df2.na.drop()
    joined_df2  = joined_df2.distinct()
    joined_df2.show()
    #joined_df2 = joined_df2.select(col("_c8"), when(to_date(col("_c8"),"MM-dd-yyyy").isNotNull, date_format(to_date(col("Date"),"yyyy-MM-dd"),"MM/dd/yyyy")))
    #joined_df2 = joined_df2.select(col("_c8"), trunc(to_date(col("_c8"), "MM/dd/yyyy"), "Month").alias("Month"))
    
    '''joined_df2 = joined_df2.select(col("_c8"), to_date(joined_df2["_c8"], 'MM/dd/yyyy').alias("Month"))#.collect()
    joined_df2 = joined_df2.filter(col("Month") > "2019-01-01")
    joined_df2.show()'''
   
    joined_df2.coalesce(1).write.csv("\\Users\\alena\\Documents\\FinalProject\\output.csv")   
    spark.stop()




