from flask import Flask, render_template, request                                                                                              
from itertools import combinations
import scripts
import requests

from jinja2 import Environment
from builtins import len

app = Flask(__name__)

app.jinja_env.globals.update(len=len)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    search_terms = []
    fieldCount = 1

    if request.method == 'POST':
        search_terms = [request.form.get(f'search{i}', '').strip() for i in range(1, 11)]

        # Remove empty search terms                                                                                                            
        search_terms = [term for term in search_terms if term]

        # Generate pairs of search terms                                                                                                       
        search_term_pairs = list(combinations(search_terms, 2))

        for pair in search_term_pairs:
            search_result = "N/A"
            url = scripts.make_url(pair)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    source_code = response.text
                    search_result = scripts.find_nShared(source_code)
            except requests.RequestException:
                pass

            # You can also replace the placeholder URL with the actual URL you want to display                                                 
            result[f'{pair[0]} + {pair[1]}'] = {
                'values': search_result,
                'url': url  # Replace this with the actual URL                                                                                 
            }

    return render_template('index.html', result=result, search_terms=search_terms, fieldCount=fieldCount)

if __name__ == '__main__':
    app.run(debug=True)
