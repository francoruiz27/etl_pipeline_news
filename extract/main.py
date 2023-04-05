#import datetime
import logging
import json

logging.basicConfig(level=logging.INFO)
import re
import requests

from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from .common import config
from .news_page_objects import HomePage, ApiArticlePage, ArticlePage


logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') # https://example.com/hello
is_root_path = re.compile(r'^/.+$') # /some-text


def extract(news_site_uid):
    if news_site_uid == 'NYTimes':
        articles = _api_nyt_articles(news_site_uid)
    else:
        articles = _news_scraper(news_site_uid)
    return articles 


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    homepage = HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('Article fetched!!')
            articles.append(article)

    #_save_articles(news_site_uid, articles)
    return articles
                


def _fetch_article(news_site_uid, host, link):
    logger.info(format(link))

    article = None
    try:
        article = ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, ConnectionError, MaxRetryError) as e:
        logger.warning('Error while fechting the article', exc_info=False)


    if article and not article._subtitle:
        logger.warning('Invalid article. There is no subtitle')
        return None

    return article


def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


def _api_nyt_articles(news_site_uid):
    apikey = 'NdC7sgN1GMxNWaUTWYKXbCZwfEZAAiAJ'     #it has to be a secret
    query_url = f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={apikey}'
    response = requests.get(query_url)
    results = response.json().get('results')
    articles = []

    for article in results:
        title = article.get('title')
        logger.info(title)
        subtitle = article.get('abstract')
        url = article.get('url')
        article = ApiArticlePage(title, subtitle, url, news_site_uid)
        if article:
            articles.append(article)
            logger.info('Article fetched!!')
        else:
            logger.warning('Error creating article')
    
    #_save_articles(news_site_uid, articles)
    return articles


