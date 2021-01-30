import requests
import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from parser import AdvertisementParser

class BaseCrawler(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data, filename):
        pass

    @staticmethod
    def get(url):
        try:
            response = requests.get(url)
        except requests.HTTPError:
            return None
        return response


class LinkCrawler(BaseCrawler):

    def __init__(self, url, cities):
        self.url = url
        self.cities = cities

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.findAll('a', attrs={'class': 'hdrlnk'})

    def crawl_cities(self, url):
        crawl = True
        start = 0
        adv_link = []

        while crawl:
            response = self.get(url+str(start))
            new_links = self.find_links(response.text)
            adv_link.extend(new_links)
            start += 120
            crawl = bool(len(new_links))

        return adv_link

    def store(self, data, *args):
        with open('fixtures/links.json', 'w') as f:
            f.write(json.dumps(data))

    def start(self):
        adv_links = []
        for city in self.cities:
            result = self.crawl_cities(self.url.format(city))
            print(f"{city} | {len(result)}")
            adv_links.extend(result)

        self.store([li.get('href') for li in adv_links])



class DataCrawler(BaseCrawler):

    def __init__(self):
        self.links = self.__load_links()
        self.parser = AdvertisementParser()
        
    @staticmethod    
    def __load_links():
        with open('fixtures/links.json', 'r') as f:
            result = json.loads(f.read())
            print(f"{result} \n")
        return result

    def start(self, store = False):
        for li in self.links:
            response = self.get(li)
            data = self.parser.parse(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))

    def store(self, data, filename):
        with open(f'fixtures/advs/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f"saved in {filename}")
        print('finished')
