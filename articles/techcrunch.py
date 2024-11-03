import requests
from bs4 import BeautifulSoup

class tc:
    def get_articles():
        response = []
        url = 'https://techcrunch.com/latest/'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser') 

        articles = soup.find('ul', {'class': 'wp-block-post-template is-layout-flow wp-block-post-template-is-layout-flow'}).find_all('h3')

        for article in articles:
            
            headline = article.find('a')
            link = headline['href']
            headline= headline.text
            date = link.split('.com/')[1].split('/')[0:3]
            date = '/'.join(date)
            response.append({'headline': headline, 'url': link, 'date': date, 'source': 'TechCrunch'})

        return response

    def read_articles(articles: dict):
        for article in articles:
            url = article['url']
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')

            paragraphs = soup.find('div', {'class': 'entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained'}).find_all('p',{'class': 'wp-block-paragraph'})
            all_text = ""
            for paragraph in paragraphs:
                if paragraph.text == 'This is TechCrunch’s Week in Review, where we recap the week’s biggest news. Want this delivered as a newsletter to your inbox every Saturday? Sign up here.':
                    break
                all_text += paragraph.text + '\n'
            article['content'] = all_text
        return articles