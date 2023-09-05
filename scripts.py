def find_nShared(source_code):
    try:
        source_code = source_code.split('results-amount-container')[1].split('</div>')[0]
        source_code = source_code.split('<span')[1].split('</span>')[0].split('>')[1]
        return source_code
    except:
        if "Found 1 result for" in source_code: return '1'
        return '0'

def make_url(searchpair, db="pubmed"):
    if db == "google_scholar":
        url = f'https://scholar.google.com/scholar?hl=sv&as_sdt=0%252C5&q=+author%3A"{searchpair[0]}"+author%3A"{searchpair[1]}"&btnG='
    if db == "pubmed":
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={searchpair[0]}+and+{searchpair[1]}'
    return f'https://pubmed.ncbi.nlm.nih.gov/?term={searchpair[0]}+and+{searchpair[1]}'
