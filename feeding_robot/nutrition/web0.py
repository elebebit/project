## How to exectute?
## scrapy runspider web_psider.py -o result.csv

import scrapy
import csv

class StockItem(scrapy.Item):
	NurUrl = scrapy.Field()
	Food = scrapy.Field()
 
class urlSpider(scrapy.Spider):

	start_urls=[]

	with open ('result.csv') as f:
		f_csv=csv.reader(f)
		headings = next(f_csv)
		for r in f_csv:
			fn = ''.join(str(a) for a in r)
			#global fn

			name = "urlSpider"
			start_urls.append('https://baike.baidu.com/item/'+fn) 

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
						#item['Food'] = fn
						yield item	
					else:
						continue
