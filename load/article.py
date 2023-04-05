from sqlalchemy import Column, String, Integer

from .base import Base


class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    host = Column(String)
    title = Column(String)
    subtitle = Column(String)
    newspaper_uid = Column(String)
    n_tokens_subtitle = Column(Integer)
    n_tokens_title = Column(Integer)
    url = Column(String, unique=True)
    language = Column(String)

    def __init__(self, uid, host, title, subtitle, newspaper_uid, n_tokens_title, n_tokens_subtitle, url, language):
        self.id = uid
        self.host = host
        self.title = title
        self.subtitle = subtitle
        self.newspaper_uid = newspaper_uid
        self.n_tokens_title = n_tokens_title
        self.n_tokens_subtitle = n_tokens_subtitle
        self.url = url
        self.language = language
