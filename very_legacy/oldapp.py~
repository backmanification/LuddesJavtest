# app.py
from flask import Flask, render_template, request
import requests
import urllib.parse
import scripts

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/generate_urls', methods=['POST'])
def generate_urls():
    search_term = request.form['search_term']
    terms = scripts.unscramble(search_term)
    urls = scripts.make_urls(terms)
    #encoded_search = urllib.parse.quote(search_term)
    #urls = [f'https://www.example.com/search?q={encoded_search}&page={page}' for page in range(1, 21)]
    return render_template('urls.html', urls=urls)

@app.route('/fetch_source/<searchterm>')
def fetch_source(searchterm):
    url = scripts.make_urls(searchterm)[0]
    response = requests.get(url)
    source_code = response.text
    return render_template('source.html', source_code=source_code)


if __name__ == '__main__':
    app.run()
