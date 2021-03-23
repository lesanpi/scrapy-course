import scrapy

XPATHS = {
    'links': '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href',
    'title': '//h1[@class="documentFirstHeading"]/text()',
    'body': '//div[@class="field-item even"]//p[not(@class)]/text()'
}

class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = ['https://www.cia.gov/library/readingroom/historical-collections']
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath(XPATHS['links']).getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(XPATHS['title']).get()
        body = response.xpath(XPATHS['body']).get()

        results = {
            'url': link,
            'title': title,
            'body': body
        }
        print('*'*20)
        print('\n'*3)
        print(results)
        print('\n'*3)
        print('*'*20)
        yield results