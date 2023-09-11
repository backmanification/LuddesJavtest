import requests

def find_nShared(source_code):
    try:
        source_code = source_code.split('results-amount-container')[1].split('</div>')[0]
        source_code = source_code.split('<span')[1].split('</span>')[0].split('>')[1]
        return source_code
    except:
        if "Found 1 result for" in source_code: return '1'
        return '0'

def get_pubmed_nArticles(query):
    source_code = ""
    try:
        response = requests.get(query)
        if response.status_code == 200:
            source_code = response.text
        elif response.status_code == 500:
            source_code = f'<Count>Server Error</Count>'
    except requests.RequestException:
        pass
    if '<PhraseNotFound>' in source_code:
        return 0
    try:
        nArticles = source_code.split('<Count>')[1].split('</Count>')[0]
    except:
        nArticles = source_code
    return nArticles

def get_google_scholar_nArticles(query):
    source_code = ""
    if True:#try:
        response = requests.get(query)
        print("HERES WHERE IT HAPPENS!!!!!",response.status_code)
        if response.status_code == 200:
            source_code = response.text
        elif response.status_code == 500:
            source_code = f'<div id=\"gs_ab_md\"><div class=\"gs_ab_mdw\">Server Error</div>'
    else:#except requests.RequestException:
        pass
    try:
        nArticles = source_code.split('<div id=\"gs_ab_md\"><div class=\"gs_ab_mdw\">')[1].split('</div>')[0]
    except:
        nArticles = 0
    print("nArticles",nArticles)
    #print(source_code)
    return nArticles


def make_url(searchpair, db="pubmed"):
    if db == "google_scholar":
        url = f'https://scholar.google.com/scholar?hl=sv&as_sdt=0%2C5&q=author%3A%22{searchpair[0]}%22+and+author%3A%22{searchpair[1]}%22+&btnG='
        nArticles = get_google_scholar_nArticles(url)

        

    if db == "pubmed":
        #for i in range(len(searchpair)):
        #    searchpair[i] = searchpair[i].replace(' ','+')
        query = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={searchpair[0]}+and+{searchpair[1]}'
        nArticles = get_pubmed_nArticles(query)
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={searchpair[0]}+and+{searchpair[1]}'
    if db == "inspire_hep":
        url = f'https://inspirehep.net/literature?sort=mostrecent&size=25&page=1&q=find%20a%20{searchpair[0]}%20and%20a%20{searchpair[1]}'
    return url,nArticles
