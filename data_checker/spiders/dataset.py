import scrapy

from data_checker.items import Dataset

class DatasetSpider(scrapy.Spider):
    name = 'dataset'
    allowed_domains = ['catalog.data.gov']
    start_urls = ['http://catalog.data.gov/']
    max_page = 5
    temp = '/Users/jennynguyen/Downloads/'

    # Define custom setting to save the output
    custom_settings = {
        'FEED_FORMAT': 'json',
        # 'FEED_URI': './output/%(time)s.json'
        'FEED_URI': temp + 'output/%(time)s.json'
    }

    # Pagination to retrieve all pages
    def parse(self, response):
        host = response.url.split("/dataset")[0]
        for dataset in response.css(".dataset-content"):
            yield Dataset(
                name=dataset.css("h3.dataset-heading > a::text").get(),
                link=host + dataset.css("h3.dataset-heading > a::attr(href)").get(),
                organization=dataset.css(".dataset-organization::text").get().strip(" —")
            )
        
        for link in response.css(".pagination > ul > li:last-child:not(.active) > a"):
            total_page = int(link.attrib['href'].split("=")[1])
            if total_page > self.max_page:
                break
            yield response.follow(link, callback = self.parse)

# https://docs.scrapy.org/en/latest/topics/selectors.html
#        
