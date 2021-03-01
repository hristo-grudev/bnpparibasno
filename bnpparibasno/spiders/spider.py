import scrapy

from scrapy.loader import ItemLoader
from ..items import BnpparibasnoItem
from itemloaders.processors import TakeFirst


class BnpparibasnoSpider(scrapy.Spider):
	name = 'bnpparibasno'
	start_urls = ['https://www.bnpparibas.no/en/news-press/all-our-news/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href')
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="nextpostslink"]/@href')
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]/descendant-or-self::*/text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description)
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=BnpparibasnoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()