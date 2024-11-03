import hashlib
from .firebase import does_article_exist

def get_url_hash(url: str) -> str: 
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return url_hash

def purge_duplicate_articles(articles):
    response = []
    for article in articles:
        article['id'] = get_url_hash(article['url'])
        if not does_article_exist(article['id']):
            response.append(article)
    return response


