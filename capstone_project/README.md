# **Predicting growth of sourdough bread market size based on global trends**
### **Data Engineering Capstone Project**

#### **Project Summary**
This project aims to identify trends in a growing community of sourdough bread enthusiasts based on global trends. The company, Sourdough Queen, has seen a rise in sales due to COVID-19 and stay home policy and wishes to analyze past trends in global sourdough community based on newsworthy events. They hope to use this information predict spikes in sales volume in future years. As a result, Sourdough Queen will be able to prepare adequate inventory as well as create highly engaging and relevant social media campaigns to drive more visitors to their website and e-commerce store.

The objective of the current notebook is to create a data pipeline that will provide the necessary data for a data scientist at Sourdough Queen to build a predictive model for anticipating growth in the sourdough market based on global events.

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

The project includes the following files:

* `etl.py` reads data from root directory, processes that data using Spark, and writes them to S3
* `dl.cfg` contains the AWS credentials

## **Data Sources**

We would like to use real-time streaming data of global events and trends. This data may be requested via News API (`https://newsapi.org/docs/endpoints/everything`) and the unofficial Google Trends API (`https://pypi.org/project/pytrends/`), respectively. However, for the purposes of this project, since it would take a long time to accumulate 1 million rows of data, we chose to use a historical data for news headlines (Million News Headlines dataset) and historical trends data downloaded from `https://trends.google.com/trends/explore?q=sourdough`.

Steps to using both APIs can be found in `Capstone Project Template.ipynb`

##### Million News Headlines Data

This contains data of news headlines published over a period of 17 years. Sourced from the reputable Australian news source ABC (Australian Broadcasting Corporation) (`data/abcnews-date-text.csv`).This news dataset is a summarised historical record of noteworthy events in the globe from early-2003 to end-2019 with a more granular focus on Australia. 
This includes the entire corpus of articles published by the ABC website in the given time range. With a volume of two hundred articles each day and a good focus on international news, we can be fairly certain that every event of significance has been captured here. 
Digging into the keywords, one can see all the important episodes shaping the last decade and how they evolved over time. For example: financial crisis, iraq war, multiple elections, ecological disasters, terrorism, famous people, local crimes etc.

##### Google Trends Data

This data includes interest over time for 'sourdough' over the past 5 years (`data/multiTimeline.csv`) as well as interest by countries in the world (`data/geoMap.csv`). Search interest is calculated as a score and interpreted as search interest relative to the highest value for the given region and time. A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. A score of 0 means that there was not enough data for this term.

## **Data Model**

In order to optimize the analysis, we constructed a pipeline that extracts data from the above sources, processes them using Spark, and loads the data back into S3 as a set of dimensional tables as shown in Figure 1 below. This will allow the Sourdough Queen analytics team to explore trends in global sourdough community based on newsworthy events.

![data model](https://r766466c839826xjupyterlnnfq3jud.udacity-student-workspaces.com/lab/tree/data_model.png)

### **Data Pipeline**

The following steps were used to process the raw data into the tables in our database for further analysis as outlined in `etl.py` and `create_tables.py`:

![data pipelines](https://r766466c839826xjupyterlnnfq3jud.udacity-student-workspaces.com/lab/tree/data_pipelines.png)

#### **Data Dictionary**

##### Raw Data Tables

Global search interest for 'sourdough' over the past 5 years

**Interest by date**

| Column      | Type | Description |
| ----------- | ----------- | -----------|
| date      | int64       | Dates ranging from  2015-01-01 to 2020-12-31     |
| search_interest_sourdough_worldwide   | int64        | Search interest ranging from 6 - 100, where 100 is the highest value for the given time period        |

**Interest by country**

| Column      | Type | Description |
| ----------- | ----------- | -----------|
| country      | object       | list of 216 countries in the world       |
| relative_search_interest   | float64        | relative search interest for 75 countries         |

**Million news headlines**

| Column      | Type | Description |
| ----------- | ----------- | -----------|
| publish_date      | object       | Dates ranging from 2003-02-19 to 2019-12-31       |
| headline_text   | object        | Top news headlines        |

##### Staged Data Tables

###### **Fact table**
1. **global_trends** - monthly search trends associated with news headlines
    - *global_trends_id, month, day, day_of_week, publish_date, headline_text*

###### **Dimension tables**
1. **news** - news headlines by date
    - *publish_date, headline_text*
2. **trends** - songs in music database
    - *year, month, day, day_of_week, search_interest_sourdough_worldwide, relative_serach_interest*
3. **time** - global news headline publish dates broken down into specific time units
    - *publish_date, day, month, year, day_of_week*

#### Recommended next steps

Sentiment analysis
Load to Redshift as outlined in Figure 2

#### **Complete Project Write Up**
* Clearly state the rationale for the choice of tools and technologies for the project.

We decided to use Apache Spark for processing data and AWS S3 for the data lake due to their scalability and for building a cost-effective solution for this startup. As the company grows, they will be able to use the existing pipelines to meet their data needs without requiring the switch to a new platform. They will also be able to connect to additional data sources and expand the pipeline in the future using the current tools.

* Propose how often the data should be updated and why.

##### Streaming data

If streaming data is used, the data pipeline can be set to download real-time news and search trends, or other interval (hourly or daily) as required for the business analytics.

##### Static data

In the case of static data, updated google trends data is available on a daily and hourly basis and can be downloaded via the Google Trends API.

#### **Addressing Other Scenarios**

* Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x.
 
With the above scalable, fully managed cloud services, we could increase the availability of the resources to handle larger volumes of data. Specifically, if streaming data is increased by 100x, we may choose to process these in parallel batches using a scheduled pipeline. If larger storage is require, we can increase the storage required on S3. 
 
 * The data populates a dashboard that must be updated on a daily basis by 7am every day.
 
With streaming data, we can use Airflow to create tables using S3 to Redshift operator, stage data and derive fact and dimension tables, for instance:

start

get latest news headlines >> determine sentiment >> check

upload trends data >> create new table >> check

load to Redshift >> check

end
 
 * The database needed to be accessed by 100+ people.
 
By increasing the number of Redshift nodes in our cluster as well as precomputing and storing commonly requested tables in a separate Redshift table, we can avoid slow response times of our data warehouse.