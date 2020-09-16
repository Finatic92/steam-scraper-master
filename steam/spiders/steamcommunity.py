import scrapy

group = 'KeyVendorNet'

class SteamCommunity(scrapy.Spider):
    name = 'Steam Community'

    base_url = 'http://steamcommunity.com/app/227680/eventcomments/1631915072539961227'
    #base_url += '?p={}'

    start_urls = [
        'http://steamcommunity.com/app/227680/eventcomments/1631915072539961227'
    ]

    def parse(self, response):
        last_page = response.css('.commentthread_comment_text::text').extract()[-1]
        #for n in range(2, int(last_page) + 1):
        for n in range(1, 10):
            yield scrapy.Request(
                self.base_url.format(n), callback=self.extract_members)

    def extract_members(self, response):
        for href in response.css('.linkFriend::attr(href)'):
            yield { 'href': href.extract() }


# scrapy runspider steamcommunity.py -s USER_AGENT=Mozilla/5.0 -o links.csv
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36


# sc= SteamCommunity(scrapy.Spider)
# sc.parse()
# print(sc.name)