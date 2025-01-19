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

    # Retrieve values from all input fields dynamically
    search_terms = [request.form.get(f'search{i}', '').strip() for i in range(1, 101)]  # Assume a maximum of 100 search fields
    author_options =  [request.form.get(f'option{i}', '').strip() for i in range(1, 101)]
    for key, val in request.form.items():
        print(key,val)
    db = request.form.get('search-option')
    # Remove empty search terms and options
    t_st = []
    t_ao =[]
    warning_mess = ''
    for i in range(len(search_terms)):
        if search_terms[i] != '':
            _,nArticles = scripts.make_url([search_terms[i],''],db)
            if int(nArticles) == 0:
                warning_mess += f'<b>No entries found for {search_terms[i]}</b> </br>'
                continue
            t_st.append(search_terms[i])
            t_ao.append(author_options[i])
    search_terms = t_st
    author_options = t_ao
    warning_mess += '</br>'
    # Generate pairs of search terms
    search_term_pairs = []

    for i in range(len(search_terms)):
        for j in range(i+1,len(search_terms)):
            if (author_options[i]=='def' and author_options[j]=='def') or (author_options[i]=='opp' and author_options[j]=='opp'): continue
            search_term_pairs.append((search_terms[i],search_terms[j]))
    #search_term_pairs = list(combinations(search_terms, 2))
    if len(search_terms)==1: search_term_pairs = [[search_terms[0], '']]

    #print("AO:",author_options, "\nST:", search_terms,  "\nDB:", db)
    
    for pair in search_term_pairs:
        search_result = "N/A"
        url,nArticles = scripts.make_url(pair, db)        
        # You can also replace the placeholder URL with the actual URL you want to display
        if pair[1] == '':
            result[f'{pair[0]}'] = {
                'values': nArticles,
                'url': url,
                'warning_message':warning_mess,
            } 
        else:
            result[f'{pair[0]} + {pair[1]}'] = {
                'values': nArticles,
                'url': url,
                'warning_message':warning_mess,
            }
        warning_mess=""

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
