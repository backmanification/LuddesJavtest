from globalthings import *
import requests
import random as rd
from time import sleep
from time import time
import json
#from scholarly import scholarly
#from scholarly import ProxyGenerator
"""
from proxy_randomizer import RegisteredProviders
from proxy_randomizer.proxy import Anonymity

rp = RegisteredProviders()
rp.parse_providers()

anonymous_proxies = list(
    filter(lambda proxy: proxy.anonymity == Anonymity.ANONYMOUS, rp.proxies)
)
"""
def find_nShared(source_code):
    try:
        source_code = source_code.split('results-amount-container')[1].split('</div>')[0]
        source_code = source_code.split('<span')[1].split('</span>')[0].split('>')[1]
        return source_code
    except:
        if "Found 1 result for" in source_code: return '1'
        return '0'

def get_pubmed_source(query, count=0):
    tid = time()
    response = requests.get(query)
    #print("response time", time()-tid)
    #print("status code", response.status_code)
    if response.status_code == 200:
        return response.text
    else:
        if count > 2: return f'Error {response.status_code}'
        sleep(0.34)
        return get_pubmed_source(query, count+1)
    return "Unknown Error"
    
def get_pubmed_nArticles(query):
    source_code = get_pubmed_source(query)
    if '<PhraseNotFound>' in source_code:
        return 0
    try:
        nArticles = source_code.split('<Count>')[1].split('</Count>')[0]
    except:
        nArticles = source_code
    return nArticles

def get_inspirehep_source(query, count=0):
    tid = time()
    response = requests.get(query)
    #print("response time", time()-tid)
    #print("status code", response.status_code)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        if count > 2: return f'Error {response.status_code}'
        sleep(5)
        return get_inspirehep_source(query, count+1)
    return "Unknown Error"

def get_inspirehep_nArticles(query):
    json_source = get_inspirehep_source(query)
    return json_source['hits']['total'] 


def get_google_scholar_nArticles_scholarly(pair,url):
    #print("lego")
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    #print('---')
    #print(pg)
    #print(dir(pg))
    #print('----')
    urlext = url.split('.com')[1]
    query = scholarly.search_author('Mikael Wiberg')
    #print("yoyoyo")
    author = next(query)
    #print("gotem")
    author = scholarly.fill(author, sections=['coauthors'])
    #query = scholarly.search_pubs('Literature Review of Methods to Translate Health-Related Quality of Life Questionnaires for Use in Multinational Clinical Trials', patents = False, citations = False, year_low = None, year_high = None) 
    #query = scholarly.search_author_custom_url(urlext)

    #print("query",author)

    return ""

def get_google_scholar_nArticles(query):
    source_code = ""
    if True:#try:
        """
        for it in range(len(anonymous_proxies)):
            try:
                proxies = {'https' : anonymous_proxies[it].get_proxy()}
                print("we got a proxy! Lets go!")
                response = requests.get(query, proxies = proxies, headers=headerlist[1])
                print(f"this number works!!!: {it}")
                break
            except:
                print(f"not number {it}")
            print(f'{it}/{len(anonymous_proxies)}')
        """
        response = requests.get(query, headers=headerlist[1])
        print("HERES WHERE IT HAPPENS!!!!!",response.status_code)
        sleep(0.5)
        if response.status_code == 200:
            source_code = response.text
        elif response.status_code == 500:
            source_code = f'<div id=\"gs_ab_md\"><div class=\"gs_ab_mdw\">Server Error</div>'
    else:#except requests.RequestException:
        pass
    try:
        nArticles = source_code.split('<div id=\"gs_ab_md\"><div class=\"gs_ab_mdw\">')[1].split('</div>')[0]
    except:
        nArticles = response.status_code
    print("nArticles",nArticles)
    #print(source_code)
    return nArticles


def make_url(searchpair, db="pubmed"):
    #start_t = time()
    if db == "google_scholar":
        url = f'https://scholar.google.com/scholar?hl=sv&as_sdt=0%2C5&q=author%3A%22{searchpair[0]}%22+and+author%3A%22{searchpair[1]}%22+&btnG='.replace(' ','+')
        if searchpair[1]=='': url = f'https://scholar.google.com/scholar?hl=sv&as_sdt=0%2C5&q=author%3A%22{searchpair[0]}%22+&btnG='.replace(' ','+')

        #nArticles = get_google_scholar_nArticles(url)
        nArticles = get_google_scholar_nArticles_scholarly(searchpair, url)

    if db == "pubmed":
        query = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=({searchpair[0]}[Author])+and+({searchpair[1]}[Author])'
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term=({searchpair[0]}[Author])+and+({searchpair[1]}[Author])'
        if searchpair[1]=='': 
            query = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=({searchpair[0]}[Author])'
            url = f'https://pubmed.ncbi.nlm.nih.gov/?term=({searchpair[0]}[Author])'
        query = query.replace(' ','+')
        url = url.replace(' ','+')
        nArticles = get_pubmed_nArticles(query)
    if db == "inspire_hep":
        url = f'https://inspirehep.net/literature?q=find+a+{searchpair[0]}+and+a+{searchpair[1]}'
        query = f'https://inspirehep.net/api/literature?q=find+a+{searchpair[0]}+and+a+{searchpair[1]}'
        if searchpair[1]=='':
            url = f'https://inspirehep.net/literature?q=find+a+{searchpair[0]}'
            query = f'https://inspirehep.net/api/literature?q=find+a+{searchpair[0]}'
        query = query.replace(' ','+')
        url = url.replace(' ','+')
        nArticles = get_inspirehep_nArticles(query)
    #print(f'{searchpair} took {time()-start_t} to process')
    return url,nArticles







