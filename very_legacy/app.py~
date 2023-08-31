# app.py
from flask import Flask, render_template, request, jsonify
import requests
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

@app.route('/get_source', methods=['GET'])
def get_source():
    url = request.args.get('url')
    if url:
        response = requests.get(url)
        source_code = response.text
        return render_template('source.html', source_code=source_code)
    else:
        return "No URL provided."

@app.route('/generate_source_strings', methods=['POST'])
def generate_source_strings():
    url_list = request.json.get('urls', [])
    source_strings = []

    for url in url_list:
        response = requests.get(url)
        source_code = response.text
        source_strings.append(source_code)

    return jsonify(source_strings)

if __name__ == '__main__':
    app.run()
