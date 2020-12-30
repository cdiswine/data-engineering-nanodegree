import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)
    
    # create temporary table view to write SQL queries
    df.createOrReplaceTempView("songs_table")

    # extract columns to create songs table
    songs_table = spark.sql("""
                      SELECT DISTINCT s.song_id, s.title, s.artist_id, s.year, s.duration
                      FROM songs_table s
                      WHERE song_id IS NOT NULL
    """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(output_data+'songs_table/')

    # extract columns to create artists table
    artists_table = spark.sql("""
                        SELECT DISTINCT a.artist_id, a.artist_name, a.artist_location, a.artist_latitude, a.artist_longitude
                        FROM songs_table a
                        WHERE a.artist_id IS NOT NULL
    """)
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data+'artists_table/')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')
    
    # create temporary table view to write SQL queries
    df.createOrReplaceTempView("logs_table")

    # extract columns for users table    
    artists_table = spark.sql("""
                        SELECT DISTINCT l.userId as user_id, l.firstName as first_name, l.lastName as last_name, l.gender as gender, l.level as level
                        FROM logs_table l
                        WHERE l.userId IS NOT NULL
    """)
    
    # write users table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data+'artists_table/')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(x/1000), TimestampType())
    df = df.withColumn("timestamp", get_timestamp(col("ts")))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: to_date(x), TimestampType())
    df = df.withColumn("start_time", get_timestamp(col("ts")))
    
    # extract columns to create time table
    df = df.withColumn("hour", hour("timestamp"))
    df = df.withColumn("day", dayofmonth("timestamp"))
    df = df.withColumn("month", month("timestamp"))
    df = df.withColumn("year", year("timestamp"))
    df = df.withColumn("week", weekofyear("timestamp"))
    df = df.withColumn("weekday", dayofweek("timestamp"))
    
    time_table = spark.sql("""
                        SELECT DISTINCT t.start_time, t.hour, t.day, t.week, t.month, t.year, t.weekday
                        FROM df t
                        WHERE t.start_time IS NOT NULL
    """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy("year", "month").paraquet(output_data+'time_table/')

    # read in song data to use for songplays table
    song_df = spark.sql("""
                    SELECT DISTINCT song_id, artist_id, artist_name
                    FROM songs_table
    """)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
                        SELECT MONOTONICALLY_INCREASING_ID() as songplay_id, totimestamp(l.ts/1000) as start_time, month(to_timestamp(l.ts/1000)) as month, year(to_timestamp(l.ts/1000)) as year, l.userId as user_id, l.level as level, s.song_id as song_id, s.artist_id as artist_id, l.sessionId as session_id, l.location as location, l.userAgent as user_agent
                        FROM logs_table l
                        JOIN songs_table s ON l.artist = s.artist_name AND l.song = s.title
    """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'songplays_table/')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/dloutput/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
