import scrapy

class StockItem(scrapy.Item):
	Project = scrapy.Field()
	data_100g = scrapy.Field()
	NRVs= scrapy.Field()
 
class NutritionSpider(scrapy.Spider):
	
	name = "NutritionSpider"
	start_urls = [
	'https://baikebcs.bdimg.com/baike-other/nutrition_module/1188630.html',
	]


	def parse(self, response):
		for quote in response.css('tr'):
			print("\n---------------------------------------")
			#print ("quote:",quote)
			data= quote.css('div::text').extract()
			print('data:',data)

			if data[0] != '项目':
				item = StockItem()
				item['Project'] =  data[0]
				item['data_100g'] =  data[1]
				item['NRVs'] = data[2]	
				yield item

				item = StockItem()			
				item['Project'] =   data[3]
				item['data_100g'] =  data[4]
				item['NRVs'] = data[5]
				yield item

			else:	
				continue	
            
# scrapy runspider bike_spider.py -o nur.csv

            
