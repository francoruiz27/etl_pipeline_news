#import argparse
import logging
logging.basicConfig(level=logging.INFO)

import pandas as pd

from .article import Article
from .base import Base, engine, Session


logger = logging.getLogger(__name__)


def load(articles):
    logger.info(articles.iloc[0])
    Base.metadata.create_all(engine)
    session = Session()
    articles.to_csv('news_data.csv')
    for index, row in articles.iterrows():
        #logger.info('Loading article id {} into DB'.format(row['uid']))
        article = Article(row['uid'],
                          row['host'],
                          row['_title'],
                          row['_subtitle'],
                          row['_news_site_uid'],
                          row['n_tokens__title'],
                          row['n_tokens__subtitle'],
                          row['_url'],
                          row['language'])
        session.add(article)

    session.commit()
    session.close()

