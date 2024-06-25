import scrapy


class ProfilesSpider(scrapy.Spider):
    name = "profiles"
    allowed_domains = ["bbb.org"]
    start_urls = ["https://bbb.org"]

    def parse(self, response):
        pass
