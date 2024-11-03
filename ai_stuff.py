from transformers import pipeline
from utils import get_unsumarized, update_article
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")



def summarize(article):
    article_text = article['content'][:4000]
    article['summary']= summarizer(article_text, max_length=400, min_length=100, do_sample=False)[0]['summary_text']
    tags = ["google", "apple", "microsoft", "amazon","intel","nvidia","dell","ai",'economic']
    article['tags'] = []
    article_tags = classifier(article_text, candidate_labels=tags, multi_label=True)
    for tag,score in zip(article_tags['labels'], article_tags['scores']):
        if score >= 0.77:
            article['tags'].append(tag)
    return article



unsumarized_articles = get_unsumarized()

for article in unsumarized_articles:
    print(f"Summarizing {article['headline']}")
    new_article = summarize(article)
    new_article['summarized'] = True
    update_article(new_article)
    print(f"Summarized {article['headline']}")