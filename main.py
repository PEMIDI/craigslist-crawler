from crawl import Link_crawler
import sys
from config import BASE_LINK




if __name__ == "__main__":
    link = BASE_LINK
    crawler = Link_crawler(link, cities=['london', 'munich'])
    crawler.start()
    
    # print()