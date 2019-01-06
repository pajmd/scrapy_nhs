from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.nhs_spider import NhsSpider


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process = CrawlerProcess(get_project_settings())
    process.crawl(NhsSpider)
    process.start()  # the script will block here until the crawling is finished
