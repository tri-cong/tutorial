import scrapy


class QuotesSpider(scrapy.Spider):
    name = "myspider"
    start_urls = ["https://docs.scrapy.org/"]
    allowed_domains = ['docs.scrapy.org']

    def parse(self, response):
        for detail in response.css('div.document'):
            yield {
                'h1': detail.css('section h1::text').extract_first(),
                'h2': detail.css('section h2::text').extract_first(),
                'content': detail.css('p::text').extract()
            }

        links = response.css('a::attr(href)').extract()
        for link in links:
            if link.startswith('https://docs.scrapy.org/'):
                yield scrapy.Request(link, callback=self.parse)
            else:
                yield scrapy.Request(response.urljoin(link), callback=self.parse)

        yield {
            'url': response.url,
        }