# Data Lake on AWS with Spark

## Purpose of the database

This database was created for Sparkify. Their user and song database in S3 is growing and would like to move their data into a data lake in S3. We built an ETL pipeline that extracts their data from S3, processess them using Spark and loads back into S3 in table format to help with data analysis.

## Database schema

In order to optimize their analysis, we constructed a S3 database using a star schema comprised of the following tables:

### **Fact table**
1. **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
    - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

### **Dimension tables**
1. **users** - users in the app
    - *user_id, first_name, last_name, gender, level*
2. **songs** - songs in music database
    - *song_id, title, artist_id, year, duration*
3. **artists** - artists in music database
    - *artist_id, name, location, latitude, longitude*
4. **time** - timestamps of records in **songplays** broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*

## ETL pipeline
`etl.py` reads data from S3, processes that data using Spark, and writes them back to S3

