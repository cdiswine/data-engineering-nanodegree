# imports
import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

# configure AWS
config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']

# create spark session
def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

# spark jobs to create s3 data lake

    # read data from s3, process using pyspark, write back in s3
    
    # process trends data

def process_trends_data(spark, input_data, output_data):
        # get file path to trends data file
        trends_data = input_data + 'trends_df_expanded.csv'

        # read trends data file
        df = spark.read.csv(trends_data)

        # create temporary table view to write SQL queries
        df.createOrReplaceTempView("trends_table")

        # extract columns to create trends table
        trends_table = spark.sql("""
                            SELECT s.year, s.month, s.day, s.day_of_week, s.search_interest_sourdough_worldwide, s.relative_search_interest
                            FROM trends_table s
                            WHERE s.search_interest_sourdough_worldwide IS NOT NULL
        """)

        # write trends table to parquet files
        trends_table.write.mode('overwrite').parquet(output_data+'trends_table/')

    # process news data

def process_news_data(spark, input_data, output_data):
        # get file path to news data file
        news_data = input_data + 'abcnews-date-text.csv'

        # read news data file
        df = spark.read.csv(news_data)

        # create temporary table view to write SQL queries
        df.createOrReplaceTempView("news_table")

        # extract columns to create news table
        news_table = spark.sql("""
                        SELECT n.publish_date, n.headline_text
                        FROM news_table n
                        WHERE headline_text IS NOT NULL
        """)

        # write news table to parquet files partitioned by country and date
        news_table.write.mode('overwrite').parquet(output_data+'news_table/')
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: to_date(x), TimestampType())
    df = df.withColumn("publish_date", get_timestamp(col("ts")))
    
    # extract columns to create time table
    df = df.withColumn("day", dayofmonth("publish_date"))
    df = df.withColumn("month", month("publish_date"))
    df = df.withColumn("year", year("publish_date"))
    df = df.withColumn("day_of_week", dayofweek("publish_date"))
    
    time_table = spark.sql("""
                        SELECT DISTINCT t.publish_date, t.day, t.month, t.year, t.day_of_week
                        FROM df t
                        WHERE t.publish_date IS NOT NULL
    """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').paraquet(output_data+'time_table/')

        
    # extract columns from joined news, trends and time datasets to create global_trends table 
    global_trends_table = spark.sql("""
                        SELECT MONOTONICALLY_INCREASING_ID() as global_trends_id, month, day, day_of_week, publish_date, headline_text
                        FROM news_table n
                        JOIN trends_table s ON s.month AND s.day AND s.day_of_week
    """)

    # write global trends table to parquet files partitioned by year and month
    global_trends_table.write.mode('overwrite').parquet(output_data+'global_trends_table/')
        

def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/dloutput/"
    
    process_news_data(spark, input_data, output_data)    
    process_trends_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()