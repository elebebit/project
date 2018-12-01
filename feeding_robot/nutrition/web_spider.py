import scrapy

class StockItem(scrapy.Item):
	NurUrl = scrapy.Field()
 
class urlSpider(scrapy.Spider):
	
	name = "urlSpider"
	start_urls = [
	'https://baike.baidu.com/item/%E7%B3%96%E9%86%8B%E9%B1%BC',
	]

	def parse(self, response):

		for sele in response.css('iframe'):

			ifr=sele.xpath('descendant-or-self::iframe').extract()

			for data in ifr:

				ls=data.split(' ')
				#print('x4',x4)

			for index in ls:
				if str('src') in index:
					url=index.split('"')[1]
					print('****************************')
					print(url)
					item = StockItem()
					item['NurUrl'] = url
					yield item	
				else:
					continue
