import hashlib
import logging
from urllib.parse import urlparse
import pandas as pd
import nltk
from nltk.corpus import stopwords
from langdetect import detect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def transform(articles):
    df = pd.DataFrame()
    logger.info('Starting cleaning process')
    df = _read_data(articles, df)
    language = _detect_language(df)
    df = _add_language_column(df, language)
    df = _extract_host(df)
    df = _generate_uids_for_rows(df)
    df = _tokenize_column(df, '_title', language)
    df = _tokenize_column(df, '_subtitle', language)
    df = _remove_duplicate_entries(df, '_title')
    df = _drop_rows_with_missing_values(df)

    return df


def _read_data(articles, df):
    logger.info('Converting articles list to df ')
    df2 = pd.DataFrame()
    for a in articles:
        data = {'_title': [a._title], '_subtitle': [a._subtitle], '_url': [a._url], '_news_site_uid': [a._news_site_uid]}  
        df2 = pd.DataFrame(data)
        df = pd.concat([df2, df], ignore_index=True) 
    return df

def _detect_language(df):           #hay que recorrer el df o la lista articulos y crear un df a partir de esa con los languages 1x1
    logger.info('Detecting language')
    some_title = df['_title'].iloc[0]  #to use it for detecting language 
    language = detect(some_title)
    language = "english" if language == 'en' else "spanish"
    return language     #should be solved by dinamic tasks to be more eficcient


def _add_language_column(df, language):
    logger.info('Filling language column')
    df['language'] = language

    return df


def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['_url'].apply(lambda url: urlparse(url).netloc)

    return df


def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['_url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids

    return df


def _tokenize_column(df, column_name, language):
    logger.info('Calculating the number of unique tokens in {}'.format(column_name))
    stop_words = set(stopwords.words(language))

    n_tokens =  (df
                 .dropna()
                 .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                 .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                 .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
                 .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
                 .apply(lambda valid_word_list: len(valid_word_list))
            )

    df['n_tokens_' + column_name] = n_tokens

    return df


def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df


def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing values')
    return df.dropna()



