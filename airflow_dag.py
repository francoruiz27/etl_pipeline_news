from __future__ import annotations
import pendulum
from airflow.decorators import dag, task
import sys
from news_proyect.extract.main import extract
from news_proyect.transform.main import transform
from news_proyect.load.main import load
import resource

news_sites_uids = ['clarin', 'NYTimes', 'lanacion']     #shouldnt be hardcoded
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(50000)


@dag(
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    catchup=False,
    tags=["news_dag"],
    schedule_interval='0 0 * * 0' 
)
def taskflow_api_news_proyect():

    @task()
    def extracting():
        articles = []
        for news_site_uid in news_sites_uids:
            articles.extend(extract(news_site_uid))
        return articles

    @task()
    def transforming(articles):
        return transform(articles)


    @task()
    def loading(articles):
        load(articles)

            
    articles = extracting()
    transformed_articles = transforming(articles)
    loading(transformed_articles)

taskflow_api_news_proyect()



