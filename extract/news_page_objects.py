import bs4
import requests
from .common import config

class NewsPage:

    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        self._news_site_uid = news_site_uid

        self._visit(self._url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url) 

    @property
    def _title(self):
        result = self._select(self._queries['article_title'])
        try:
            return str(result[0].text.strip()) if len(result) else ''
        except:
            return ''

    @property
    def _subtitle(self):
        result = self._select(self._queries['article_subtitle'])
        try:
            return str(result[0].text.strip()) if len(result) else ''
        except:
            return ''
    @property
    def url(self):
        return self._url

    @property
    def news_site_uid(self):
        return self._news_site_uid


class ApiArticlePage:

    def __init__(self, title, subtitle, url, news_site_uid):
        self._title = title
        self._subtitle = subtitle
        self._url = url
        self._news_site_uid = news_site_uid