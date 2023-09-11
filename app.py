from flask import Flask, render_template, request, jsonify
from itertools import combinations
import scripts
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    result = {}
    search_terms = []
    author_options = []
    db = ""

    """
    Add following functionality:
    - If only one name, show all their results
    - Check to see if each name has any hit. If the result is 0, suggest to check spelling
    """
    
    # Retrieve values from all input fields dynamically
    search_terms = [request.form.get(f'search{i}', '').strip() for i in range(1, 101)]  # Assume a maximum of 100 search fields
    author_options =  [request.form.get(f'option{i}', '').strip() for i in range(1, 101)]
    for key, val in request.form.items():
        print(key,val)
    db = request.form.get('search-option')
    # Remove empty search terms and options
    t_st = []
    t_ao =[]
    for i in range(len(search_terms)):
        if search_terms[i] != '':
            t_st.append(search_terms[i])
            t_ao.append(author_options[i])
    search_terms = t_st
    author_options = t_ao

    # Generate pairs of search terms
    search_term_pairs = []
    for i in range(len(search_terms)):
        for j in range(i+1,len(search_terms)):
            if t_ao[i]=='def' and t_ao[j]=='def': continue
            search_term_pairs.append((t_st[i],t_st[j]))
    #search_term_pairs = list(combinations(search_terms, 2))

    print("AO:",author_options, "\nST:", search_terms,  "\nDB:", db)
    
    for pair in search_term_pairs:
        search_result = "N/A"
        url,nArticles = scripts.make_url(pair, db)
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                source_code = response.text
                search_result = scripts.find_nShared(source_code)
        except requests.RequestException:
            pass
        """
        
        # You can also replace the placeholder URL with the actual URL you want to display
        result[f'{pair[0]} + {pair[1]}'] = {
            'values': nArticles,
            'url': url
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
