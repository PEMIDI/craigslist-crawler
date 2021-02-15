from crawl import LinkCrawler, DataCrawler
import sys
from config import BASE_LINK




if __name__ == "__main__":
    link = BASE_LINK

    # crawler = LinkCrawler(link, cities=['london', 'munich'])
    # crawler.start()
    #
    crawler = DataCrawler()
    crawler.start(store=True)
    #
