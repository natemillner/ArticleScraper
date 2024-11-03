import requests
from bs4 import BeautifulSoup
import pandas as pd

class intel:
    def get_articles():
        url = 'https://www.intel.com/libs/aggregator?node=/content/www/us/en/newsroom/news-stories/jcr:content/storypar/sortablegrid'
        resp = requests.get(url)
        resp = resp.json()
        response = []
        for article in resp['articles'][::-1][:50]:
            temp = {}
            temp['headline'] = article['title']
            temp['date'] = pd.to_datetime(article['date']).strftime('%Y-%m-%d')
            temp['url'] = "https://intel.com"+article['link']
            temp['source'] = 'Intel'
            response.append(temp)
        return response
    
    def read_articles(articles: list[dict]):
        for article in articles:
            resp = requests.get(article['url'])
            soup = BeautifulSoup(resp.text, 'html.parser')
            article_content = soup.find('div', {'class': 'article-content'})
            paragraphs = article_content.find_all('p')
            all_text = ""
            for paragraph in paragraphs:
                all_text += paragraph.text + '\n'
            article['content'] = all_text
        return articles