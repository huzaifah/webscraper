import scrapy
from scrapy_splash import SplashRequest

class BsklSpider(scrapy.Spider):
    name = 'thestar'

    start_urls = [
        'https://www.thestar.com.my/business/marketwatch/stock-list/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, 
            self.parse, 
            endpoint='render.html',
            args={'wait': 10})

    def exportPage(self, response):
        page = response.url.split("/")[-1]
        filename = 'thestar-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def parse(self, response):
        query_list = response.css('div#glossarynavi a::attr(data-value)').getall()
        for alphabet in query_list:
            url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet=' + str(alphabet)
            yield SplashRequest(url, 
                self.parse_list, 
                endpoint='render.html',
                args={'wait': 10})

    def parse_list(self, response):
        stock_list_in_page = response.css('table#marketwatchtable tr')
        for stock in stock_list_in_page[1:]:
            stock_url = stock.css('td a::attr(href)').get(default='').strip()
            url = 'https://www.thestar.com.my' + str(stock_url)
            self.log('visit %s' % url)
            yield response.follow(url, 
                self.parse_stock_info)

    def parse_stock_info(self, response):
        yield {
            'counter': response.url.split("=")[-1],
            'board': response.css('li.f14::text').getall()[0][3:].strip(),
            'stock_code': response.css('li.f14::text').getall()[1][3:].strip(),
            'stock_name': response.css('h1.stock-profile::text').get(default='').strip(),
            'logged_date': response.css('span#slcontent_0_ileft_0_datetxt::text').get(default='')[10:-2].strip(),
            'logged_time': response.css('span.time::text').get(default='').strip(),
            'open_price': response.css('td#slcontent_0_ileft_0_opentext::text').get(default='').strip(),
            'high_price': response.css('td#slcontent_0_ileft_0_hightext::text').get(default='').strip(),
            'low_price': response.css('td#slcontent_0_ileft_0_lowtext::text').get(default='').strip(),
            'last_price': response.css('td#slcontent_0_ileft_0_lastdonetext::text').get(default='').strip()
        }