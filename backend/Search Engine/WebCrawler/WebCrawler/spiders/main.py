from scrapy.crawler import CrawlerProcess
from EazApplybot import EazApplySpider

def run_spider():
    process = CrawlerProcess(settings={
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': False,
    })
    process.crawl(EazApplySpider, capacity=5, refill_time=5, refill_amount=1)
    process.start()

if __name__ == '__main__':
    run_spider()