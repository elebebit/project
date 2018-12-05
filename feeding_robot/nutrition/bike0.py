
## How to exectute?
## scrapy runspider bike_spider.py -o result.csv

import scrapy
import csv

class NutritionSpider(scrapy.Spider):
	
	name = "NutritionSpider"
	start_urls = [
	'https://baikebcs.bdimg.com/baike-other/nutrition_module/173346.html',
	]

	def parse(self, response):
		fl=[]
		fe=[]

		ft=response.css('title::text').extract()
		f0=''.join(str(a) for a in ft)
		fn=f0.split('e')[1]
		for quote in response.css('tr'):
			print("\n---------------------------------------")
			data= quote.css('div::text').extract()

			if data[0] != '项目':

				fl.append(data[0])
				fe.append(data[1])

				if len(data)>=4:
					fl.append(data[3])
					fe.append(data[4])


		print("fl=",fl)
		print('fe=',fe)
		with open("td.csv","w") as csvfile: 
			wr = csv.writer(csvfile)
			wr.writerow(list(fn))
			wr.writerow(fl)
			wr.writerow(fe)

