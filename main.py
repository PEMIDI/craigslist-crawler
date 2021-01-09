import requests
from bs4 import BeautifulSoup


#get adv_links
#stop crawl when adv pages finished

def get_page(url, start = 0):
    try:
        respone = requests.get(url.format(str(start)))
    except:
        return None
    print(f"Status code : {respone.status_code}, link : {respone.url}")

    return respone


def find_links(html_doc):

    soup = BeautifulSoup(html_doc)
    return soup.findAll('a', attrs={'class':'hdrlnk'})
        

def start_crawl(url):
    start = 0
    crawl = True
    adv_links = list()

    while crawl:
        response = get_page(url, start)
        new_links = find_links(response.text)
        adv_links.extend(new_links)
        start += 120
        crawl = bool(len(new_links))

    return adv_links




if __name__ == "__main__":
    link = 'https://poconos.craigslist.org/d/apartments-housing-for-rent/search/apa?s={}'
    

    links = start_crawl(link)
    print('total:', len(links))    

    