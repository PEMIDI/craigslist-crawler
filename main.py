import requests
from bs4 import BeautifulSoup
import sys

#get adv_links
#stop crawl when adv pages finished

def get_page(url, start = 0):
    try:
        respone = requests.get(url+str(start))
    except:
        return None
    print(f"Status code : {respone.status_code}, link : {respone.url}")

    return respone


def find_links(html_doc):

    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.findAll('a', attrs={'class':'hdrlnk'})
    

def start_crawl_cites(url):
    start = 0
    crawl = True
    adv_links = list()

    while crawl:
        response = get_page(url, start)
        if response is None:
            crawl = False
            continue
        new_links = find_links(response.text)
        adv_links.extend(new_links)
        start += 120
        crawl = bool(len(new_links))

    return adv_links

def start_crawl():
    cites = ['london', 'berlin']

    link = 'https://{}.craigslist.org/d/apartments-housing-for-rent/search/brx/apa?s='

    for city in cites:
        result = start_crawl_cites(link.format(city))
        print(f"{city} : {len(result)}")


def get_pages_data():
    raise NotImplementedError()


if __name__ == "__main__":
    
    switch = sys.arg[1]

    if switch == 'find_links':
        start_crawl()
    elif switch == 'extract_pages':
        get_pages_data()
    