import scrapy
 
class StockItem(scrapy.Item):
    stockcode       = scrapy.Field()
    doclink         = scrapy.Field()
    doctype         = scrapy.Field()
    companyname     = scrapy.Field()
    companyurl      = scrapy.Field()
 
class CompanySpider(scrapy.Spider):
    name = "CompanySpider"
    start_urls = [
        'http://japan-ar.com/list.html',
    ]
 
    def parse(self, response):
        for quote in response.css('tr'):
            print ("quote:")
            text = quote.xpath('descendant-or-self::a/text()').extract()
            print (quote.css('span+*::text').extract())
#            if quote.css('a::text').extract_first() == 'AR' or quote.css('a::text').extract_first() == 'IR' :
            if quote.css('a::text').extract_first() == 'AR':
                item = StockItem()
                item['stockcode']   =   quote.css('td::text').extract_first()
                item['doctype']     =   quote.css('a::text').extract_first()
                item['doclink']     =   quote.css('a::attr(href)').extract_first()
                item['companyname'] =   quote.css('span+*::text').extract()[0]
                item['companyurl']  =   quote.css('span+*::attr(href)').extract()[0]
                yield item
 
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
# scrapy runspider bike_spider.py -o nur.csv

            
