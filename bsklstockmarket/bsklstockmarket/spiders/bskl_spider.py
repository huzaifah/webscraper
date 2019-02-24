import scrapy
# from selenium import webdriver
# from time import sleep
# from random import randint

class BsklSpider(scrapy.Spider):
    name = 'bskl'

    start_urls = [
        'https://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value=0'
    ]

    def __init__(self):
        #self.driver = webdriver.Chrome()
        pass

    def exportPage(self, response):
        page = response.url.split("/")[-1]
        filename = 'bskl-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse(self, response):
        for href in response.css('td.filteringSelection a::attr(href)'):
            #yield response.follow(href, self.exportPage)
            yield response.follow(href, self.parse_stock_info)

    def parse_stock_info(self, response):
        stockListInPage = response.css('table#MainContent_tStock tr')
        for stock in stockListInPage[1:]:
            yield {
                'company': stock.css('h3 a::text').get(default='').strip(),
                'name': stock.css('h3:nth-child(3)::text').get(default='').strip(),
                'price': stock.css('td:nth-child(5)::text').get(default='').strip(),
                'sourceUrl': response.url.split("/")[-1]
            }