# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        all_the_books = response.xpath('//article')

        for books in all_the_books:
            title = books.xpath('.//h3/a/@title').extract_first()
            price = books.xpath('.//div[@class="product_price"]/p[@class="price_color"]/text()').extract_first()
            image_url = self.start_urls[0] + books.xpath('.//img/@src').extract_first()
            book_url = self.start_urls[0] + books.xpath('.//div[@class="image_container"]/a/@href').extract_first()
            print(title + " @ " + price)
            print(image_url)
            print(book_url)
