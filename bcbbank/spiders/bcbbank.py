import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bcbbank.items import Article


class BcbbankSpider(scrapy.Spider):
    name = 'bcbbank'
    start_urls = ['https://www.bcb.bank/about-bcb/news']

    def parse(self, response):
        articles = response.xpath('//div[@class="news-item hidden-content m-b-md"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = "".join(article.xpath('.//h2/text()').getall())
            date = article.xpath('.//div[@class="sort-date"]/div/text()').get()

            content = article.xpath('./div[@class="news-content"]/div[3]//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



