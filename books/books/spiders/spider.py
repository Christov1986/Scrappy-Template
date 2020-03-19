# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        all_the_books = response.xpath('//article[@class="product_pod"]')

        for books in all_the_books:
            book_url = self.start_urls[0] + books.xpath('.//div[@class="image_container"]/a/@href').extract_first()

            if 'catalogue/' not in book_url:
                book_url = self.start_urls[0] + 'catalogue/' + \
                           books.xpath('.//div[@class="image_container"]/a/@href').extract_first()

            yield scrapy.Request(book_url, callback=self.parse_book)

        next_page_url = self.start_urls[0] + response.xpath('//li[@class="next"]/a/@href').extract_first()

        if 'catalogue/' not in next_page_url:
            next_page_url = self.start_urls[0] + 'catalogue/' + \
                            response.xpath('//li[@class="next"]/a/@href').extract_first()

        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_book(self, response):
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
