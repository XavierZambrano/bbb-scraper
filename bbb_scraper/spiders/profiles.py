import scrapy
from scrapy.spiders import SitemapSpider
import json


class ProfilesSpider(SitemapSpider):
    name = "profiles"
    allowed_domains = ["bbb.org"]
    sitemap_urls = [
        'https://www.bbb.org/robots.txt',
        # 'https://www.bbb.org/sitemap-accredited-business-profiles-1.xml'  # for quick test
    ]
    sitemap_rules = [
        ('/profile/', 'parse'),
    ]

    def parse(self, response):
        script_text = response.xpath('//script[contains(text(), "window.__PRELOADED_STATE__")]').get()
        data_raw = script_text.split('window.__PRELOADED_STATE__ = ')[1].split(';</script>')[0]
        data = json.loads(data_raw)

        categories = [category['title'] for category in data['businessProfile']['categories']['links']]
        yield {
            'url': response.url,
            'id': data['analytics']['legacyDataLayer']['businessInfo']['businessId'],
            'name': data['analytics']['legacyDataLayer']['businessInfo']['name'],
            'address': data['businessProfile']['location']['formattedAddress'],
            'website': data['businessProfile']['urls'].get('primary'),
            'phone_number': data['businessProfile']['contactInformation']['phoneNumber'],
            'categories': categories,
        }

