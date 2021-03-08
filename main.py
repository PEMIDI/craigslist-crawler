from crawl import LinkCrawler, DataCrawler, ImageDownloader
import sys
from config import BASE_LINK




if __name__ == "__main__":
    link = BASE_LINK

    #get links
    # crawler = LinkCrawler(link, cities=['london', 'munich'])
    # crawler.start()
    #

    #get data
    # crawler = DataCrawler()
    # crawler.start(store=True)



    #get images
    crawler = ImageDownloader()
    crawler.start(store=True)