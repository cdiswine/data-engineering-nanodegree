# Sparkify Datawarehouse

## Purpose of this project

This database was created for Sparkify. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. They would like to use their data to improve their business by gaining insights into what songs their users are listening to. 

## Database schema

In order to optimize their analysis, we built an ETL pipeline that extracted their data from S3, staged them in Redshift, and transformed their data into a set of dimensional tables comprised of the following tables:

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

## Sample queries


```
SELECT songs.song_id FROM songs JOIN artists ON songs.artist_id = artists.artist_id WHERE artist.name = <ARTIST>

```
