from flask import Flask, render_template, request
from itertools import combinations
import scripts
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}

    if request.method == 'POST':
        fieldCount = len([key for key in request.form if key.startswith('search')])
        search_terms = []
        for i in range(1, fieldCount + 1):
            search_term = request.form.get(f'search{i}', '').strip()
            if search_term:
                search_terms.append(search_term)

        # Generate pairs of search terms
        search_term_pairs = list(combinations(search_terms, 2))
        
        for pair in search_term_pairs:
            search_result = "N/A"
            url= scripts.make_url(pair)
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

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
