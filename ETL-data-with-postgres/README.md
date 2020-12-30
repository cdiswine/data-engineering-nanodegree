# **Data Modelling with Postgres**

## **Purpose of this database**

This database was created for Sparkify. This startup has user activity data stored in `.json` format. They would like to use their data to improve their business (i.e. convert more users from free to paid plans) and their user experience (i.e. making recommendations for other songs that they may like). 

### **Song data**

Following is an example of the filepaths containing song and artist metadata:

```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

```

Following is an example of the song and artist metadata contained in each file:

```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

```

### **Log data**

Following is an example of the filepaths containing daily user activity data:

```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

```

## **Database design**

In order to optimize their analysis, we constructed a postgres database using a star schema comprised of the following tables:

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

### **ETL Pipeline**

The following steps were used to process the raw data into the tables in our database for further analysis as outlined in `etl.py` and `create_tables.py`:

1. **users table**
    - created the user table
    - selected and inserted the user ID, first name, last name, gender and level data into the user table

2. **songs table**
    - created the songs table
    - selected and inserted the song ID, title, artist ID, year, and duration data into the songs table

3. **artists table**
    - created the artists table
    - selected and inserted the artist ID, name, location, latitude, and longitude data into the artists table
    

4. **time table**
    - created the time table
    - filtered the data by `NextSong`
    - converted the `ts` column to datetime
    - calculated the timestamp in seconds and stored the time data as a dataframe
    - inserted the timestamp, hour, day, week of year, month, year, and weekday data into the time table

5. **songplays table**
    - created the songplays table
    - selected song ID and artist ID by querying the songs and artists tables to find matches based on song title, artist name, and song duration time
    - selected and inserted the timestamp, user ID, level, song ID, artist ID, session ID, location, and user agent data into the songplays table
    
## **Sample queries**

For increasing ad revenue, find the times that users are most active. Starting with the following queries:

```
SELECT * FROM users;
```

```
SELECT * FROM time;
```

For creating recommendations for music, find out which songs users like. Starting with the following query: 

```
SELECT first_name, last_name, song_id, artist_id FROM users INNER JOIN songplays ON users.user_id = songplays.user_id;
```