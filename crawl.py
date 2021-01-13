import requests
from bs4 import BeautifulSoup
import json
from abc import ABC, abstractmethod

class BaseCrawler(ABC):

    @abstractmethod
    def start(self):
        pass

    # @abstractclassmethod
    # def store():
    #     pass


class Link_crawler(BaseCrawler):

    def __init__(self, link, cities):
        self.link = link
        self.cities = cities

    def get_page(self ,link, start=0):
        try:
            response = requests.get(link+str(start))
        except:
            return None

        print(f"Status code : {response.status_code} : {response.url}")

        return response

    def link_finder(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup.findAll('a', attrs={'class':'hdrlnk'})

    
    def crawl_cities(self, url):
        start = 0
        crawl = True
        adv_links = []

        while crawl:
            response = self.get_page(link=url, start=start)
            if response is None:
                crawl = False
                continue
            new_links = self.link_finder(response.text)
            adv_links.extend(new_links)
            start += 120
            crawl = bool(len(new_links))

        return adv_links

    def start(self):
        for city in self.cities:
            result = self.crawl_cities(self.link.format(city))
            print(f"{city} : {len(result)}")

    
