import scrapy

class EazApplySpider(scrapy.Spider):
    name = 'EazApplybot'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        page = response.url.split("//")[-1].split("/")[0]
        filename = f'/home/vithursh/Coding/EazApply/backend/File Data/Raw HTML Pages/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')