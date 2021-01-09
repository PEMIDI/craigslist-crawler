import requests
from bs4 import BeautifulSoup


def get_page(url):
    try:
        respone = requests.get(url)
    except:
        return None

    return respone

def find_links(html_doc):
    soup = BeautifulSoup(html_doc)
    return soup.findAll('a')


if __name__ == "__main__":
    link = 'https://newyork.craigslist.org/d/apartments-housing-for-rent/search/apa'
    respone = get_page(link)

    links = find_links(respone.text)    

    for li in set(links):
        print(li.get('href'))