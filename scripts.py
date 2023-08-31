import requests

def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False

data = get('https://pubmed.ncbi.nlm.nih.gov/?term=ludvig+backman+and+patrik+danielson')
print(data)

def unscramble(searchstr):
    searchstr = searchstr.replace(": ",":")
    searchstr = searchstr.replace(" :",":")
    test_str = searchstr.replace(" ","+")
    authors = test_str.split(":")
    returnterms = []
    if len(authors)<2: return authors
    for i in range(len(authors)):
        for j in range(i+1,len(authors)):
            returnterms.append(f'{authors[i]}+and+{authors[j]}')
    print(returnterms)
    return returnterms

def make_urls(searchlist):
    urllist=[]
    for searchterm in searchlist:
        urllist.append(f'https://pubmed.ncbi.nlm.nih.gov/?term={searchterm}')
    return urllist
