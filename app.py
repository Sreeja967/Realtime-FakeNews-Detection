from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(_name_)

# Replace with your real NewsAPI key
NEWS_API_KEY = '9fbc7bea9b9c45aa9ae0d51dc2e03e20'

def search_news_api(query, api_key, num_results=5):
    url = f'https://newsapi.org/v2/everything?q={query}&language=en&pageSize={num_results}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': f'API Error {response.status_code}: {response.json().get("message", "Unknown error")}'}
    return response.json().get('articles', [])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        claim = request.form['claim']
        return redirect(url_for('verify_claim', claim=claim))
    return render_template('index.html')

@app.route('/verify/<claim>')
def verify_claim(claim):
    articles = search_news_api(claim, NEWS_API_KEY)
    verification_result = {
        'claim': claim,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'articles': [],
        'error': None,
        'verdict': '',
        'confidence': 0
    }

    if isinstance(articles, dict) and 'error' in articles:
        verification_result['error'] = articles['error']
        verification_result['verdict'] = f"Error - {articles['error']}"
    elif not articles:
        verification_result['verdict'] = "Unverified - No recent news found"
        verification_result['confidence'] = 0
    else:
        verification_result['verdict'] = "Verified - News found"
        verification_result['confidence'] = min(100, len(articles) * 20)
        verification_result['articles'] = articles

    return render_template('result.html', result=verification_result)

if _name_ == "_main_":
    app.run(debug=True)