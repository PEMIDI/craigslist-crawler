import requests
import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class BaseCrawler(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self):
        pass


class LinkCrawler(BaseCrawler):

    def __init__(self, url, cities):
        self.url = url
        self.cities = cities

    def get_page(self, url, start):
        try:
            response = requests.get(url+str(start))
        except:
            return None

        print(f"{response.status_code} | {response.url}")
        return response

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.findAll('a', attrs={'class':'hdrlnk'})

    def crawl_cities(self, url):
        crawl = True
        start = 0
        adv_link = []

        while crawl:
            response = self.get_page(url, start)
            new_links = self.find_links(response.text)
            adv_link.extend(new_links)
            start += 120
            crawl = bool(len(new_links))

        return adv_link

    def store(self, data):
        with open('storage/links.json', 'w') as f:
            f.write(json.dumps(data))

    def start(self):
        adv_links = []
        for city in self.cities:
            result = self.crawl_cities(self.url.format(city))
            print(f"{city} | {len(result)}")
            adv_links.extend(result)

        self.store([li.get('href') for li in adv_links])