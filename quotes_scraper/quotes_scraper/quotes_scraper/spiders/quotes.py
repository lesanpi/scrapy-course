import scrapy

XPATHS = {
    "title": "//h1/a/text()",
    "quotes": "//span[@class='text' and @itemprop='text']/text()",
    "top-ten": "//div[contains(@class, 'tags-box')]/span[@class='tag-item']/a/text()",
    "next-page": "//ul[@class='pager']//li[@class='next']/a/@href"
}

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['lespinerua@gmail.com'],
        'ROBOTSTXT_OBEY': True, 
        'USER_AGENT': 'PepitoMartinez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        
        quotes.extend(response.xpath(XPATHS['quotes']).getall())
        next_page_button_link = response.xpath(XPATHS['next-page']).get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):
        
        title = response.xpath(XPATHS['title']).get()
        quotes = response.xpath(XPATHS['quotes']).getall()
        top_ten_tags = response.xpath(XPATHS['top-ten']).getall()

        top = getattr(self, 'top', None)
        if top: 
            top = int(top)
            top_tags = top_ten_tags[:top]

        results = {
            'title': title,
            'tags': top_tags
        }
        yield results

        next_page_button_link = response.xpath(XPATHS['next-page']).get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})

        