# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SpiderSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = [Rule(LinkExtractor(allow='catalogue/'), callback='parse_filter_book', follow=True)]

    def parse_filter_book(self, response):

        exist = response.xpath('//div[@id="product_gallery"]').extract_first()

        if exist:
            title = response.xpath('//div/h1/text()').extract_first()
            image_url = self.start_urls[0] + response.xpath('//div/img/@src').extract_first().replace('../../', '')
            price = response.xpath('//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
            stock = response.xpath('//div[contains(@class, "product_main")]/'
                                   'p[@class="instock availability"]/text()').extract()[1].strip()
            star_rating = response.xpath('//div[contains(@class, "product_main")]/p[contains(@class, "star-rating")]/'
                                         '@class').extract_first().replace('star-rating ', '')
            description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').extract_first()
            upc_code = response.xpath('//tr[1]/td/text()').extract_first()
            price_excl = response.xpath('//tr[3]/td/text()').extract_first()
            price_incl = response.xpath('//tr[4]/td/text()').extract_first()
            tax = response.xpath('//tr[5]/td/text()').extract_first()

            yield{
            'Title' : title,
            'Image URL' : image_url,
            'Price' : price,
            'Stock level' : stock,
            'Star rating' : star_rating,
            'Description' : description,
            'UPC code' : upc_code,
            'Price excluding tax' : price_excl,
            'Price including tax' : price_incl,
            'Tax' : tax
            }

        else:
            print(exist)
