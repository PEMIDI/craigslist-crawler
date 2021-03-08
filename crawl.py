import requests
import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from parser import AdvertisementParser
from storage import MongoStore, FileStore
from config import STORAGE_TYPE


class BaseCrawler(ABC):

    def __init__(self):
        self.storage = self.__set_storage()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStore()
        return FileStore()


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
        super().__init__()

    @staticmethod
    def find_links(html_doc):
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
        self.storage.store(data, 'adv_links')

    def start(self):
        adv_links = []
        for city in self.cities:
            result = self.crawl_cities(self.url.format(city))
            print(f"{city} | {len(result)}")
            adv_links.extend(result)

        self.store([{'url': li.get('href'), 'flag': False} for li in adv_links])


class DataCrawler(BaseCrawler):

    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementParser()

    def __load_links(self):
        return self.storage.load()

    def start(self, store=False):
        for li in self.links:
            response = self.get(li['url'])
            data = self.parser.parse(response.text)
            if store:
                self.store(data, 'adv_data')
            self.storage.update_flag(li)

    def store(self, data, filename):
        self.storage.store(data, filename)


class ImageDownloader(BaseCrawler):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.advertisements = self.__load_advertisements()

    def __load_advertisements(self):
        return self.storage.load('adv_data')

    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.HTTPError:
            return None
        return response

    def start(self, store=True):
        for advertisements in self.advertisements:
            counter = 1
            for image in advertisements['images']:
                response = self.get(image['url'])
                if store:
                    self.store(response, advertisements['post_id'], counter)
                counter += 1

    def store(self, data, adv_id, img_number):
        filename = f"{adv_id}-{img_number}"
        return self.save_to_disk(data, filename)

    @staticmethod
    def save_to_disk(response, filename):
        with open(f'fixtures/images/{filename}.jpg', 'ab') as f:
            f.write(response.content)
            for _ in response.iter_content():
                f.write(response.content)

        print(filename)
        return filename