import requests

def find_nShared(source_code):
    try:
        source_code = source_code.split('results-amount-container')[1].split('</div>')[0]
        source_code = source_code.split('<span')[1].split('</span>')[0].split('>')[1]
        return source_code
    except:
        if "Found 1 result for" in source_code: return '1'
        return '0'



def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False

data = get('https://pubmed.ncbi.nlm.nih.gov/?term=ludvig+backman+and+patrik+danielson')
print(data)

def unscramble(searchstr):
    searchstr = searchstr.replace("\n ","\n")
    searchstr = searchstr.replace(" \n","\n")
    test_str = searchstr.replace(" ","+")
    authors = test_str.split("\n")
    returnterms = []
    if len(authors)<2: return authors
    for i in range(len(authors)):
        if authors[i] == "": continue
        for j in range(i+1,len(authors)):
            if authors[j] == "": continue
            returnterms.append(f'{authors[i]}+and+{authors[j]}')
    print(returnterms)
    return returnterms

def make_urls(searchlist):
    urllist=[]
    for searchterm in searchlist:
        urllist.append(f'https://pubmed.ncbi.nlm.nih.gov/?term={searchterm}')
    return urllist
