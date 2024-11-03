import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase app
cred = credentials.Certificate('./firebaseauth.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


def does_article_exist(url_hash: str):
    doc_ref = db.collection('articles').document(url_hash)
    if doc_ref.get().exists:
        return True
    else:
        return False
    
def add_articles(articles: list[dict]):
    for article in articles:
        article['summarized']= False
        article['image'] = ""
        doc_ref = db.collection('articles').document(article['id'])
        doc_ref.set(article)
    return True

def get_unsumarized():
    docs = db.collection('articles').where('summarized', '==', False).stream()
    articles = []
    for doc in docs:
        articles.append(doc.to_dict())
    return articles

def update_article(article: dict):
    doc_ref = db.collection('articles').document(article['id'])
    doc_ref.set(article)
    return True

#iterate all docs and update date to "YYYY-MM-DD" format
def update_date():
    docs = db.collection('articles').stream()
    for doc in docs:
        article = doc.to_dict()
        article['date'] = article['date'].split('T')[0]
        doc_ref = db.collection('articles').document(article['id'])
        doc_ref.set(article)
    return True